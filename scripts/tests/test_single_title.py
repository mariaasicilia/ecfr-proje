import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Configuration
BASE_URL = "https://www.ecfr.gov"
TEST_TITLE = "1"  # Title 1 - General Provisions
TEST_YEAR = "2023"
OUTPUT_DIR = "test_output"

def download_single_title():
    """Download XML for a single title."""
    print(f"\n[INFO] Downloading Title {TEST_TITLE} for year {TEST_YEAR}")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Construct the URL and download
    date_str = f"{TEST_YEAR}-01-01"
    url = f"{BASE_URL}/api/versioner/v1/full/{date_str}/title-{TEST_TITLE}.xml"
    print(f"[DEBUG] Requesting XML from: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the XML file
        filename = f"title-{TEST_TITLE}-{date_str}.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[INFO] Successfully saved XML to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"[ERROR] Failed to download XML: {e}")
        return None

def process_single_xml(file_path):
    """Process a single XML file and extract word counts."""
    print(f"\n[INFO] Processing XML file: {file_path}")
    
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
    # Download the XML
    xml_filepath = download_single_title()
    if not xml_filepath:
        print("[ERROR] Failed to download XML file")
        return

    # Process the XML
    data = process_single_xml(xml_filepath)
    if not data:
        print("[ERROR] Failed to process XML file")
        return

    # Create DataFrame and save intermediate results
    df = pd.DataFrame(data, columns=["Title", "Chapter", "Agency", "WordCount"])
    intermediate_file = os.path.join(OUTPUT_DIR, "output_chapter.xlsx")
    df.to_excel(intermediate_file, index=False)
    print(f"[INFO] Saved intermediate results to {intermediate_file}")

    # Combine rows and process agency word counts
    df = combine_rows(df)
    
    # Remove rows with 0 in WordCount
    agency_wordcounts = df[df['WordCount'] != 0]

    # Calculate total WordCount for each agency
    agency_wordcounts = agency_wordcounts.groupby('Agency')['WordCount'].sum().reset_index()

    # Save final results
    final_file = os.path.join(OUTPUT_DIR, "output_agency_words.xlsx")
    agency_wordcounts.to_excel(final_file, index=False)
    print(f"[INFO] Saved final results to {final_file}")

    # Print summary
    print("\n[SUMMARY]")
    print(f"Total number of agencies found: {len(agency_wordcounts)}")
    print(f"Total word count: {agency_wordcounts['WordCount'].sum():,}")
    print("\nTop 5 agencies by word count:")
    print(agency_wordcounts.nlargest(5, 'WordCount').to_string(index=False))

if __name__ == "__main__":
    main() 