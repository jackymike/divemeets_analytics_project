import csv
import os


def split_events(input_csv_path, output_dir):
    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get the base name of the meet without the .csv extension to use in naming the output files
    meet_name = os.path.basename(input_csv_path).replace('.csv', '')

    # Initialize variables
    event_number = 0
    current_event_rows = []

    with open(input_csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Capture the header row

        for row in reader:
            place = row[2]  # Assuming the "place" column is the third column (index 2)

            # Check if this row is the start of a new event
            if place == '1' and current_event_rows:
                # Write the previous event's rows to a new file
                output_csv_path = os.path.join(output_dir, f'{meet_name}_event_{event_number}.csv')
                with open(output_csv_path, 'w', newline='') as event_file:
                    writer = csv.writer(event_file)
                    writer.writerow(headers)  # Write the header
                    writer.writerows(current_event_rows)
                event_number += 1  # Increment the event number
                current_event_rows = []  # Start a new event
                
            # Add the current row to the event rows
            current_event_rows.append(row)

        # Write the last event to a CSV file if it exists
        if current_event_rows:
            output_csv_path = os.path.join(output_dir, f'{meet_name}_event_{event_number}.csv')
            with open(output_csv_path, 'w', newline='') as event_file:
                writer = csv.writer(event_file)
                writer.writerow(headers)
                writer.writerows(current_event_rows)

# Define the path to your input CSV file and the directory for output files
input_csv_paths = [
    'US Nationals and Olympic Trials/scraped_links/2022 USA Diving Winter Nationals.csv',
    'US Nationals and Olympic Trials/scraped_links/2023 USA Diving Winter Nationals.csv'
]
output_dir = 'US Nationals and Olympic Trials/Events Split'

# Split the events into separate CSV files
for meet in input_csv_paths:
    split_events(meet, output_dir)