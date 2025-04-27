document.addEventListener('DOMContentLoaded', function() {
  const calculateBtn = document.getElementById('calculateBtn');
  const loading = document.getElementById('loading');
  const results = document.getElementById('results');
  const error = document.getElementById('error');
  const chartContainer = document.getElementById('chartContainer');
  const planetaryPositions = document.getElementById('planetaryPositions');
  
  const BACKEND_URL = 'https://11bc0d6b-635a-418a-aab1-c1c7088ce225.preview.emergentagent.com';
  
  calculateBtn.addEventListener('click', function() {
    // Validate inputs
    const birthdate = document.getElementById('birthdate').value;
    const birthtime = document.getElementById('birthtime').value;
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    const timezone = document.getElementById('timezone').value;
    const ayanamsha = document.getElementById('ayanamsha').value;
    
    if (!birthdate || !birthtime || !latitude || !longitude || !timezone) {
      alert('Please fill in all required fields');
      return;
    }
    
    // Show loading
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
    
    // Parse date and time
    const dateObj = new Date(`${birthdate}T${birthtime}`);
    const year = dateObj.getFullYear();
    const month = dateObj.getMonth() + 1; // JavaScript months are 0-indexed
    const day = dateObj.getDate();
    const hours = dateObj.getHours();
    const minutes = dateObj.getMinutes();
    
    // Prepare data for API request
    const requestData = {
      year,
      month,
      day,
      hours,
      minutes,
      seconds: 0,
      latitude: parseFloat(latitude),
      longitude: parseFloat(longitude),
      timezone: parseFloat(timezone),
      ayanamsha
    };
    
    // Call our backend API
    fetch(`${BACKEND_URL}/api/birth-chart`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Hide loading
      loading.classList.add('hidden');
      
      // Display results
      results.classList.remove('hidden');
      
      // Display chart image if available
      if (data.chart_url) {
        chartContainer.innerHTML = `<img src="${data.chart_url}" alt="Birth Chart" style="max-width: 100%;">`;
      } else {
        chartContainer.innerHTML = '<p>Chart visualization not available</p>';
      }
      
      // Display planetary positions
      planetaryPositions.innerHTML = '';
      data.planets.forEach(planet => {
        const planetRow = document.createElement('div');
        planetRow.className = 'planet-row';
        planetRow.innerHTML = `
          <span class="planet-name">${planet.name}</span>
          <span>${planet.sign} ${planet.degrees.toFixed(2)}° ${planet.retrograde ? '(R)' : ''}</span>
        `;
        planetaryPositions.appendChild(planetRow);
      });
    })
    .catch(err => {
      console.error('Error:', err);
      loading.classList.add('hidden');
      error.classList.remove('hidden');
    });
  });
});