// Chart configuration
export const CHART_CONFIG = {
    type: 'bar',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    title: (context) => context[0].label,
                    label: (context) => `Word Count: ${context.raw.toLocaleString()}`
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
                grid: { color: 'rgba(0, 0, 0, 0.05)' }
            },
            x: { 
                display: false,
                grid: { display: false }
            }
        }
    }
};

// Data file paths
export const DATA_PATHS = {
    EXCEL_FILE: 'data/output_agency_words.xlsx'
};

// DOM element IDs
export const ELEMENTS = {
    CHART: 'aggregatedChart',
    SEARCH: 'searchInput',
    SORT_NAME: 'sortName',
    SORT_COUNT: 'sortCount',
    TILE_GRID: 'tileGrid',
    LOADING: 'loading-indicator',
    ERROR_TEMPLATE: 'error-template'
};

// CSS classes
export const CLASSES = {
    ACTIVE: 'active',
    HIDDEN: 'hidden',
    TILE: 'tile',
    ERROR: 'error-message'
};

// Sort types
export const SORT_TYPES = {
    NAME: 'name',
    COUNT: 'count'
};

// Chart styles
export const CHART_STYLES = {
    backgroundColor: 'rgba(52, 152, 219, 0.7)',
    borderColor: 'rgba(52, 152, 219, 1)',
    borderWidth: 1,
    borderRadius: 8,
    barThickness: 'flex'
}; 