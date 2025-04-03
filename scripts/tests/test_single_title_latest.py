import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
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

def process_xml(file_path):
    """Process a single XML file and extract word counts."""
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "xml")

    # Extract title number from filename
    title_number = os.path.basename(file_path).split("-")[1].split(".")[0]

    # Extract agencies and word counts
    data = []
    for div3 in soup.find_all("DIV3"):
        agency_text = div3.find("HEAD").get_text().strip() if div3.find("HEAD") else "No HEAD"

        # Split agency_text on em dash (—)
        parts = agency_text.split('—')

        # Assign Chapter and Agency based on split results
        if len(parts) > 1:  # If em dash was found
            chapter = parts[0].strip()
            agency = '—'.join(parts[1:]).strip()  # Rejoin remaining parts for agency
        else:
            chapter = parts[0].strip()  # If no em dash, assume entire text is chapter
            agency = ''

        word_count = sum(len(p.get_text().split()) for p in div3.find_all("P"))
        data.append([title_number, chapter, agency, word_count])

    return data

def combine_rows(df):
    """Combine rows where one agency is contained within another."""
    # Group by 'Title' and 'Chapter'
    grouped = df.groupby(['Title', 'Chapter'])

    # Iterate through groups
    combined_data = []
    for name, group in grouped:
        # Find rows where 'Agency' is fully contained in another row
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if group.iloc[i]['Agency'] in group.iloc[j]['Agency'] and group.iloc[i]['Agency'] != group.iloc[j]['Agency']:
                    # Add WordCounts and update the longer row
                    group.loc[group.index[i], 'WordCount'] += group.loc[group.index[j], 'WordCount']
                    group.loc[group.index[j], 'WordCount'] = -1  # Mark for deletion

        # Remove rows marked for deletion
        combined_data.extend(group[group['WordCount'] != -1].values.tolist())

    # Create a new DataFrame from the combined data
    combined_df = pd.DataFrame(combined_data, columns=df.columns)
    return combined_df

def main():
    # Create test directory
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)
    print(f"[INFO] Created test directory: {test_dir}")
    
    # Get the latest available date
    latest_date = get_latest_date()
    print(f"[INFO] Using latest available date: {latest_date}")
    
    # Test with Title 1 (General Provisions)
    test_title = 1
    print(f"\n[INFO] Testing with Title {test_title}")
    
    # Create filename based on title
    filename = f"title-{test_title}-{latest_date}.xml"
    filepath = os.path.join(test_dir, filename)
    
    # Download the XML file
    try:
        xml_data = get_title_xml(latest_date, test_title)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_data)
        print(f"[INFO] Saved XML for {filename}")
    except Exception as e:
        print(f"[ERROR] Error saving {filename}: {e}")
        return
    
    # Process the XML file
    print("\n[INFO] Processing XML file...")
    data = process_xml(filepath)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["Title", "Chapter", "Agency", "WordCount"])
    
    # Save intermediate results
    intermediate_file = os.path.join(test_dir, 'output_chapter.xlsx')
    df.to_excel(intermediate_file, index=False)
    print(f"[INFO] Saved intermediate results to {intermediate_file}")
    
    # Combine rows and process agency word counts
    df = combine_rows(df)
    
    # Remove rows with 0 in WordCount
    agency_wordcounts = df[df['WordCount'] != 0]
    
    # Calculate total WordCount for each agency
    agency_wordcounts = agency_wordcounts.groupby('Agency')['WordCount'].sum().reset_index()
    
    # Save final results
    final_file = os.path.join(test_dir, 'output_agency_words.xlsx')
    agency_wordcounts.to_excel(final_file, index=False)
    print(f"[INFO] Saved final results to {final_file}")
    
    # Print summary
    print("\n[INFO] Summary:")
    print(f"Total agencies found: {len(agency_wordcounts)}")
    print(f"Total word count: {agency_wordcounts['WordCount'].sum():,}")
    print("\nTop 5 agencies by word count:")
    print(agency_wordcounts.nlargest(5, 'WordCount').to_string(index=False))

if __name__ == "__main__":
    main()