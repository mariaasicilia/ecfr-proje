import { DATA_PATHS, ELEMENTS } from './utils/constants.js';
import { showLoading, hideLoading, handleError } from './utils/helpers.js';
import ChartComponent from './components/Chart.js';
import GridComponent from './components/Grid.js';
import SearchComponent from './components/Search.js';

class App {
    constructor() {
        this.data = [];
        this.chart = new ChartComponent();
        this.grid = new GridComponent();
        this.search = new SearchComponent(this.handleDataUpdate.bind(this));
    }

    // Initialize the application
    async initialize() {
        try {
            showLoading(ELEMENTS.LOADING);
            await this.loadData();
            this.search.setData(this.data);
            hideLoading(ELEMENTS.LOADING);
        } catch (error) {
            handleError(error);
        }
    }

    // Load data from Excel file
    async loadData() {
        try {
            const response = await fetch(DATA_PATHS.EXCEL_FILE);
            const arrayBuffer = await response.arrayBuffer();
            const workbook = XLSX.read(arrayBuffer, { type: 'array' });
            
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            
            // Convert to JSON and process data
            const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
            
            this.data = jsonData.slice(1)
                .map(row => ({
                    agency: row[0] || '',
                    wordCount: parseInt(row[1] || '0')
                }))
                .filter(item => item.agency);

        } catch (error) {
            console.error('Error loading data:', error);
            throw new Error('Failed to load data from Excel file');
        }
    }

    // Handle data updates from search/sort
    handleDataUpdate(filteredData) {
        this.chart.update(filteredData);
        this.grid.update(filteredData);
        this.grid.animateTiles();
    }

    // Clean up resources
    destroy() {
        this.chart.destroy();
        this.grid.removeAnimations();
    }
}

// Start the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.initialize();

    // Clean up on page unload
    window.addEventListener('unload', () => {
        app.destroy();
    });
}); 