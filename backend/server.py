import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
from pymongo import MongoClient
from fastapi.responses import JSONResponse
import swisseph as swe
import math
from datetime import datetime

# Environment
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "test_database")

# Initialize FastAPI
app = FastAPI()

# Initialize MongoDB connection
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Models ---------

class BirthChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hours: int
    minutes: int
    seconds: int = 0
    latitude: float
    longitude: float
    timezone: float
    ayanamsha: str = "lahiri"

class Planet(BaseModel):
    name: str
    degrees: float
    sign: str
    house: int
    retrograde: bool

class BirthChartResponse(BaseModel):
    planets: List[Planet]
    chart_url: Optional[str] = None

# --------- Astrological Functions ---------

# Zodiac signs
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", 
    "Leo", "Virgo", "Libra", "Scorpio", 
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Planet names
PLANET_NAMES = {
    swe.SUN: "Sun", 
    swe.MOON: "Moon", 
    swe.MERCURY: "Mercury",
    swe.VENUS: "Venus", 
    swe.MARS: "Mars", 
    swe.JUPITER: "Jupiter",
    swe.SATURN: "Saturn", 
    swe.URANUS: "Uranus", 
    swe.NEPTUNE: "Neptune",
    swe.PLUTO: "Pluto", 
    swe.MEAN_NODE: "Rahu (North Node)"
}

def get_ayanamsha_flag(ayanamsha: str):
    """Convert ayanamsha string to Swiss Ephemeris constant."""
    mapping = {
        "lahiri": swe.SIDM_LAHIRI,
        "fagan_bradley": swe.SIDM_FAGAN_BRADLEY,
        "krishnamurti": swe.SIDM_KRISHNAMURTI,
        "raman": swe.SIDM_RAMAN
    }
    return mapping.get(ayanamsha, swe.SIDM_LAHIRI)

def get_zodiac_sign(longitude: float) -> str:
    """Get zodiac sign from longitude."""
    sign_num = int(longitude / 30)
    return SIGNS[sign_num]

def calculate_birth_chart(birth_data: BirthChartRequest) -> BirthChartResponse:
    """Calculate sidereal birth chart using Swiss Ephemeris."""
    # Calculate Julian day
    julian_day = swe.julday(
        birth_data.year, birth_data.month, birth_data.day,
        birth_data.hours + birth_data.minutes/60.0 + birth_data.seconds/3600.0 - birth_data.timezone
    )
    
    # Set ayanamsha for sidereal calculations
    swe.set_sid_mode(get_ayanamsha_flag(birth_data.ayanamsha))
    
    # Calculate Ascendant (first house cusp)
    houses, ascmc = swe.houses(
        julian_day, birth_data.latitude, birth_data.longitude, b'P'
    )
    ascendant = houses[0]
    
    # Initialize planets list
    planets = []
    
    # Calculate positions for each planet
    for planet_id, planet_name in PLANET_NAMES.items():
        try:
            # Calculate planetary position with sidereal flag
            flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
            result, status = swe.calc_ut(julian_day, planet_id, flags)
            
            longitude = result[0]
            retrograde = result[3] < 0  # Negative speed means retrograde
            
            # Calculate house position
            house = 1
            for i in range(12):
                house_cusp = houses[i]
                next_cusp = houses[(i + 1) % 12]
                
                # Handle case where house crosses 0° Aries
                if next_cusp < house_cusp:
                    if longitude >= house_cusp or longitude < next_cusp:
                        house = i + 1
                        break
                else:
                    if house_cusp <= longitude < next_cusp:
                        house = i + 1
                        break
            
            # Create planet object
            planet = Planet(
                name=planet_name,
                degrees=longitude % 30,  # Degrees within sign
                sign=get_zodiac_sign(longitude),
                house=house,
                retrograde=retrograde
            )
            
            planets.append(planet)
        except Exception as e:
            print(f"Error calculating {planet_name}: {e}")
    
    # Create response
    return BirthChartResponse(
        planets=planets,
        # No chart URL for now, we could generate this with matplotlib or another library
        chart_url=None
    )

# --------- Routes ---------

@app.get("/api/")
def read_root():
    return {"message": "Sidereal Astrology API is running!"}

@app.post("/api/birth-chart", response_model=BirthChartResponse)
def birth_chart(request: BirthChartRequest):
    try:
        chart = calculate_birth_chart(request)
        
        # Save the request in MongoDB for history
        chart_data = {
            "id": str(uuid.uuid4()),
            "request": request.dict(),
            "timestamp": datetime.now(),
            "planets": [planet.dict() for planet in chart.planets]
        }
        db.birth_charts.insert_one(chart_data)
        
        return chart
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
def get_history():
    try:
        history = list(db.birth_charts.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Shutdown event handler
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()
