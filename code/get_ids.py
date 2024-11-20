"""
Get all the match data for a certain season
"""

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd

for season in range(2, 5):

    year = season + 1956 - 2

    if year == 2019:
        continue

    teams = 18
    if year >= 1962 and year <= 1965:
        teams = 16

    season_id = str(season) if season >= 10 else "0" + str(season)

    URL = "https://www.voetbalstats.nl/listjaarere.php?seizoenid=" + season_id
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    td_elements = soup.find_all("td", class_="linkere")

    thuis_teams = []
    uit_teams = []
    data = []
    uitslagen = []

    for i in range(len(td_elements)):
        a_tag = td_elements[i].find("a", href=True)

        if a_tag and a_tag["href"].startswith("listclubjaarere"):
            if i > teams * 2 and len(thuis_teams) < teams * (teams - 1) and i % 2 != 0:
                thuis_teams.append(a_tag.get_text().strip())
            if i > teams * 2 and len(uit_teams) < teams * (teams - 1) and i % 2 == 0:
                uit_teams.append(a_tag.get_text().strip())

        if a_tag and a_tag["href"].startswith("opstelere"):
            if len(uitslagen) < teams * (teams - 1) and i % 2 != 0:
                uitslagen.append(a_tag.get_text().strip())
            if len(data) < teams * (teams - 1) and i % 2 == 0:
                data.append(a_tag.get_text().strip())

    if uitslagen[0].count("-") == 2:
        uitslagen, data = data, uitslagen
        thuis_teams, uit_teams = uit_teams, thuis_teams

    if len(thuis_teams) != teams * (teams - 1) or len(uit_teams) != teams * (teams - 1) or len(data) != teams * (teams - 1) or len(uitslagen) != teams * (teams - 1):
        print(year)
        print("Something went wrong")

    rows = []

    for i in range(teams * (teams - 1)):
        thuis_doelpunten = int(uitslagen[i].split()[0])
        uit_doelpunten = int(uitslagen[i].split()[2])
        if thuis_doelpunten > uit_doelpunten:
            uitslag = "Gewonnen"
        elif thuis_doelpunten == uit_doelpunten:
            uitslag = "Gelijk"
        else:
            uitslag = "Verloren"

        rows.append([data[i], thuis_teams[i], uit_teams[i], thuis_doelpunten, uit_doelpunten, uitslag])


    df = pd.DataFrame(rows, columns=["Datum", "Thuis", "Uit", "Thuis Doelpunten", "Uit Doelpunten", "Uitslag"])

    # Define paths
    raw_dir = f"../raw data/{year}"
    processed_dir = f"../processed data/{year}"
    file_path_raw = f"{raw_dir}/uitslagen{year}.txt"
    file_path_processed = f"{processed_dir}/uitslagen{year}.csv"

    # Ensure directories exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    # Check and resolve conflicts for processed file
    if os.path.isfile(file_path_processed):
        os.remove(file_path_processed)  # Remove the conflicting file
    elif os.path.isdir(file_path_processed):
        import shutil
        shutil.rmtree(file_path_processed)  # Remove the conflicting directory

    # Write raw file
    page_text = "Example page content"  # Replace with actual content
    with open(file_path_raw, "w", encoding="utf-8") as file:
        file.write(page_text)

    # Write processed CSV file
    df.to_csv(file_path_processed, index=False)

    print(year, "Succes")

