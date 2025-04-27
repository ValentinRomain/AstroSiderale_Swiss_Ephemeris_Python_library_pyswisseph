import React, { useState } from 'react';
import './App.css';

function App() {
  const [birthData, setBirthData] = useState({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
    day: new Date().getDate(),
    hours: 12,
    minutes: 0,
    seconds: 0,
    latitude: '',
    longitude: '',
    timezone: '',
    ayanamsha: 'lahiri'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('12:00');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBirthData({
      ...birthData,
      [name]: value
    });
  };

  const handleDateChange = (e) => {
    const date = new Date(e.target.value);
    setBirthDate(e.target.value);
    
    if (!isNaN(date.getTime())) {
      setBirthData({
        ...birthData,
        year: date.getFullYear(),
        month: date.getMonth() + 1,
        day: date.getDate()
      });
    }
  };

  const handleTimeChange = (e) => {
    const timeStr = e.target.value;
    setBirthTime(timeStr);
    
    const [hours, minutes] = timeStr.split(':').map(Number);
    
    setBirthData({
      ...birthData,
      hours,
      minutes
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${BACKEND_URL}/api/birth-chart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(birthData)
      });

      if (!response.ok) {
        throw new Error('Failed to calculate birth chart');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error('Error calculating birth chart:', err);
      setError('Failed to calculate birth chart. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSignEmoji = (sign) => {
    const signEmojis = {
      'Aries': '♈',
      'Taurus': '♉',
      'Gemini': '♊',
      'Cancer': '♋',
      'Leo': '♌',
      'Virgo': '♍',
      'Libra': '♎',
      'Scorpio': '♏',
      'Sagittarius': '♐',
      'Capricorn': '♑',
      'Aquarius': '♒',
      'Pisces': '♓'
    };
    return signEmojis[sign] || '';
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Sidereal Astrology Birth Chart Calculator</h1>
        <p className="subtitle">Calculate your accurate birth chart using sidereal zodiac</p>
      </header>

      <main className="main-content">
        <div className="container">
          <div className="left-panel">
            <div className="form-container">
              <h2>Enter Your Birth Details</h2>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="birthDate">Birth Date:</label>
                  <input
                    type="date"
                    id="birthDate"
                    value={birthDate}
                    onChange={handleDateChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="birthTime">Birth Time:</label>
                  <input
                    type="time"
                    id="birthTime"
                    value={birthTime}
                    onChange={handleTimeChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="latitude">Latitude:</label>
                  <input
                    type="number"
                    id="latitude"
                    name="latitude"
                    step="0.000001"
                    value={birthData.latitude}
                    onChange={handleInputChange}
                    placeholder="e.g. 51.5074"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="longitude">Longitude:</label>
                  <input
                    type="number"
                    id="longitude"
                    name="longitude"
                    step="0.000001"
                    value={birthData.longitude}
                    onChange={handleInputChange}
                    placeholder="e.g. -0.1278"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="timezone">Timezone Offset (hours):</label>
                  <input
                    type="number"
                    id="timezone"
                    name="timezone"
                    step="0.5"
                    value={birthData.timezone}
                    onChange={handleInputChange}
                    placeholder="e.g. +1, -5"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="ayanamsha">Ayanamsha:</label>
                  <select
                    id="ayanamsha"
                    name="ayanamsha"
                    value={birthData.ayanamsha}
                    onChange={handleInputChange}
                  >
                    <option value="lahiri">Lahiri</option>
                    <option value="fagan_bradley">Fagan-Bradley</option>
                    <option value="krishnamurti">Krishnamurti</option>
                    <option value="raman">Raman</option>
                  </select>
                </div>

                <button type="submit" className="calculate-btn" disabled={loading}>
                  {loading ? 'Calculating...' : 'Calculate Birth Chart'}
                </button>
              </form>
            </div>
          </div>

          <div className="right-panel">
            {loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Calculating your sidereal birth chart...</p>
              </div>
            )}

            {error && <div className="error-message">{error}</div>}

            {results && !loading && (
              <div className="results">
                <h2>Your Sidereal Birth Chart</h2>
                
                <div className="planets-table">
                  <div className="planets-header">
                    <div>Planet</div>
                    <div>Sign</div>
                    <div>Degrees</div>
                    <div>House</div>
                  </div>
                  
                  {results.planets.map((planet, index) => (
                    <div className="planet-row" key={index}>
                      <div className="planet-name">
                        {planet.name} {planet.retrograde && '(R)'}
                      </div>
                      <div className="planet-sign">
                        {getSignEmoji(planet.sign)} {planet.sign}
                      </div>
                      <div className="planet-degrees">
                        {planet.degrees.toFixed(2)}°
                      </div>
                      <div className="planet-house">
                        {planet.house}
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="info-box">
                  <h3>About Sidereal Astrology</h3>
                  <p>
                    Sidereal astrology takes into account the precession of the equinoxes, resulting in 
                    a zodiac that is aligned with the actual constellations in the sky. This system is widely used 
                    in Vedic/Indian astrology and differs from the more common Western tropical system.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>
          Sidereal Astrology Birth Chart Calculator &copy; {new Date().getFullYear()}
        </p>
        <p className="footnote">
          Calculations performed using Swiss Ephemeris
        </p>
      </footer>
    </div>
  );
}

export default App;