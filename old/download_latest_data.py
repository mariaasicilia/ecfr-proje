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

def get_agencies():
    """Retrieve the agencies JSON from the Admin Service."""
    url = f"{BASE_URL}/api/admin/v1/agencies.json"
    print(f"[DEBUG] Requesting agencies data from: {url}")
    response = requests.get(url)
    print(f"[DEBUG] Agencies request status code: {response.status_code}")
    response.raise_for_status()
    data = response.json()
    print("[DEBUG] Agencies retrieved successfully.")
    return data.get("agencies", [])

def flatten_agencies(agencies):
    """Flatten the agency hierarchy (include children)."""
    flat = []
    for agency in agencies:
        flat.append(agency)
        if agency.get("children"):
            flat.extend(flatten_agencies(agency["children"]))
    return flat

def get_title_xml(date, title, extra_params=None):
    """
    Download the full XML for a given title as of a particular date.
    Optionally include additional query parameters (e.g., chapter).
    """
    url = f"{BASE_URL}/api/versioner/v1/full/{date}/title-{title}.xml"
    params = extra_params if extra_params is not None else {}
    print(f"[DEBUG] Requesting XML from: {url} with params: {params}")
    response = requests.get(url, params=params)
    print(f"[DEBUG] XML request status code: {response.status_code}")
    response.raise_for_status()
    return response.text

def process_agency(agency, date):
    """
    Process one agency: for each CFR reference,
    download the XML and save it to a file.
    """
    slug = agency.get("slug")
    print(f"\n[INFO] Processing agency: {slug}")
    cfr_refs = agency.get("cfr_references", [])
    
    for ref in cfr_refs:
        title = ref.get("title")
        chapter = ref.get("chapter")
        
        extra_params = {}
        if chapter:
            extra_params["chapter"] = chapter
        
        # Create filename based on title and chapter
        filename = f"title-{title}"
        if chapter:
            filename += f"-chapter-{chapter}"
        filename += f"-{date}.xml"
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"[INFO] File already exists: {filename}")
            continue
            
        try:
            xml_data = get_title_xml(date, title, extra_params)
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
    
    # Get all agencies
    agencies = get_agencies()
    agencies_flat = flatten_agencies(agencies)
    
    # Use ThreadPoolExecutor to process each agency in its own thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_agency = {
            executor.submit(process_agency, agency, latest_date): agency 
            for agency in agencies_flat
        }
        
        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_agency):
            agency = future_to_agency[future]
            try:
                future.result()
            except Exception as e:
                print(f"[ERROR] Exception processing agency {agency.get('slug')}: {e}")

if __name__ == "__main__":
    main()