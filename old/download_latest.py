import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures
from datetime import datetime

# Update this to the correct API base URL
BASE_URL = "https://www.ecfr.gov"

def get_latest_date():
    """Get the latest available date from the eCFR API."""
    url = f"{BASE_URL}/api/versioner/v1/versions.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Get the most recent date
    latest_date = data.get("versions", [])[0].get("date")
    return latest_date

def get_title_xml(date, title):
    """
    Download the full XML for a given title as of a particular date.
    """
    url = f"{BASE_URL}/api/versioner/v1/full/{date}/title-{title}.xml"
    print(f"[DEBUG] Requesting XML from: {url}")
    response = requests.get(url)
    print(f"[DEBUG] XML request status code: {response.status_code}")
    response.raise_for_status()
    return response.text

def process_title(title, date):
    """
    Process one title: download the XML and save it to a file.
    """
    print(f"\n[INFO] Processing title: {title}")
    
    # Create filename based on title
    filename = f"title-{title}-{date}.xml"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    
    # Skip if file already exists
    if os.path.exists(filepath):
        print(f"[INFO] File already exists: {filename}")
        return
    
    try:
        xml_data = get_title_xml(date, title)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_data)
        print(f"[INFO] Saved XML for {filename}")
    except Exception as e:
        print(f"[ERROR] Error saving {filename}: {e}")

def main():
    # Get the latest available date
    latest_date = get_latest_date()
    print(f"[INFO] Using latest available date: {latest_date}")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Define the range of titles (1 to 50, as per eCFR structure)
    titles = range(1, 51)
    
    # Use ThreadPoolExecutor to process each title in its own thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_title = {
            executor.submit(process_title, title, latest_date): title 
            for title in titles
        }
        
        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_title):
            title = future_to_title[future]
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] Exception processing title {title}: {e}")

if __name__ == "__main__":
    main() 