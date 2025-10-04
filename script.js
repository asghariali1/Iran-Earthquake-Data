// GitHub Pages optimized script - no CORS proxy needed
let earthquakeData = [];
let map;
let magnitudeChart, timelineChart, depthMagnitudeChart, monthlyChart;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    loadEarthquakeData();
    setupEventListeners();
    checkGitHubUpdate();
});

// Check GitHub Actions update status
function checkGitHubUpdate() {
    try {
        // Try to load data.json with timestamp to check freshness
        fetch('data.json?' + new Date().getTime())
            .then(response => {
                if (response.ok) {
                    const lastModified = response.headers.get('Last-Modified');
                    if (lastModified) {
                        const updateTime = new Date(lastModified);
                        document.getElementById('last-github-update').innerHTML = 
                            `Last updated: ${updateTime.toLocaleString()}`;
                    } else {
                        document.getElementById('last-github-update').innerHTML = 
                            'Data loaded successfully from GitHub';
                    }
                }
            })
            .catch(error => {
                console.log('GitHub update check:', error);
                document.getElementById('last-github-update').innerHTML = 
                    'GitHub auto-update active';
            });
    } catch (error) {
        console.log('Update check error:', error);
    }
}

// Load earthquake data from JSON file
function loadEarthquakeData() {
    // Load from local data.json file (updated by GitHub Actions)
    fetch('data.json?' + new Date().getTime())
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text(); // Get as text first
        })
        .then(text => {
            // Parse JSONL format (one JSON object per line)
            const lines = text.trim().split('\n');
            const data = [];
            
            for (const line of lines) {
                if (line.trim()) {
                    try {
                        const earthquake = JSON.parse(line);
                        // Convert timestamp to readable datetime if needed
                        if (earthquake.time && !earthquake.datetime) {
                            earthquake.datetime = new Date(earthquake.time).toISOString();
                        }
                        // Ensure magnitude is properly named
                        if (earthquake.mag && !earthquake.magnitude) {
                            earthquake.magnitude = earthquake.mag;
                        }
                        data.push(earthquake);
                    } catch (parseError) {
                        console.warn('Error parsing line:', line, parseError);
                    }
                }
            }
            
            console.log('Loaded earthquake data:', data.length, 'earthquakes');
            earthquakeData = data;
            updateOverviewStats();
            updateMapMarkers();
            updateCharts();
            updateDataTable();
        })
        .catch(error => {
            console.error('Error loading earthquake data:', error);
            // Show error message to user
            document.getElementById('total-earthquakes').textContent = 'Error loading data';
            document.getElementById('last-github-update').innerHTML = 
                'Error loading data - please refresh page';
        });
}

// Setup event listeners
function setupEventListeners() {
    // Magnitude filter for map
    const magnitudeFilter = document.getElementById('magnitude-filter');
    const magnitudeValue = document.getElementById('magnitude-value');
    
    magnitudeFilter.addEventListener('input', function() {
        magnitudeValue.textContent = this.value;
        updateMapMarkers();
    });

    // Time period filter for timeline chart
    const timePeriod = document.getElementById('time-period');
    timePeriod.addEventListener('change', function() {
        updateTimelineChart();
    });

    // Table magnitude filter
    const tableMagnitudeFilter = document.getElementById('table-magnitude-filter');
    tableMagnitudeFilter.addEventListener('change', function() {
        updateDataTable();
    });
}

// Initialize Leaflet map
function initializeMap() {
    map = L.map('earthquake-map').setView([35.0, 53.0], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    
    // Add Iran boundary
    const iranBounds = [
        [25.205, 41.045],
        [40.447, 63.984]
    ];
    
    L.rectangle(iranBounds, {
        color: '#ff6b6b',
        weight: 2,
        fillOpacity: 0.1
    }).addTo(map).bindPopup('Iran Region Focus Area');
}

// Update overview statistics
function updateOverviewStats() {
    if (earthquakeData.length === 0) return;

    const totalEarthquakes = earthquakeData.length;
    const magnitudes = earthquakeData.map(eq => parseFloat(eq.magnitude)).filter(m => !isNaN(m));
    const avgMagnitude = magnitudes.reduce((a, b) => a + b, 0) / magnitudes.length;
    const maxMagnitude = Math.max(...magnitudes);
    
    // Get date range
    const dates = earthquakeData.map(eq => new Date(eq.datetime)).filter(d => !isNaN(d));
    const minDate = new Date(Math.min(...dates));
    const maxDate = new Date(Math.max(...dates));
    
    document.getElementById('total-earthquakes').textContent = totalEarthquakes.toLocaleString();
    document.getElementById('avg-magnitude').textContent = avgMagnitude.toFixed(1);
    document.getElementById('max-magnitude').textContent = maxMagnitude.toFixed(1);
    document.getElementById('date-range').textContent = 
        `${minDate.getFullYear()} - ${maxDate.getFullYear()}`;
}

// Update map markers
function updateMapMarkers() {
    if (!map) return;
    
    // Clear existing markers
    map.eachLayer(layer => {
        if (layer instanceof L.CircleMarker) {
            map.removeLayer(layer);
        }
    });
    
    const minMagnitude = parseFloat(document.getElementById('magnitude-filter').value);
    
    earthquakeData.forEach(earthquake => {
        const magnitude = parseFloat(earthquake.magnitude);
        if (isNaN(magnitude) || magnitude < minMagnitude) return;
        
        const lat = parseFloat(earthquake.latitude);
        const lon = parseFloat(earthquake.longitude);
        if (isNaN(lat) || isNaN(lon)) return;
        
        // Color based on magnitude
        let color, size;
        if (magnitude < 4) {
            color = '#4CAF50'; size = 5;
        } else if (magnitude < 6) {
            color = '#FF9800'; size = 8;
        } else if (magnitude < 7) {
            color = '#FF5722'; size = 12;
        } else {
            color = '#F44336'; size = 16;
        }
        
        const marker = L.circleMarker([lat, lon], {
            radius: size,
            fillColor: color,
            color: '#fff',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.7
        });
        
        marker.bindPopup(`
            <div class="popup-content">
                <h4>Magnitude ${magnitude}</h4>
                <p><strong>Location:</strong> ${earthquake.place || 'Unknown'}</p>
                <p><strong>Date:</strong> ${new Date(earthquake.datetime).toLocaleDateString()}</p>
                <p><strong>Depth:</strong> ${earthquake.depth || 'Unknown'} km</p>
                <p><strong>Coordinates:</strong> ${lat.toFixed(3)}, ${lon.toFixed(3)}</p>
            </div>
        `);
        
        marker.addTo(map);
    });
}

// Update all charts
function updateCharts() {
    updateMagnitudeChart();
    updateTimelineChart();
    updateDepthMagnitudeChart();
    updateMonthlyChart();
}

// Update magnitude distribution chart
function updateMagnitudeChart() {
    const ctx = document.getElementById('magnitude-chart').getContext('2d');
    
    // Destroy existing chart
    if (magnitudeChart) {
        magnitudeChart.destroy();
    }
    
    const magnitudes = earthquakeData.map(eq => parseFloat(eq.magnitude)).filter(m => !isNaN(m));
    const bins = {};
    
    magnitudes.forEach(mag => {
        const bin = Math.floor(mag * 2) / 2; // 0.5 intervals
        bins[bin] = (bins[bin] || 0) + 1;
    });
    
    const labels = Object.keys(bins).sort((a, b) => a - b);
    const data = labels.map(label => bins[label]);
    
    magnitudeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.map(l => `${l} - ${(parseFloat(l) + 0.5).toFixed(1)}`),
            datasets: [{
                label: 'Number of Earthquakes',
                data: data,
                backgroundColor: 'rgba(99, 102, 241, 0.7)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#ffffff' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Update timeline chart
function updateTimelineChart() {
    const ctx = document.getElementById('timeline-chart').getContext('2d');
    const period = document.getElementById('time-period').value;
    
    // Destroy existing chart
    if (timelineChart) {
        timelineChart.destroy();
    }
    
    const timeData = {};
    
    earthquakeData.forEach(eq => {
        const date = new Date(eq.datetime);
        if (isNaN(date)) return;
        
        let key;
        switch (period) {
            case 'yearly':
                key = date.getFullYear().toString();
                break;
            case 'monthly':
                key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
                break;
            case 'daily':
                key = date.toISOString().split('T')[0];
                break;
        }
        
        timeData[key] = (timeData[key] || 0) + 1;
    });
    
    const labels = Object.keys(timeData).sort();
    const data = labels.map(label => timeData[label]);
    
    timelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Earthquakes per ' + period.slice(0, -2),
                data: data,
                borderColor: 'rgba(34, 197, 94, 1)',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#ffffff' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    ticks: { 
                        color: '#ffffff',
                        maxTicksLimit: 10
                    },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Update depth vs magnitude scatter chart
function updateDepthMagnitudeChart() {
    const ctx = document.getElementById('depth-magnitude-chart').getContext('2d');
    
    // Destroy existing chart
    if (depthMagnitudeChart) {
        depthMagnitudeChart.destroy();
    }
    
    const scatterData = earthquakeData
        .filter(eq => eq.depth && eq.magnitude && !isNaN(parseFloat(eq.depth)) && !isNaN(parseFloat(eq.magnitude)))
        .map(eq => ({
            x: parseFloat(eq.magnitude),
            y: parseFloat(eq.depth)
        }));
    
    depthMagnitudeChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Depth vs Magnitude',
                data: scatterData,
                backgroundColor: 'rgba(251, 191, 36, 0.7)',
                borderColor: 'rgba(251, 191, 36, 1)',
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: '#ffffff' }
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Depth (km)',
                        color: '#ffffff'
                    },
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Magnitude',
                        color: '#ffffff'
                    },
                    ticks: { color: '#ffffff' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Update monthly distribution chart
function updateMonthlyChart() {
    const ctx = document.getElementById('monthly-chart').getContext('2d');
    
    // Destroy existing chart
    if (monthlyChart) {
        monthlyChart.destroy();
    }
    
    const monthData = new Array(12).fill(0);
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    earthquakeData.forEach(eq => {
        const date = new Date(eq.datetime);
        if (!isNaN(date)) {
            monthData[date.getMonth()]++;
        }
    });
    
    monthlyChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: monthNames,
            datasets: [{
                data: monthData,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                    '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF',
                    '#4BC0C0', '#FF6384', '#36A2EB', '#FFCE56'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#ffffff' }
                }
            }
        }
    });
}

// Update data table
function updateDataTable() {
    const tableBody = document.querySelector('#earthquakes-table tbody');
    const minMagnitude = parseFloat(document.getElementById('table-magnitude-filter').value);
    
    // Filter earthquakes by magnitude
    const filteredData = earthquakeData.filter(eq => {
        const magnitude = parseFloat(eq.magnitude);
        return !isNaN(magnitude) && magnitude >= minMagnitude;
    });
    
    // Sort by date (most recent first)
    filteredData.sort((a, b) => new Date(b.datetime) - new Date(a.datetime));
    
    // Take only the most recent 50 earthquakes for performance
    const recentData = filteredData.slice(0, 50);
    
    tableBody.innerHTML = '';
    
    recentData.forEach(earthquake => {
        const row = tableBody.insertRow();
        
        const date = new Date(earthquake.datetime);
        const dateStr = !isNaN(date) ? date.toLocaleString() : 'Invalid Date';
        
        row.innerHTML = `
            <td>${dateStr}</td>
            <td>${earthquake.place || 'Unknown'}</td>
            <td class="magnitude-cell">${earthquake.magnitude || 'N/A'}</td>
            <td>${earthquake.depth || 'N/A'}</td>
            <td>${parseFloat(earthquake.latitude).toFixed(3)}, ${parseFloat(earthquake.longitude).toFixed(3)}</td>
        `;
    });
    
    // Update count display
    const countElement = document.getElementById('table-earthquake-count');
    if (minMagnitude > 0) {
        countElement.textContent = `Showing ${recentData.length} recent earthquakes (magnitude ≥ ${minMagnitude})`;
    } else {
        countElement.textContent = `Showing ${recentData.length} most recent earthquakes`;
    }
}

// Auto-refresh data every 6 hours (matching GitHub Actions schedule)
setInterval(() => {
    console.log('Auto-refreshing earthquake data...');
    loadEarthquakeData();
    checkGitHubUpdate();
}, 6 * 60 * 60 * 1000); // 6 hours in milliseconds