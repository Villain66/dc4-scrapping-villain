import csv
import requests
from bs4 import BeautifulSoup

URL = 'https://www.scrapethissite.com/pages/forms/?page_num={}'
nb_pages = 10
filtered_team_data_list = []

for page in range(1, nb_pages + 1):
    url = URL.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

for page in range(1, nb_pages + 1):
    url = URL.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if page == 1:
        headers = table.find_all("th")
        header_names = [header.text.strip() for header in headers]

    for row in table.find_all("tr"):
        cells = row.find_all("td")

        if len(cells) >= 9:
            data = [cell.text.strip() for cell in cells]
            team_data = dict(zip(header_names, data))
            goals_for = int(team_data.get("Goals For (GF)", 0))
            goals_against = int(team_data.get("Goals Against (GA)", 0))
            plus_minus = int(team_data.get("+ / -", 0))

            if plus_minus > 0 and goals_against < 300:
                filtered_team_data_list.append(team_data)
                
csv_file = "resultats.csv"

with open(csv_file, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header_names)
    writer.writeheader()
    writer.writerows(filtered_team_data_list)
