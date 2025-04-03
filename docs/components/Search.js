import { ELEMENTS, CLASSES, SORT_TYPES } from '../utils/constants.js';
import { debounce, getElement, filterData, sortData } from '../utils/helpers.js';

class SearchComponent {
    constructor(onDataUpdate) {
        this.searchInput = getElement(ELEMENTS.SEARCH);
        this.sortNameBtn = getElement(ELEMENTS.SORT_NAME);
        this.sortCountBtn = getElement(ELEMENTS.SORT_COUNT);
        this.currentSort = SORT_TYPES.NAME;
        this.onDataUpdate = onDataUpdate;
        this.data = [];

        this.initialize();
    }

    // Initialize search and sort functionality
    initialize() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', 
                debounce(() => this.handleSearch(), 300)
            );
        }

        if (this.sortNameBtn) {
            this.sortNameBtn.addEventListener('click', () => {
                this.handleSort(SORT_TYPES.NAME);
            });
        }

        if (this.sortCountBtn) {
            this.sortCountBtn.addEventListener('click', () => {
                this.handleSort(SORT_TYPES.COUNT);
            });
        }
    }

    // Set initial data
    setData(data) {
        this.data = data;
        this.processData();
    }

    // Handle search input
    handleSearch() {
        this.processData();
    }

    // Handle sort button clicks
    handleSort(sortType) {
        this.currentSort = sortType;
        this.updateSortButtons();
        this.processData();
    }

    // Update sort button states
    updateSortButtons() {
        if (this.sortNameBtn && this.sortCountBtn) {
            this.sortNameBtn.classList.toggle(CLASSES.ACTIVE, this.currentSort === SORT_TYPES.NAME);
            this.sortCountBtn.classList.toggle(CLASSES.ACTIVE, this.currentSort === SORT_TYPES.COUNT);
            
            this.sortNameBtn.setAttribute('aria-pressed', this.currentSort === SORT_TYPES.NAME);
            this.sortCountBtn.setAttribute('aria-pressed', this.currentSort === SORT_TYPES.COUNT);
        }
    }

    // Process data with current search and sort settings
    processData() {
        if (!this.data.length) return;

        let processedData = [...this.data];

        // Apply search filter
        if (this.searchInput && this.searchInput.value) {
            processedData = filterData(processedData, this.searchInput.value);
        }

        // Apply sorting
        processedData = sortData(processedData, this.currentSort);

        // Update the view
        if (this.onDataUpdate) {
            this.onDataUpdate(processedData);
        }
    }

    // Reset search and sort
    reset() {
        if (this.searchInput) {
            this.searchInput.value = '';
        }
        this.currentSort = SORT_TYPES.NAME;
        this.updateSortButtons();
    }
}

export default SearchComponent; 