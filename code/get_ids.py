"""
Get all the match ids for a certain season
"""


import requests
from bs4 import BeautifulSoup
import os
import csv
from time import sleep

# The first season has id 02, and the last 69
for season in range(2, 70):
    sleep(1)
    year = season + 1954
    season_id = str(season) if season >= 10 else "0" + str(season)
    
    URL = "https://www.voetbalstats.nl/listjaarere.php?seizoenid=" + season_id
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    td_elements = soup.find_all("td", class_="linkere")

    wedstrijden = []
    for td in td_elements:
        a_tag = td.find("a", href=True)
        if a_tag and a_tag["href"].startswith("opstelere"):
            wedstrijden.append(a_tag["href"])

    wedstrijden = list(set(wedstrijden))
    print(len(wedstrijden))

    ids = [int(x.split("=", 1)[1]) for x in wedstrijden]

    # Get the project directory (one level up from the current script's folder)
    project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Define the raw data folder path in the project directory
    raw_data_folder = os.path.join(project_folder, "raw data", str(year))

    # Ensure the directory exists
    os.makedirs(raw_data_folder, exist_ok=True)

    # Define the file path
    file_path = os.path.join(raw_data_folder, f"wedstrijd_ids_{year}.csv")

    # Save the list to a CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the data
        for value in ids:
            writer.writerow([value])

    print(f"Data saved to {file_path}")
