import csv
import os

# Directory containing the CSV files
input_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned/Prelims'
output_dir = 'US Nationals and Olympic Trials/Events Split/Scores/Cleaned and Truncated/Prelims'

os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Function to truncate a CSV file to the first 13 rows
def truncate_csv(file_path, output_dir):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[:13]  # Read the first 13 rows, including the header

    # Write the truncated rows to a new file in the output directory
    output_file_path = os.path.join(output_dir, os.path.basename(file_path))
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Process each CSV file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_dir, filename)
        truncate_csv(file_path, output_dir)
        print(f'Truncated {filename} to the first 13 rows.')