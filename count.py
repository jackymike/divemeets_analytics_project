import csv
import os
import numpy as np

# DIRECTORY TO FOLDER CONTAINING CLEANED .csv Dive score files
input_dir = 'US Nationals and Olympic Trials/CLEANED Dive scores'

#output dict
dd_scores_dict = {}

# scores from csv file to dict, keys are the DDs of the dive scores.
def add_scores_to_dict(file_path, scores_dict):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # header row skip
        
        for row in reader:
            for i in range(1, len(row) - 1, 2):  # iterate by pairs (score, DD)
                score = row[i]
                dd = row[i + 1]
                if not score or not dd:  # empty placeholders in data
                    continue
                
                try:
                    score = float(score)
                    dd = float(dd)
                    scores_dict.setdefault(dd, []).append(score)
                except ValueError:
                    continue

#loop for each file in dir
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):  

        file_path = os.path.join(input_dir, filename)
        add_scores_to_dict(file_path, dd_scores_dict)



def expected_value_for_dd(scores_dict, desired_dd):
    if desired_dd in scores_dict and scores_dict[desired_dd]:
        scores = scores_dict[desired_dd]
        frequency_dict = {}
        for score in scores:
            if score in frequency_dict:
                frequency_dict[score] += 1
            else:
                frequency_dict[score] = 1
        
        weighted_sum = 0
        for score in frequency_dict:
            weighted_sum += score * (frequency_dict[score])
    return weighted_sum/len(scores_dict[desired_dd])

for i in range(26):
    display_dd = round(1.6 + (i/10), 1)  
    #print(dd_scores_dict[display_dd]) 
    if (display_dd not in dd_scores_dict):
        print("No dives done with DD of " + str(display_dd))
    else:
       print("PRINTING MEET HISTORY FOR DIVES WITH " + str(display_dd) + " DEGREE OF DIFFICULTY")
       #print(str(len(dd_scores_dict[display_dd]))+ " dives have been done with DD " + str(display_dd))
       # print("Minimum value is " + str(min(dd_scores_dict[display_dd])))
       # print("Maximum value is " + str(max(dd_scores_dict[display_dd])))
       #print(str(expected_value_for_dd(dd_scores_dict, display_dd)))
       #print("Expected value for " + str(display_dd) + " is " + str(expected_value_for_dd(dd_scores_dict, display_dd)))