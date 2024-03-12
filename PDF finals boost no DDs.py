import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import norm

# DIRECTORIES TO FOLDERS CONTAINING CLEANED .csv Dive score files
input_dir_finals = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned and Truncated/Finals'
input_dir_semis = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned and Truncated/Semifinals'
input_dir_prelims = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned and Truncated/Prelims'

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
                    list.append((score/dd)/3)
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


# mean and standard deviation, generate points on x-axis, pdf value for each point
finals_mean, finals_std = np.mean(finals_scores_list), np.std(finals_scores_list)
finals_points = np.linspace(np.min(finals_scores_list), np.max(finals_scores_list), 100)
finals_pdf_values = norm.pdf(finals_points, finals_mean, finals_std)

semis_mean, semis_std = np.mean(semis_scores_list), np.std(semis_scores_list)
semis_points = np.linspace(np.min(semis_scores_list), np.max(semis_scores_list), 100)
semis_pdf_values = norm.pdf(semis_points, semis_mean, semis_std)

prelims_mean, prelims_std = np.mean(prelims_scores_list), np.std(prelims_scores_list)
prelims_points = np.linspace(np.min(prelims_scores_list), np.max(prelims_scores_list), 100)
prelims_pdf_values = norm.pdf(prelims_points, prelims_mean, prelims_std)



#plotting
plt.figure(figsize=(10, 6))  
plt.hist(finals_scores_list, bins=30, density=True, alpha=0.3, color='b', label='Finals Scores')
plt.hist(semis_scores_list, bins=30, density=True, alpha=0.3, color='g', label='Semifinals Scores')
plt.hist(prelims_scores_list, bins=30, density=True, alpha=0.3, color='r', label='Semifinals Scores')
plt.plot(finals_points, finals_pdf_values, label='Finals', color='blue')
plt.plot(semis_points, semis_pdf_values, label='Semifinals', color='green')
plt.plot(prelims_points, prelims_pdf_values, label='Preliminaries', color='red')

plt.scatter(finals_mean, norm.pdf(finals_mean, finals_mean, finals_std), color='blue', zorder=5)
plt.scatter(semis_mean, norm.pdf(semis_mean, semis_mean, semis_std), color='green', zorder=5)
plt.scatter(prelims_mean, norm.pdf(prelims_mean, prelims_mean, prelims_std), color='red', zorder=5)

plt.title('Judge Scores PDF for US Nationals - Finals vs. Semifinals vs. Preliminaries - Top 12 Performers Only')
plt.xlabel('Judge Scores')
plt.ylabel('Probability Density')
plt.legend() 

plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.5))
plt.grid(True)  


plt.show() 