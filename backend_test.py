
import requests
import json
import sys
from datetime import datetime

class AstrologyAPITester:
    def __init__(self, base_url="https://11bc0d6b-635a-418a-aab1-c1c7088ce225.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_details = response.json()
                    print(f"Error details: {json.dumps(error_details, indent=2)}")
                except:
                    print(f"Response text: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_api_root(self):
        """Test API root endpoint"""
        return self.run_test(
            "API Root",
            "GET",
            "api/",
            200
        )

    def test_birth_chart(self, birth_data):
        """Test birth chart calculation"""
        return self.run_test(
            "Birth Chart Calculation",
            "POST",
            "api/birth-chart",
            200,
            data=birth_data
        )

    def test_history(self):
        """Test history endpoint"""
        return self.run_test(
            "Chart History",
            "GET",
            "api/history",
            200
        )

    def test_invalid_data(self):
        """Test with invalid data"""
        invalid_data = {
            "year": 1990,
            "month": 15,  # Invalid month
            "day": 15,
            "hours": 14, 
            "minutes": 30,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": -4
        }
        return self.run_test(
            "Invalid Data Handling",
            "POST", 
            "api/birth-chart",
            400,  # Should return Bad Request
            data=invalid_data
        )

def main():
    # Setup
    tester = AstrologyAPITester("https://11bc0d6b-635a-418a-aab1-c1c7088ce225.preview.emergentagent.com")
    
    # Test sample birth data (New York coordinates)
    birth_data = {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hours": 14,
        "minutes": 30,
        "seconds": 0,
        "latitude": 40.7128,  # New York
        "longitude": -74.0060,
        "timezone": -4,
        "ayanamsha": "lahiri"
    }

    # Run tests
    print("\n=== Testing Sidereal Astrology API ===\n")
    
    # Test 1: API Root
    root_success, root_response = tester.test_api_root()
    if root_success:
        print(f"API Message: {root_response.get('message', '')}")
    
    # Test 2: Birth Chart Calculation (with requested test data)
    chart_success, chart_response = tester.test_birth_chart(birth_data)
    if chart_success:
        print("\nBirth Chart Results:")
        planets = chart_response.get("planets", [])
        for planet in planets:
            retrograde = " (R)" if planet.get("retrograde", False) else ""
            print(f"  {planet.get('name')}: {planet.get('sign')} {planet.get('degrees'):.2f}° (House {planet.get('house')}){retrograde}")
    
    # Test 3: History
    history_success, history_response = tester.test_history()
    if history_success:
        history_entries = history_response.get("history", [])
        print(f"\nHistory entries found: {len(history_entries)}")
        if history_entries:
            print(f"Most recent entry: {history_entries[0].get('timestamp', '')}")
    
    # Test 4: Invalid Data Handling
    invalid_success, invalid_response = tester.test_invalid_data()
    if invalid_success:
        print("Invalid data handling works correctly")
    else:
        print("Note: The API did not return the expected 400 status code for invalid data")

    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
