# eCFR Dashboard

A web-based dashboard for visualizing word counts across different agencies in the [Electronic Code of Federal Regulations (eCFR)](https://www.ecfr.gov/).

## Project Structure

```
ecfr-project/
├── data/                           # Directory for XML and Excel files, XMLs from [govinfo.gov](https://www.govinfo.gov/bulkdata/ECFR)
│   ├── output_chapter.xlsx         # Intermediate results with chapter-level data
│   └── output_agency_words.xlsx    # Final results with agency-level word counts
├── test_output/                    # Directory for test results
├── index.html                      # Main dashboard webpage with Chart.js and XLSX integration
├── styles.css                      # Modern, responsive styling with gradient effects
├── script.js                       # Dashboard functionality including data loading and visualization
├── download_data.py                # Script to download historical XML data (2017-2023)
├── download_latest_data.py         # Script to download latest XML data for all titles
├── process_xml.py                  # Script to process XML files and generate Excel outputs
├── test_single_title.py            # Test script for downloading, processing Title when debugging downloading
└── server.py                       # Simple HTTP server to host the dashboard locally
```
The user guide was very helpful when trying to understand the data in eCFR, specifically in the difference between the DIV#s.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control and deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/ecfr-project.git
cd ecfr-project
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

Required packages:
- [requests](https://pypi.org/project/requests/)>=2.31.0
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)>=4.12.0
- [pandas](https://pypi.org/project/pandas/)>=2.0.0
- [openpyxl](https://pypi.org/project/openpyxl/)>=3.1.0
- [lxml](https://pypi.org/project/lxml/)>=4.9.0

## Usage

### Data Collection

There are three ways to collect data:

1. **Download Historical Data** (all years from 2017-2023):
```bash
python download_data.py
```
This will download XML files for all agencies and their chapters from 2017 to 2023.

2. **Download Latest Data** (current year only):
```bash
python download_latest_data.py
```
This will download XML files for all titles using the latest available date.

3. **Test with Single Title**:
```bash
python test_single_title.py
```
This will download and process Title 1 (General Provisions) as a test, saving results in the `test_output` directory.

### Data Processing

After downloading XML files, process them to generate Excel files:
```bash
python process_xml.py
```

This will generate two Excel files in the `data` directory:
- `output_chapter.xlsx`: Intermediate results with chapter-level data
- `output_agency_words.xlsx`: Final results with agency-level word counts

### Running the Dashboard

1. Start the local web server:
```bash
python server.py
```

2. Open a web browser and navigate to:
```
http://localhost:8000
```

The dashboard features:
- Interactive bar chart showing word counts by agency
- Searchable grid of agency tiles
- Sort options by agency name or word count
- Responsive design that works on different screen sizes

## Deployment

This project is deployed using GitHub Pages. To deploy your own version:

1. Fork this repository to your GitHub account
2. Go to your repository's Settings
3. Scroll down to "GitHub Pages" section
4. Under "Source", select "main" branch
5. Click "Save"

Your dashboard will be available at:
```
https://YOUR_USERNAME.github.io/ecfr-project
```

Note: The dashboard requires the Excel files to be in the `data` directory. You'll need to:
1. Run the data collection scripts
2. Process the XML files
3. Commit the generated Excel files to your repository

## File Descriptions

- `download_data.py`: Downloads historical XML data for all agencies and chapters
- `download_latest_data.py`: Downloads latest XML data for all titles
- `process_xml.py`: Processes XML files to extract word counts and generate Excel files
- `test_single_title.py`: Test script for downloading and processing a single title
- `server.py`: Simple HTTP server to host the dashboard locally
- `index.html`: Main dashboard webpage
- `styles.css`: Dashboard styling
- `script.js`: Dashboard functionality and data processing

## Notes

- The dashboard requires the Excel files to be in the `data` directory
- XML files are large and downloading all historical data may take some time
- The test script is useful for verifying the download and processing functionality
- The local server must be running to view the dashboard

## Troubleshooting

1. If you see CORS errors in the browser console:
   - Make sure the server is running
   - Check that the Excel files are in the correct location
   - Verify file permissions

2. If the dashboard shows no data:
   - Ensure the Excel files exist and have the correct format
   - Check the browser console for any errors
   - Verify the data processing completed successfully

3. If downloads fail:
   - Check your internet connection
   - Verify the eCFR API is accessible
   - Ensure you have sufficient disk space
