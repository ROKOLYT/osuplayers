import requests
from bs4 import BeautifulSoup
import datetime
import time
import json

def get_data(page):
    response = requests.get(f"https://osu.ppy.sh/rankings/osu/country?page={page}#scores")
    return response

def player_count():
    player_count = []
    
    for i in range(1, 6):
        time.sleep(0.5)
        data = get_data(i)
        soup = BeautifulSoup(data.text, "html.parser")
        table = soup.find("table", {"class": "ranking-page-table"})
        rows = table.find_all("tr", {"class": "ranking-page-table__row"})
        
        for row in rows:
            players = row.find("td", {"class": "ranking-page-table__column ranking-page-table__column--dimmed"}).text
            players = players.replace("\n", "")
            players = players.replace(",", "")
            players = int(players)
            player_count.append(players)
    
    return sum(player_count)

def save_data(data):
    with open("player_count.json", "a") as file:
        json.dump(data, file)
        file.write('\n')
    
if __name__ == "__main__":
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    players = player_count()
    data = {'time': formatted_time, 'player_count': players}
    save_data(data)