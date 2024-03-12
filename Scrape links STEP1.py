"""
This file takes in a divemeets url to the "all results" tab on the landing page for a competition
it will return a CSV file to the "filename" variable that contains the names of each diver, their
place, and their final score. 


Divemeets links the detailed score information on the number for final score, and that link is added
to the end of the diver information. 

After this process finishes, run the "Get scores from links" script on the file that was just created.
"""
import requests
from bs4 import BeautifulSoup
import csv

#MUST BE THE eventnum=all URL FOR THE MEET, CLICK "ALL RESULTS" on divemeets
results_all_url = 'https://secure.meetcontrol.com/divemeets/system/eventresultsext.php?meetnum=8961&eventnum=all'

#get request
response = requests.get(results_all_url)
soup = BeautifulSoup(response.text, 'html.parser')

divers_data = []

for row in soup.find_all('tr')[1:]:
    cells = row.find_all('td')
    if cells and len(cells) >= 5 and cells[3].find('a'):
        diver_data = {
            'diver_name': cells[0].get_text(strip=True),
            'team': cells[1].get_text(strip=True),
            'place': cells[2].get_text(strip=True),
            'score': cells[3].get_text(strip=True),
            'diff': cells[4].get_text(strip=True),
            'detailed_score_url': cells[3].find('a').get('href')  #href attribute 
        }
        divers_data.append(diver_data)


for diver in divers_data:
    print(diver)
filename = 'NCAA Championships/2023 Women.csv'



with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    # header row
    csvwriter.writerow(['Diver Name', 'Team', 'Place', 'Score', 'Diff', 'Detailed Score URL'])

    for diver in divers_data:
        row = [
            diver['diver_name'],
            diver['team'],
            diver['place'],
            diver['score'],
            diver['diff'],
            diver['detailed_score_url']
        ]
        csvwriter.writerow(row)

print(f"Data has been written to {filename}")