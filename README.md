# eCFR Dashboard

> **Recent Update**: The latest update includes no changes to the actual website, however I did a 20-min organizational cleanup to improve maintainability and understandability. Key changes include:
> - Modularized the codebase into components for better separation of concerns
> - Improved error handling and loading states
> - Enhanced performance through code optimization and modern web practices
> - Added proper documentation and code organization
> - Implemented accessibility improvements
> These changes make the codebase more maintainable, easier to understand, and follow modern web development standards.

> An additional 30 min was spent correspondingly updating this README documentation. The original push is in the old-organization fork.
> I describe some of the debugging issues I encountered below, as well as how to run processes further below. 

> Note that while in the process, I left my original download_latest_data.py running overnight, saving data in XML and JSON. I originally had it calculating word counts at the same time, which also definitely slowed it down. It ended up finishing running by the morning, having printed out word counts for agencies per year, but didn't save any actual files. I went back to fix the script so that it works, but to be able to have data to build off of for the front end and not waste time, I got data from [govinfo.com/bulkdata/ECFR](https://www.govinfo.gov/bulkdata/ECFR).

> I think this was a logical approach to be speed-aware. Reflecting, I think the best approach for speed, especially when trying to understand past data + combine with live updates would be to:
> 1. take the historical data from the easiest point of access to get a base built out fast, then 
> 2. POST request the API on a 1x daily schedule to check changes to old regulation, then when updates are made that could change word content, request that Title and Chapter from the API to recalculate and update relevant word counts stored for the impacted agencies. 

A web-based dashboard for visualizing word counts across different agencies in the [Electronic Code of Federal Regulations (eCFR)](https://www.ecfr.gov/).

## Project Structure

```
ecfr-project/
├── src/                            # Frontend code
│   ├── components/                 # Modular components
│   │   ├── Chart.js                # Chart visualization component
│   │   ├── Grid.js                 # Grid display component
│   │   └── Search.js               # Search and sort functionality
│   ├── styles/                     # Stylesheet directory
│   │   └── main.css                # Main CSS with modern practices
│   ├── utils/                      # Utility functions and constants
│   │   ├── constants.js            # Configuration and constants
│   │   └── helpers.js              # Helper functions
│   ├── app.js                      # Main application logic
│   └── index.html                  # Entry point HTML
├── scripts/                        # Backend scripts
│   ├── data/                       # Data processing scripts
│   │   ├── download_data.py        # Historical data downloader
│   │   ├── download_latest_data.py # Latest data downloader
│   │   └── process_xml.py          # XML processor
│   ├── tests/                      # Test scripts
│   │   └── test_single_title.py    # Single title test
│   └── server/                     # Server scripts
│       └── server.py               # Local development server
├── data/                           # Data storage
│   ├── output_chapter.xlsx         # Chapter-level data
│   └── output_agency_words.xlsx    # Agency-level word counts
└── test_output/                    # Test results directory
```
The eCFR user guide was very helpful when trying to understand the data in eCFR, specifically in the difference between the DIV#s.

## Prerequisites

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mariaasicilia/ecfr-project.git
cd ecfr-project
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

1. Start the local development server:
```bash
python scripts/server/server.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

The server will automatically serve files from the `src` directory.

## How It Works

### Data Flow
1. XML data is downloaded from eCFR using `download_data.py` or `download_latest_data.py`
2. Data is processed into Excel files using `process_xml.py`
   - `output_chapter.xlsx`: Intermediate results w/chapter-level data (you could get rid of this and not save it)
   - `output_agency_words.xlsx`: Final results w/agency-level word counts
3. The web dashboard reads the saved XLSX files and displays visualizations

### Components
- **Chart Component**: Visualizes agency word counts using Chart.js
- **Grid Component**: Displays detailed agency information in a responsive grid
- **Search Component**: Handles search and sort functionality

### Features
- Interactive bar chart showing word counts by agency
- Searchable and sortable grid of agency tiles
- Responsive design for screen sizes
- Loading states and error handling

## Development

### Local Development
1. Make changes to files in the `src` directory
2. The server will serve the latest files automatically
3. Refresh your browser to see changes

### Code Organization
- Components are modular and follow single-responsibility principle
- Styles use CSS variables for consistent theming
- JavaScript uses ES6 modules for better organization
- Utility functions are now separated for reusability

### Best Practices
- Semantic HTML for better accessibility
- Responsive design w/modern CSS
- Performance optimizations (debouncing, lazy loading)
- Error boundaries and proper error handling for local server .py file
- Cleaner code w/consistent formatting

## Data Collection

### Historical Data
Download all data from 2017-2023:
```bash
python scripts/data/download_data.py
```
This uses the eCFR API, however, you could also get more clearly distinguished annual data from the [CFR Annual Edition](https://www.govinfo.gov/app/collection/cfr/) website. This just depends on your purpose; the eCFR can be updated on any given day, while the CFR is updated on a periodic schedule (titles 1-16 revised Jan. 1; titles 17-27 revised April 1; titles 28-41 revised July 1; titles 42-50 revised Oct. 1). 

### Latest Data
Latest data can be scraped from [govinfo.com/bulkdata/ECFR](https://www.govinfo.gov/bulkdata/ECFR), per the US GPO's [user guide](https://github.com/usgpo/bulk-data/blob/main/ECFR-XML-User-Guide.md). Download current year's data:
```bash
python scripts/data/download_latest_data.py
```

### Test Single Title
Test with Title 1 (General Provisions):
```bash
python scripts/tests/test_single_title.py
```

## Troubleshooting

### Common Issues

1. **API and Download Issues**
   - If downloads fail or timeout:
     - Check your internet connection
     - Verify the eCFR API is accessible (sometimes it has downtime, or they're updating files apparently)
     - Try using the [govinfo.com/bulkdata/ECFR](https://www.govinfo.gov/bulkdata/ECFR) as a backup
     - Ensure you have sufficient disk space for XML files
   - If download_latest_data.py runs slowly:
     - Consider running overnight for full dataset
     - Use test_single_title.py first to verify functionality
     - Try downloading from CFR Annual Edition for historical data

2. **Data Processing Issues**
   - If Excel files aren't generating:
     - Check Python dependencies are installed correctly
     - Verify XML files exist in data directory
     - Look for error messages in console output (added for this very reason myself)
   - If word counts seem incorrect:
     - Verify XML structure matches expected DIV# format
     - Check for encoding issues in source files
     - Run single calls to the API (i.e. test_single_title.py) to validate processing to not waste time on nonproductive/non-saved requests

3. **Server/Display Issues**
   - If server won't start:
     - Check if port 8000 is already in use
     - Try changing PORT in server.py
     - Verify you're in the correct directory
   - If dashboard shows no data:
     - Ensure Excel files are in the correct location
     - Check browser console for specific errors
     - Verify file permissions
   - If charts don't render:
     - Clear browser cache
     - Check if Chart.js loaded correctly
     - Look for JavaScript errors in page inspection console

4. **CORS and File Access**
   - If seeing CORS errors:
     - Always use http://localhost:8000
     - Don't open index.html directly
     - Check server.py is running
   - If files aren't accessible:
     - Verify src/ directory structure
     - Check file permissions
     - Ensure server.py has correct directory path

### Error Messages Guide

Common error messages and solutions:

```
Error: Cannot find module 'Chart.js'
Solution: Verify Chart.js is properly loaded in index.html

Error: CORS policy: No 'Access-Control-Allow-Origin' header
Solution: Access through localhost server, not direct file

Error: Port 8000 already in use
Solution: Change PORT in server.py or close competing process

Error: Excel file not found
Solution: Verify data files are in correct directory
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [eCFR](https://www.ecfr.gov/) for providing the data
- Chart.js for visualization
- Python community for excellent tools

## Contact

For questions or issues, please open an issue on GitHub.
