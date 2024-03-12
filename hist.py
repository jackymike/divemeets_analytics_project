import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import beta

# DIRECTORIES TO FOLDERS CONTAINING CLEANED .csv Dive score files
input_dir_finals = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Finals'
input_dir_semis = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Semifinals'
input_dir_prelims = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Prelims'

#output lists
finals_scores_list = []
semis_scores_list = []
prelims_scores_list = []

# scores from csv file to dir 
def add_scores_to_list(file_path, list):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # header row skip
        
        for row in reader:
            for i in range(1, len(row) - 1, 2):  # iterate by pairs (score, DD)
                score = row[i]
                dd = row[i + 1]
                if score == 'NO_DIVE':  # empty placeholders in data
                    continue
                try:
                    score = float(score)
                    dd = float(dd)
                    list.append(((score/dd)/3)/10)
                except ValueError:
                    continue

#loop for each file in dir, adds scores from the file into the list
for filename in os.listdir(input_dir_finals):
    if filename.endswith('.csv'):  
        file_path = os.path.join(input_dir_finals, filename)
        add_scores_to_list(file_path, finals_scores_list)

for filename in os.listdir(input_dir_semis):
    if filename.endswith('.csv'):  
        file_path = os.path.join(input_dir_semis, filename)
        add_scores_to_list(file_path, semis_scores_list)

for filename in os.listdir(input_dir_prelims):
    if filename.endswith('.csv'):  
        file_path = os.path.join(input_dir_prelims, filename)
        add_scores_to_list(file_path, prelims_scores_list)

# Apply a small correction to ensure data falls strictly within the (0, 1) interval
epsilon = 1e-6
finals_scores_list = [max(min(score, 1-epsilon), epsilon) for score in finals_scores_list]

# Now, try fitting the beta distribution again
a, b, loc, scale = beta.fit(finals_scores_list, floc=0, fscale=1)

# Continue with the visualization as before
x = np.linspace(0, 1, 1000)
y = beta.pdf(x, a, b, loc, scale)

plt.hist(finals_scores_list, bins=30, density=True, alpha=0.5, color='g', label='Actual Scores')
plt.plot(x, y, 'r-', lw=2, label='Beta Fit')
plt.title('Fit of Beta Distribution to Finals Scores')
plt.xlabel('Score')
plt.ylabel('Density')
plt.legend()
plt.show()
