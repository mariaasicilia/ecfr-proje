import { ELEMENTS } from '../utils/constants.js';
import { createTile, getElement } from '../utils/helpers.js';

class GridComponent {
    constructor() {
        this.container = getElement(ELEMENTS.TILE_GRID);
        this.data = [];
    }

    // Initialize grid with data
    initialize(data) {
        this.data = data;
        this.render();
    }

    // Clear all tiles
    clear() {
        if (this.container) {
            this.container.innerHTML = '';
        }
    }

    // Render tiles based on current data
    render() {
        this.clear();

        if (!this.container) return;

        const fragment = document.createDocumentFragment();

        this.data.forEach(item => {
            const tile = createTile(item.agency, item.wordCount);
            fragment.appendChild(tile);
        });

        this.container.appendChild(fragment);
    }

    // Update grid with new data
    update(data) {
        this.data = data;
        this.render();
    }

    // Add animation classes to tiles
    animateTiles() {
        const tiles = this.container.querySelectorAll('.tile');
        tiles.forEach((tile, index) => {
            tile.style.animationDelay = `${index * 50}ms`;
            tile.classList.add('fade-in');
        });
    }

    // Remove animation classes
    removeAnimations() {
        const tiles = this.container.querySelectorAll('.tile');
        tiles.forEach(tile => {
            tile.classList.remove('fade-in');
        });
    }
}

export default GridComponent; 