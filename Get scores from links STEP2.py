"""
Divemeets' organization is weird, so I needed to use two scripts in order to getrequest the data and have
it in an analyze-able fashion. 


Synchronized competitions, dive changes, and other weird quirks that are represented in divemeets make the 
CSV file that this program outputs very messy. After this program finishes, use the "Clean CSVs" script
on the files that you have made. 


Additionally, my web-scraping is not very efficient, so this program can take a while to run if 
you are running it on multiple files or one large meet. 
"""
import os
import csv
import requests
from bs4 import BeautifulSoup

def fetch_dive_details(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Checks for HTTP errors
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return [], "Error"
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return [], "Error"
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return [], "Error"
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        return [], "Error"

    soup = BeautifulSoup(response.text, 'html.parser')
    dives = soup.find_all('tr', bgcolor="dddddd")

    scores_dd = []
    for dive in dives:
        details = dive.find_all('td')
        if len(details) == 8 and "Carry Over from Previous Round" not in details[3].text:
            dive_score = details[6].text.strip()
            dive_dd = details[5].text.strip()
            scores_dd.append((dive_score, dive_dd))

    total_score = soup.find_all('tr')[-2].find_all('td')[-2].text.strip()
    
    return scores_dd, total_score

def process_csv(file_path, base_url):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row
        updated_rows = []
        interation_count = 0
        for row in reader:
            full_url = base_url + row[5]
            detailed_scores_dd, total_score = fetch_dive_details(full_url)
            
            flattened_scores_dd = [item for sublist in detailed_scores_dd for item in sublist]
            new_row = [row[0]] + flattened_scores_dd + [total_score]
            updated_rows.append(new_row)
            print(interation_count)
            interation_count+=1

    output_file_path = 'NCAA Championships/Dive Scores/Dirty/dirty_' + os.path.basename(file_path)  # Use os.path.basename to get the filename
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Diver Name'] + [f'Round {i+1} Score, Round {i+1} DD' for i in range(len(updated_rows[0])//2 - 1)] + ['Total Score']
        writer.writerow(header)
        writer.writerows(updated_rows)

# Base URL for the detailed scoring pages
base_url = 'https://secure.meetcontrol.com/divemeets/system/'

input_dir = 'NCAA Championships/scraped_links'
# Get a list of all files in the directory
file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]

print("This may take several minutes, do not Keyboard Interrupt, Hopefully DiveMeets doesn't crash! \n love <3 Jack")
for file_path in file_paths:
    process_csv(file_path, base_url)
