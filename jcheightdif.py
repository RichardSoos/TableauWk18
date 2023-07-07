import pandas as pd

# Read the CSV file
data = pd.read_csv('JCCLEANED_data.csv')

# Calculate the height difference
data['height_difference'] = data['end_height'] - data['start_height']

# Save the updated data to a new CSV file
data.to_csv('JCCLEANED_heightdata.csv', index=False)
