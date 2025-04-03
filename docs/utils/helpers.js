// Format agency name for display
export function formatAgencyName(name) {
    if (!name) return '';
    return name.split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Debounce function for search input
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Sort data based on type
export function sortData(data, sortType) {
    return [...data].sort((a, b) => {
        if (sortType === 'count') {
            return b.wordCount - a.wordCount;
        }
        return a.agency.localeCompare(b.agency);
    });
}

// Filter data based on search term
export function filterData(data, searchTerm) {
    if (!searchTerm) return data;
    const term = searchTerm.toLowerCase();
    return data.filter(item => 
        item.agency.toLowerCase().includes(term)
    );
}

// Show loading state
export function showLoading(loadingId) {
    const loader = document.getElementById(loadingId);
    if (loader) {
        loader.classList.remove('hidden');
    }
}

// Hide loading state
export function hideLoading(loadingId) {
    const loader = document.getElementById(loadingId);
    if (loader) {
        loader.classList.add('hidden');
    }
}

// Show error message
export function showError(message, templateId) {
    const template = document.getElementById(templateId);
    if (!template) return;

    const clone = template.content.cloneNode(true);
    const errorElement = clone.querySelector('.error-message p');
    if (errorElement) {
        errorElement.textContent = message;
    }

    document.body.appendChild(clone);
}

// Remove error message
export function removeError() {
    const error = document.querySelector('.error-message');
    if (error) {
        error.remove();
    }
}

// Format number with commas
export function formatNumber(num) {
    return num.toLocaleString();
}

// Safely get element by ID with error handling
export function getElement(id) {
    const element = document.getElementById(id);
    if (!element) {
        console.error(`Element with id "${id}" not found`);
    }
    return element;
}

// Create a tile element
export function createTile(agency, wordCount) {
    const tile = document.createElement('div');
    tile.className = 'tile';
    tile.innerHTML = `
        <h3>${formatAgencyName(agency)}</h3>
        <p>Word Count: ${formatNumber(wordCount)}</p>
    `;
    return tile;
}

// Handle API errors
export function handleError(error) {
    console.error('Error:', error);
    showError('An error occurred while loading the data. Please try again later.', 'error-template');
    hideLoading('loading-indicator');
} 