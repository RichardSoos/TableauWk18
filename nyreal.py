import pandas as pd

# Read the CSV file
data = pd.read_csv('NYCLEANED_heightdata.csv ')

# Convert the 'started_at' and 'ended_at' columns to datetime
data['started_at'] = pd.to_datetime(data['started_at'])
data['ended_at'] = pd.to_datetime(data['ended_at'])

# Calculate the time difference
time_difference = data['ended_at'] - data['started_at']

# Create a new column 'RealJourney' with 'Y' if time difference is at least 2 minutes, 'N' otherwise
data['RealJourney'] = time_difference >= pd.Timedelta(minutes=2)
data['RealJourney'] = data['RealJourney'].map({True: 'Y', False: 'N'})

# Save all rows to a single CSV file
data.to_csv('NYReal_cleaned.csv', index=False)



