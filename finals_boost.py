import csv
import os
import numpy as np

#this code is not a perfect solution for finding the expected judge score from a competition type
#but I have just modified my DD Dictionary.py file in order to accomplish a different task. 


# DIRECTORY TO FOLDER CONTAINING CLEANED .csv Dive score files
input_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Finals'
#input_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Semifinals'
#input_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Prelims'

#output dict
dd_scores_dict = {}

# scores from csv file to dir 
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
total_judge_scores = []
def compute_overall_judge_score(scores_dd_dict):
    
    for dd, scores in scores_dd_dict.items():
        if dd != 'NO_DD':
            for score in scores:
                if score != 'NO_DIVE' and score > 0:
                    judge_score = (score / dd) / 3
                    if judge_score >= 8:
                        total_judge_scores.append(judge_score)
    
    # compute the overall average if there are any judge scores
    if total_judge_scores:
        overall_judge_score = np.mean(total_judge_scores)
    else:
        overall_judge_score = None
    
    return overall_judge_score

# calculate expected judge score
overall_judge_score = compute_overall_judge_score(dd_scores_dict)


print(f'Overall Expected Judge Score: {overall_judge_score}')
print(str(len(total_judge_scores)))