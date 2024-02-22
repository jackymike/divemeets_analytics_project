"""
Cleans the STEP 2 CSV file so that it can be used for statistics. 
"""
import csv
import os

# directory containing the CSV files to clean
input_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Dirty/Semifinals'

# output directory
output_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Semifinals'

#check if output dir exists
os.makedirs(output_dir, exist_ok=True)


def clean_and_adjust_csv_lines(lines):
    adjusted_data = []
    for line in lines:
        parts = [p.strip() for p in line.split(',') if p.strip()]
        # last elem is always total score no matter len
        total_score = parts[-1]
        dive_data = parts[:-1]

        if '/' in dive_data[0]:  # synchro event check
            if len(dive_data) == 11:  # womens/mixed synchro 
                # add placeholders for missing 6th round score and DD
                # between the round 5 DD and total score
                dive_data.insert(11, 'NO_DD')  # Adjust for 5 dives
                dive_data.insert(11, 'NO_DIVE')

        elif len(dive_data) == 11: # nonsyncro women's event check
            #adjust for 5 dives
            dive_data.insert(11, 'NO_DD')  # Adjust for 5 dives
            dive_data.insert(11, 'NO_DIVE')

        # reconstruct line
        adjusted_line = ','.join(dive_data[:1 + 6 * 2]) + ',' + total_score + '\n'
        adjusted_data.append(adjusted_line)

    return adjusted_data

#loop to iterate over 
for filename in os.listdir(input_dir):
    if filename.startswith('updated_') and filename.endswith('.csv'):
        file_path = os.path.join(input_dir, filename)
        
        with open(file_path, 'r', newline='') as infile:
            header = next(infile)  # skip the header
            lines = infile.readlines()

        adjusted_csv_lines = clean_and_adjust_csv_lines(lines)

        new_header = 'Diver Name'
        max_dives = 6  
        for i in range(1, max_dives + 1):
            new_header += f', Round {i} Score, Round {i} DD'
        new_header += ', Total Score\n'

        cleaned_file_path = os.path.join(output_dir, 'CLEANED_' + filename)

        with open(cleaned_file_path, 'w', newline='') as outfile:
            outfile.write(new_header) 
            for line in adjusted_csv_lines:
                outfile.write(line)

        print(f'Cleaned, saved to: {cleaned_file_path}')
