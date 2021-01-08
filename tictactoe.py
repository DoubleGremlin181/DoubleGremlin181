import requests
from bs4 import BeautifulSoup
import json
import os
import random


LINKS = {"Tile 0": "https://cntr.click/5xW31GG",
         "Tile 1": "https://cntr.click/k6m4pLh",
         "Tile 2": "https://cntr.click/0Jy1NdB",
         "Tile 3": "https://cntr.click/y4BYk8p",
         "Tile 4": "https://cntr.click/VCtRg6b",
         "Tile 5": "https://cntr.click/b0a0hMb",
         "Tile 6": "https://cntr.click/sGaY2s4",
         "Tile 7": "https://cntr.click/5B5pmVK",
         "Tile 8": "https://cntr.click/SG7sV89"}


def get_tile_count():
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {"email": os.environ['EMAIL'], "password": os.environ['PASSWORD'], "loginSubmit": "Sign In"}
    url = "https://www.linkclickcounter.com/userAccount.php"

    r = requests.post(url=url, headers=headers, data=payload)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")

    tile_click_count_new = {}
    tile_click_count_difference = {}
    table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 0:
            tile_click_count_new[cells[3].find(text=True)] = int(cells[4].find(text=True))

    if not os.path.exists("tile_count.json"):
        tile_click_count_difference = tile_click_count_new.copy()
    else:
        with open("tile_count.json", 'r') as f:
            tile_click_counter_old = json.load(f)
            tile_click_count_difference = {key: tile_click_count_new[key] - tile_click_counter_old.get(key, 0) for key in tile_click_count_new}

    with open("tile_count.json", 'w') as f:
        json.dump(tile_click_count_new, f)

    print(f"Click since last run:{tile_click_count_difference}")
    return tile_click_count_difference


def tictactoe(tile_click_count):
    if not os.path.exists("game_state.json"):
        game_state = {"last_played": None, "tiles": {"Tile 0": None, "Tile 1": None, "Tile 2": None, "Tile 3": None, "Tile 4": None, "Tile 5": None, "Tile 6": None, "Tile 7": None, "Tile 8": None}}

    else:
        with open("game_state.json", 'r') as f:
            game_state = json.load(f)

    if game_state["last_played"] is None:
        game_state["last_played"] = random.choice([True, False])

    move = max(tile_click_count, key=lambda x: tile_click_count[x] if game_state["tiles"][x] is None else -1)

    print(game_state)
    print(move)

    game_state["last_played"] = not game_state["last_played"]
    game_state["tiles"][move] = game_state["last_played"]

    print(game_state)

    winner = None
    for row in range(3):
        if game_state["tiles"][f"Tile {3*row}"] is not None and game_state["tiles"][f"Tile {3*row}"] == game_state["tiles"][f"Tile {3*row + 1}"] == game_state["tiles"][f"Tile {3*row + 2}"]:
            winner = game_state["tiles"][f"Tile {3*row}"]

    for col in range(3):
        if game_state["tiles"][f"Tile {col}"] is not None and game_state["tiles"][f"Tile {col}"] == game_state["tiles"][f"Tile {col+3}"] == game_state["tiles"][f"Tile {col+6}"]:
            winner = game_state["tiles"][f"Tile {col}"]

    if game_state["tiles"]["Tile 0"] is not None and game_state["tiles"]["Tile 0"] == game_state["tiles"]["Tile 4"] == game_state["tiles"]["Tile 8"]:
        winner = game_state["tiles"]["Tile 0"]

    if game_state["tiles"]["Tile 2"] is not None and game_state["tiles"]["Tile 2"] == game_state["tiles"]["Tile 4"] == game_state["tiles"]["Tile 6"]:
        winner = game_state["tiles"]["Tile 2"]

    if winner is None and all(v is not None for k, v in game_state["tiles"].items()):
        winner = "Draw"

    print(winner)

    if winner is not None and os.path.exists("game_state.json"):
        os.remove("game_state.json")
    else:
        with open("game_state.json", 'w') as f:
            json.dump(game_state, f)

    return game_state, winner


def update_readme(game_state, winner):

    tile_content = {}
    for tile in range(9):
        if game_state['tiles'][f'Tile {tile}'] is None:
            tile_content[f"Tile {tile}"] = f"[![Tile {tile}](https://github.com/DoubleGremlin181/DoubleGremlin181/blob/master/assets/{game_state['tiles'][f'Tile {tile}']}.png)]({LINKS[f'Tile {tile}']})"
        else:
            tile_content[f"Tile {tile}"] = f"[![Tile {tile}](https://github.com/DoubleGremlin181/DoubleGremlin181/blob/master/assets/{game_state['tiles'][f'Tile {tile}']}.png)](https://github.com/DoubleGremlin181)"

    README = f"""# Hi, I'm Kavish!
### Welcome to my <img src="https://img.icons8.com/color/96/000000/github--v1.png" height="24"/>GitHub Profile

<p align="center">
  <a href="https://kavishhukmani.me/"><img src="https://img.icons8.com/color/96/000000/internet.png" height="16"/>Personal Website</a> •
  <a href="https://twitter.com/2Gremlin181"><img src="https://img.icons8.com/color/96/000000/twitter-circled.png" height="16"/>Twitter</a> •
  <a href="https://www.linkedin.com/in/kavish-hukmani/"><img src="https://img.icons8.com/color/96/000000/linkedin-circled.png" height="16"/>LinkedIn</a> •
  <a href="mailto:khukmani@gmail.com"><img src="https://img.icons8.com/color/96/000000/email.png" height="16"/>Email</a>
</p>

#### Why not play a game of Tic-Tac-Toe<img src="https://img.icons8.com/material-outlined/96/000000/delete-sign.png" height="16"/><img src="https://img.icons8.com/material-outlined/96/000000/unchecked-circle.png" height="16"/> while you're here
Click on a tile to play  
The most picked move is chosen every hour

{f'Current turn: <img src= "https://github.com/DoubleGremlin181/DoubleGremlin181/blob/master/assets/{not game_state["last_played"]}.png" alt="Current Turn" width="32"/>'
    if winner is None else f'Winner: <img src= "https://github.com/DoubleGremlin181/DoubleGremlin181/blob/master/assets/{winner}.png" alt="Winner" width="32"/>'}

| Tic | Tac | Toe |
|--|--|--|
| {tile_content['Tile 0']} | {tile_content['Tile 1']} | {tile_content['Tile 2']} |
| {tile_content['Tile 3']} | {tile_content['Tile 4']} | {tile_content['Tile 5']} |
| {tile_content['Tile 6']} | {tile_content['Tile 7']} | {tile_content['Tile 8']} |

## How it works

Each open tile is a hyperlink embedded in an image which tracks the number of clicks and redirects you to back my profile.
Every time the program is run it plays the move with maximum number of clicks.
It uses GitHub Actions to run every hour using a cron job.
The rest is just a regular game of Tic-Tac-Toe
    
## About Me


I'm a passionate🥇, creative🎨 and perceptive🔭 engineer🔧 with a hands-on approach to problem-solving and an unending thirst for knowledge🎓. Anything and everything that can be classified as technology💻 fascinates me. My interests and work range from Data Science📈 to creating Chatbots🤖 to building APIs for Computer Vision applications👀 to making AR filters👓 for Instagram and much more. I'm always open to new ideas and opportunities.

"""

    with open("README.md", "w") as f:
        f.write(README)


if __name__ == "__main__":
    tile_click_count = get_tile_count()
    game_state, winner = tictactoe(tile_click_count)
    update_readme(game_state, winner)

