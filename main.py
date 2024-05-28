import webbrowser
import urllib.parse
import re
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from player import Player
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def CenterWindowToDisplay(Screen: tk, width: int, height: int):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 1.5))
    return f"{width}x{height}+{x}+{y}"

# The "best" player is the one with the highest rank. If ranks are equal, choose the one with a higher winrate.
# If winrates are equal, choose the one with the most games played.
def sorting_key(player):
    rank_order = ["Challenger", "Grandmaster", "Master", "Diamond 1", "Diamond 2"]
    return (
        rank_order.index(player.rank),
        -float(player.winrate.strip('%')),
        -int(player.games_played)
    )

def ok_button_click(event=None):
    region = combo_box.get()
    champion = champion_entry.get()
    url = "https://www.op.gg/leaderboards/champions/" + champion.lower() + "?region=" + region.lower()

    # Headless browsers are slow and performance-intensive, but lift all restrictions on web scraping.
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get(url)
    # Since this is a dynamically changing page, we must wait for some elements to appear.
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-12ijbdy e1swkqyq0']")))
    except Exception as e:
        print("Error waiting for elements:", e)

    # Write HTML code to a text file for debugging.
    #with open("webpage.html", "w", encoding="utf-8") as file:
    #    file.write(driver.page_source)

    # Tags for ranks, winrates, and games played for the top 3 players are different from the rest of the players.
    soup = BeautifulSoup(driver.page_source, "html.parser")
    player_names = soup.find_all("span", class_="css-ao94tw e1swkqyq1")[:5]
    player_tags = soup.find_all("span", class_="css-1mbuqon e1swkqyq2")[:5]
    player_ranks = soup.find_all("small")[:3]
    player_ranks += soup.find_all("td", class_="css-13jn5d5 e1nwpw1h3")[:2]
    player_winrate = soup.select("span > em")[:6]
    player_winrate += soup.find_all("div", class_="text")[:2]
    player_games_played = soup.select("span > em > b")
    player_games_played += soup.select("td.css-1amolq6.eyczova1 > b")[:2]

    # Temporary lists to hold player data.
    names = [name.get_text() for name in player_names]
    tags = [tag.get_text().replace('#', '') for tag in player_tags]
    ranks = []
    for rank in player_ranks:
        rank_text = rank.get_text().split("Lv.")[0].strip().lower()
        if "challenger" in rank_text:
            rank_text = "Challenger"
        elif "grandmaster" in rank_text:
            rank_text = "Grandmaster"
        elif "master" in rank_text:
            rank_text = "Master"
        elif "diamond 1" in rank_text:
            rank_text = "Diamond 1"
        elif "diamond 2" in rank_text:
            rank_text = "Diamond 2"
        ranks.append(rank_text)
    winrates = []
    for winrate in player_winrate:
        winrate_text = winrate.get_text().strip()
        match = re.search(r'\b\d+%$', winrate_text)
        if match:
            winrate_percentage = match.group()
            winrates.append(winrate_percentage)
    games_played = [number.get_text() for number in player_games_played]

    # Create Player objects.
    players = []
    for name, tag, rank, winrate, games in zip(names, tags, ranks, winrates, games_played):
        player = Player(name, tag, rank, winrate, games)
        players.append(player)
    #for player in players:
    #    player.showDescription()

    # Open the OP.GG webpage for the "best" player.
    players.sort(key=sorting_key)
    best_player = players[0]
    url = "https://www.op.gg/summoners/" + region.lower() + "/" + urllib.parse.quote(best_player.name) + "-" + urllib.parse.quote(best_player.tag)
    webbrowser.open(url, new=2, autoraise=False)

    '''
    driver.get(url)
    search_box = driver.find_element_by_xpath("//div[@class='search']//input[@id='championInput']")
    search_box.send_keys("Malphite")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='champion-name' and text()='Malphite']")))
    malphite_button = driver.find_element_by_xpath("//span[@class='champion-name' and text()='Malphite']")
    malphite_button.click()
    '''

    driver.quit()
    root.destroy()

root = tk.Tk()
root.geometry(CenterWindowToDisplay(root, 570, 130))
root.title("OP.GG Build Finder")

# Change font of Combobox dropdown list
root.option_add("*TCombobox*Listbox.font", "Arial 25")

# Region
label = tk.Label(root, text="Region: ", font=("Arial", 25))
label.grid(row=0, column=0, sticky="w", pady=10)
# Dropdown list
combo_box = ttk.Combobox(root, values=["NA", "EUW", "EUNE", "OCE", "KR", "JP", "BR", "LAS", "LAN", "RU", "TR",
                                       "SG", "PH", "TR", "TW", "VN", "TH"], font=("Arial", 25))
combo_box.grid(row=0, column=1, sticky="w", pady=10, padx=5)
# Set default value
combo_box.set("KR")

# Champion name
label = tk.Label(root, text="Champion: ", font=("Arial", 25))
label.grid(row=1, column=0, sticky="w", pady=10)
champion_entry = tk.Entry(root, font=("Arial", 25))
champion_entry.grid(row=1, column=1, sticky="w", pady=10, padx=5)
champion_entry.focus()

# OK Button
ok_button = tk.Button(root, text="OK", font=("Arial", 18), command=ok_button_click)
ok_button.grid(row=1, column=1, sticky="e")

# Enter key
root.bind('<Return>', ok_button_click)

root.mainloop()
