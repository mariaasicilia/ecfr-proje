// Load data from Excel file
async function loadData() {
  try {
    console.log('Attempting to load Excel file...');
    
    // First, check if we can access the file
    const response = await fetch('data/output_agency_words.xlsx');
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    // Get the file as an ArrayBuffer
    const arrayBuffer = await response.arrayBuffer();
    console.log('File loaded as ArrayBuffer, size:', arrayBuffer.byteLength);
    
    // Read the Excel file
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    console.log('Workbook loaded, sheets:', workbook.SheetNames);
    
    // Get the first sheet
    const firstSheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[firstSheetName];
    console.log('First sheet name:', firstSheetName);
    
    // Convert to JSON without specifying header to get raw data
    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    console.log('Raw JSON data length:', jsonData.length);
    console.log('First few rows:', jsonData.slice(0, 3));
    
    // Skip header row and process data
    const processedData = jsonData.slice(1).map(row => {
      if (!row || row.length < 2) {
        console.log('Skipping invalid row:', row);
        return null;
      }
      return {
        agency: row[0] || '',
        wordCount: parseInt(row[1] || '0')
      };
    }).filter(item => item && item.agency); // Filter out null/empty entries

    console.log('Processed data length:', processedData.length);
    console.log('First few processed items:', processedData.slice(0, 3));
    
    if (processedData.length === 0) {
      console.warn('No valid data found in Excel file');
      throw new Error('No valid data found in Excel file');
    }

    return processedData;
  } catch (error) {
    console.error('Error loading data:', error);
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    });
    throw error; // Re-throw the error to handle it in the calling function
  }
}

// Function to format agency name for display
function formatAgencyName(name) {
  if (!name) return '';
  return name.split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

// Function to update chart and tiles based on search and sort
function updateDisplay(data, searchTerm = '', sortBy = 'name') {
  console.log('Updating display with data:', data);
  console.log('Search term:', searchTerm);
  console.log('Sort by:', sortBy);

  if (!data || data.length === 0) {
    console.error('No data to display');
    return;
  }

  // Filter data based on search term only if there is a search term
  let filteredData = searchTerm 
    ? data.filter(item => 
        item.agency.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : data;

  console.log('Filtered data:', filteredData);

  // Sort data
  filteredData.sort((a, b) => {
    if (sortBy === 'count') {
      return b.wordCount - a.wordCount;
    } else {
      return a.agency.localeCompare(b.agency);
    }
  });

  console.log('Sorted data:', filteredData);

  // Update chart
  updateChart(filteredData);

  // Update tiles
  updateTiles(filteredData);
}

// Function to update the chart
function updateChart(data) {
  console.log('Updating chart with data:', data);
  const ctx = document.getElementById('aggregatedChart').getContext('2d');
  
  // Destroy existing chart if it exists
  if (window.aggregatedChart instanceof Chart) {
    window.aggregatedChart.destroy();
  }

  // Create new chart
  window.aggregatedChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map(item => formatAgencyName(item.agency)),
      datasets: [{
        label: 'Word Count',
        data: data.map(item => item.wordCount),
        backgroundColor: 'rgba(52, 152, 219, 0.7)',
        borderColor: 'rgba(52, 152, 219, 1)',
        borderWidth: 1,
        borderRadius: 8,
        barThickness: 'flex'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              return `Word Count: ${context.raw.toLocaleString()}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: { 
            display: true, 
            text: "Word Count",
            font: {
              family: 'Roboto',
              size: 14,
              weight: '500'
            }
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          }
        },
        x: { 
          display: false,
          grid: {
            display: false
          }
        }
      }
    }
  });
}

// Function to update the tiles
function updateTiles(data) {
  console.log('Updating tiles with data:', data);
  const tilesContainer = document.querySelector('.tiles-container');
  if (!tilesContainer) {
    console.error('Tiles container not found');
    return;
  }

  tilesContainer.innerHTML = '';

  data.forEach(item => {
    const tile = document.createElement('div');
    tile.className = 'tile';
    tile.innerHTML = `
      <h3>${formatAgencyName(item.agency)}</h3>
      <p>Word Count: ${item.wordCount.toLocaleString()}</p>
    `;
    tilesContainer.appendChild(tile);
  });
}

// Initialize the dashboard
async function initializeDashboard() {
  try {
    console.log('Initializing dashboard...');
    const data = await loadData();
    console.log('Data loaded:', data);

    if (!data || data.length === 0) {
      console.error('No data loaded');
      return;
    }

    let currentSort = 'name';
    let currentSearch = '';

    // Add event listeners
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        currentSearch = e.target.value;
        updateDisplay(data, currentSearch, currentSort);
      });
    }

    const sortCountBtn = document.getElementById('sortCount');
    if (sortCountBtn) {
      sortCountBtn.addEventListener('click', () => {
        currentSort = 'count';
        setActiveButton('sortCount');
        updateDisplay(data, currentSearch, currentSort);
      });
    }

    const sortNameBtn = document.getElementById('sortName');
    if (sortNameBtn) {
      sortNameBtn.addEventListener('click', () => {
        currentSort = 'name';
        setActiveButton('sortName');
        updateDisplay(data, currentSearch, currentSort);
      });
    }

    // Initial display with all data
    updateDisplay(data, currentSearch, currentSort);
  } catch (error) {
    console.error('Error initializing dashboard:', error);
  }
}

// Helper to update active state on sort buttons
function setActiveButton(activeId) {
  document.getElementById('sortCount').classList.remove('active');
  document.getElementById('sortName').classList.remove('active');
  document.getElementById(activeId).classList.add('active');
}

// Start the dashboard when the page loads
document.addEventListener('DOMContentLoaded', initializeDashboard); 