import requests
import json
import os
import random
import datetime

LINKS = {"Tile 0": "https://l.linklyhq.com/l/1pupi",
         "Tile 1": "https://l.linklyhq.com/l/1pupm",
         "Tile 2": "https://l.linklyhq.com/l/1pupo",
         "Tile 3": "https://l.linklyhq.com/l/1pupp",
         "Tile 4": "https://l.linklyhq.com/l/1pupt",
         "Tile 5": "https://l.linklyhq.com/l/1pupv",
         "Tile 6": "https://l.linklyhq.com/l/1puq3",
         "Tile 7": "https://l.linklyhq.com/l/1puq8",
         "Tile 8": "https://l.linklyhq.com/l/1puq9"}


def get_tile_count():
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"api_key": os.environ['API_KEY'], "workspace_id": int(os.environ['WORKSPACE_ID']), "format": "csv",
              "start": "2023-05-26", "end": str(datetime.date.today() + datetime.timedelta(days=7))}  # Adding a buffer for end_date
    url = "https://app.linklyhq.com/api/v1/workspace/113887/clicks/counters/link_id"

    r = requests.get(url=url, headers=headers, params=params)
    table = r.text

    tile_click_count_new = {}
    tile_click_count_difference = {}

    for row in table.split("\r\n"):
        cells = row.split(',')
        if len(cells) == 4:  # Check for end of file
            tile_click_count_new[cells[1]] = int(cells[3])

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

Hey there! 👋 My name is Kavish Hukmani, and I'm a passionate 🥇, creative 🎨, and perceptive 🔭 engineer 🔧 with a hands-on approach to problem-solving and an unending thirst for knowledge 📚. Anything and everything that can be classified as technology 💻 fascinates me.

Currently, I'm based in the beautiful city of San Francisco 🌉 where I work as a Data Scientist 🧑‍🔬 at Unison, tackling fascinating problems in Finance 💰, Housing 🏠, and Marketing 📣. Before that, I was part of the Impact Analytics team, creating products that helped top Retail 💃 and CPG 🍫 companies make data-driven decisions like a breeze. Oh, and I proudly hold an MS in Business Analytics 📊 from UC Davis 🎓.

When I'm not immersed in the world of technology, you can find me following a range of sports, from Soccer ⚽ and Formula1 🏎️ to various eSports 🖱️. Apart from that, I love solving puzzles 🧩 and listening to music 🎶.

I'm always open to new ideas and opportunities. You can learn more about me on my [website](https://kavishhukmani.me/) 🌐 or connect with me on [LinkedIn](https://www.linkedin.com/in/kavish-hukmani/) 👥. Feel free to reach out to me directly at [khukmani@gmail.com](mailto:khukmani@gmail.com) 📧. Let's connect and explore exciting possibilities together! 🚀
"""

    with open("README.md", "w") as f:
        f.write(README)


if __name__ == "__main__":
    tile_click_count = get_tile_count()
    game_state, winner = tictactoe(tile_click_count)
    update_readme(game_state, winner)

