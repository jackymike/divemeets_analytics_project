import csv
import os
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import norm


# DIRECTORY TO FOLDER CONTAINING CLEANED .csv Dive score files
input_dir = 'US Nationals and Olympic Trials/CLEANED Dive scores'

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
                    dd = float(dd)
                    score = float(score)
                    if 3.0 <= dd <= 3.9 and dd != 4.0:
                        scores_dict.setdefault(dd, []).append(score)
                except ValueError:
                    continue

#loop for each file in dir
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):  

        file_path = os.path.join(input_dir, filename)
        add_scores_to_dict(file_path, dd_scores_dict)

# plotting PDF for each DD
plt.figure(figsize=(10, 6)) 
colors = plt.colormaps.get_cmap('viridis').resampled(len(dd_scores_dict.items())).colors
color = colors[0]
i = 0
for dd, scores in sorted(dd_scores_dict.items()):
    # mean and standard deviation for scores
    mean = np.mean(scores)
    std = np.std(scores, ddof=1)
    
    # generate points on x-axis between min and max scores
    x = np.linspace(mean - 3*std, mean + 3*std, 100) if std != 0 else np.linspace(mean - 1, mean + 1, 100)
    
    # pdf value for each point
    pdf = norm.pdf(x, mean, std) if std != 0 else np.full_like(x, 1)  # If std is 0, all pdf values are 1

    # plotting
    plt.scatter(mean, norm.pdf(mean, mean, std), zorder=5, color = color)
    plt.plot(x, pdf, label=f'DD {dd}', color = color)
    color = colors[i]
    i = (i + 1)%20
    

# plotting
plt.title('Probability Density Function of Dive Scores by Degree of Difficulty')
plt.xlabel('Dive Scores')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()