import { CHART_CONFIG, CHART_STYLES, ELEMENTS } from '../utils/constants.js';
import { formatAgencyName } from '../utils/helpers.js';

class ChartComponent {
    constructor() {
        this.chart = null;
        this.ctx = document.getElementById(ELEMENTS.CHART).getContext('2d');
    }

    // Initialize the chart
    initialize(data) {
        if (this.chart) {
            this.chart.destroy();
        }

        const chartData = {
            labels: data.map(item => formatAgencyName(item.agency)),
            datasets: [{
                label: 'Word Count',
                data: data.map(item => item.wordCount),
                ...CHART_STYLES
            }]
        };

        this.chart = new Chart(this.ctx, {
            ...CHART_CONFIG,
            data: chartData
        });
    }

    // Update chart with new data
    update(data) {
        if (!this.chart) {
            this.initialize(data);
            return;
        }

        this.chart.data.labels = data.map(item => formatAgencyName(item.agency));
        this.chart.data.datasets[0].data = data.map(item => item.wordCount);
        this.chart.update();
    }

    // Destroy chart instance
    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
    }
}

export default ChartComponent; 