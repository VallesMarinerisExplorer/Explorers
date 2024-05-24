# https://github.com/DeepHorizons/Python-NRLMSISE-00/tree/master
# https://github.com/DeepHorizons/Python-Jacchia77
# This script gets the neutral f10.7 atmosphere data index from noaa, which can be used for other things like
# drag calculations, etc. Here is a link to some further reading:
# https://www.swpc.noaa.gov/phenomena/f107-cm-radio-emissions

import csv
import requests

url = "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json"

# Download JSON data
response = requests.get(url)
data = response.json()

csv_file_path = "solar_data.csv"

# Writing to CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write data
    writer.writerows(data)

print(f"CSV file has been created at: {csv_file_path}")
