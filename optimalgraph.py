import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = 'DD_EV.csv'

column_names = ['Dive_DD', 'Standard_Dev', 'Expected_Value']
df_csv = pd.read_csv(csv_file_path, header=None, names=column_names)

# Display the first few rows to confirm correct loading
lower_bound = df_csv['Expected_Value'] - df_csv['Standard_Dev']
upper_bound = df_csv['Expected_Value'] + df_csv['Standard_Dev']

def is_dominated(row, dataframe):
    # A point is dominated if there is another point with both lower SD and higher EV
    return any((dataframe['Standard_Dev'] < row['Standard_Dev']) & 
               (dataframe['Expected_Value'] > row['Expected_Value']))

# Apply the function to each row in the dataframe
df_csv['Dominated'] = df_csv.apply(is_dominated, dataframe=df_csv, axis=1)

# Plot
plt.figure(figsize=(12, 8))

# Plot all points
plt.scatter(df_csv['Standard_Dev'], df_csv['Expected_Value'], color='blue', label='Dominated DD', zorder=2)

# Highlight non-dominated points
non_dominated = df_csv[~df_csv['Dominated']]
plt.scatter(non_dominated['Standard_Dev'], non_dominated['Expected_Value'], color='red', label='Optimal DD', zorder=3)

# Annotate each point with the Dive DD
for i, row in df_csv.iterrows():
    plt.text(row['Standard_Dev'], row['Expected_Value'], f"{row['Dive_DD']}", 
             color='black', fontsize=8, ha='right', va='bottom', zorder=4)

# Plot details
plt.title('Expected Value vs. Standard Deviation')
plt.xlabel('Standard Deviation (Lower is better)')
plt.ylabel('Expected Value (Higher is better)')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()