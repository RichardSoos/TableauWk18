import csv
import requests
import time

# Define the Google Elevation API endpoint
api_endpoint = "https://maps.googleapis.com/maps/api/elevation/json"
# api_endpoint = "https://maps.googleapis.com/maps/api/elevation"

# Define your Google Elevation API key
//api_key = excluded

# Specify the input CSV file path and output CSV file path
input_file = "C:/Users/soosr/Documents/AllHomework/TableauWK18Challenge/All_loc.csv"
output_file = "C:/Users/soosr/Documents/AllHomework/TableauWK18Challenge/All_height_loc.csv"

# Read the input CSV file
with open(input_file, "r") as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames + ["height"]
    rows = list(reader)

# Define batch size for API calls
batch_size = 200

# Open the output CSV file
with open(output_file, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each row and add the height data
    for i, row in enumerate(rows):
        start_lat = row["start_lat"]
        start_lng = row["start_lng"]

        # Make the API request to retrieve elevation data
        params = {
            "locations": f"{start_lat},{start_lng}",
            "key": api_key
        }
        retry = 0
        while retry < 3:
            try:
                response = requests.get(api_endpoint, params=params)
                response.raise_for_status()  # Check for any HTTP errors
                elevation_data = response.json()

                # Check if elevation data is available
                if "results" in elevation_data and elevation_data["results"]:
                    # Extract the elevation value from the API response
                    elevation = elevation_data["results"][0]["elevation"]
                else:
                    # Set elevation as None or any desired value when data is not available
                    elevation = None

                # Add the elevation data to the row
                row["height"] = elevation

                # Write the updated row to the output CSV file
                writer.writerow(row)

                # Write the batch of rows to the output CSV file
                if (i + 1) % batch_size == 0:
                    print(f"Processed {i + 1} rows.")
                    file.flush()  # Flush the buffer to ensure data is written to the file
                    time.sleep(5)  # Pause for 5 seconds before making the next API call

                break  # Exit the retry loop if API call is successful
            except requests.exceptions.RequestException as e:
                print(f"API request failed: {str(e)}")
                retry += 1
                print(f"Retrying ({retry}/3)...")
                time.sleep(5)  # Pause for 5 seconds before retrying

        if retry == 3:
            print(f"API request failed after 3 retries. Skipping row {i + 1}.")
