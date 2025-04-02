import os
import pandas as pd
from bs4 import BeautifulSoup

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
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Process all XML files in the data directory
    xml_dir = "data"
    all_data = []
    for filename in os.listdir(xml_dir):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_dir, filename)
            print(f"Processing {filename}...")
            all_data.extend(process_xml(file_path))

    # Create initial DataFrame
    df = pd.DataFrame(all_data, columns=["Title", "Chapter", "Agency", "WordCount"])

    # Save intermediate results
    df.to_excel('data/output_chapter.xlsx', index=False)
    print("Saved intermediate results to output_chapter.xlsx")

    # Combine rows and process agency word counts
    df = combine_rows(df)
    
    # Remove rows with 0 in WordCount
    agency_wordcounts = df[df['WordCount'] != 0]

    # Calculate total WordCount for each agency
    agency_wordcounts = agency_wordcounts.groupby('Agency')['WordCount'].sum().reset_index()

    # Save final results
    agency_wordcounts.to_excel('data/output_agency_words.xlsx', index=False)
    print("Saved final results to output_agency_words.xlsx")

if __name__ == "__main__":
    main() 