import re
import time
import webbrowser
import urllib.parse
import customtkinter
from collections import namedtuple
from playwright.sync_api import sync_playwright

def CenterWindowToDisplay(Screen: customtkinter, width: int, height: int):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 1.5))
    return f"{width}x{height}+{x}+{y}"

Player = namedtuple("Player", ["name", "tag", "rank", "winrate", "games_played"])

# The "best" player is the one with the highest rank. If ranks are equal, choose the one with a higher winrate.
# If winrates are equal, choose the one with the most games played.
def sorting_key(player):
    rank_order = ["Challenger", "Grandmaster", "Master", "Diamond 1", "Diamond 2"]
    return (
        rank_order.index(player.rank),
        -float(player.winrate.strip("%")),
        -int(player.games_played)
    )

def ok_button_click(event=None):
    start_time = time.time()
    region = combo_box.get()
    champion = champion_entry.get()
    root.destroy()
    url = f"https://www.op.gg/leaderboards/champions/{champion.lower()}?region={region.lower()}"

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Since this is a dynamically changing page, we must wait for some elements to appear.
        # Tags for ranks, winrates, and games played for the top 3 players are different from the rest of the players.
        page.wait_for_selector("div.css-12ijbdy.e1swkqyq0")

        # Temporary lists to hold player data.
        player_names = page.query_selector_all("span.css-ao94tw.e1swkqyq1")[:5]
        player_tags = page.query_selector_all("span.css-1mbuqon.e1swkqyq2")[:5]
        player_ranks = page.query_selector_all("small")[:3]
        player_ranks += page.query_selector_all("td.css-13jn5d5.e1nwpw1h3")[:2]
        player_winrate = page.query_selector_all("span > em")[:6]
        player_winrate += page.query_selector_all("div.text")[:2]
        player_games_played = page.query_selector_all("span > em > b")
        player_games_played += page.query_selector_all("td.css-1amolq6.eyczova1 > b")[:2]

        names = [name.text_content() for name in player_names]
        tags = [tag.text_content().replace("#", "") for tag in player_tags]
        ranks = []
        for rank in player_ranks:
            rank_text = rank.text_content().split("Lv.")[0].strip().lower()
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
            winrate_text = winrate.text_content().strip()
            match = re.search(r"\b\d+%$", winrate_text)
            if match:
                winrate_percentage = match.group()
                winrates.append(winrate_percentage)
        games_played = [number.text_content() for number in player_games_played]

        # Create Player objects.
        players = [Player(name, tag, rank, winrate, games) for name, tag, rank, winrate, games in zip(names, tags, ranks, winrates, games_played)]

        # Open the OP.GG webpage for the "best" player.
        players.sort(key=sorting_key)
        best_player = players[0]
        player_url = f"https://www.op.gg/summoners/{region.lower()}/{urllib.parse.quote(best_player.name)}-{urllib.parse.quote(best_player.tag)}"
        webbrowser.open(player_url, new=2, autoraise=False)
        browser.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution Time:", execution_time, "seconds")

# customtkinter.set_appearance_mode("system")
# customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry(CenterWindowToDisplay(root, 290, 145))
root.title("OP.GG Build Finder")

# Region
label = customtkinter.CTkLabel(root, text="Region: ", font=("Arial", 25))
label.grid(row=0, column=0, sticky="w", pady=10, padx=5)
# Dropdown list
combo_box = customtkinter.CTkComboBox(root, values=["NA", "EUW", "EUNE", "OCE", "KR", "JP", "BR", "LAS", "LAN", "RU", "TR",
                                       "SG", "PH", "TR", "TW", "VN", "TH"], font=("Arial", 25), state="readonly")
combo_box.grid(row=0, column=1, sticky="w", pady=10, padx=5)
# Set default value
combo_box.set("KR")

# Champion name
label = customtkinter.CTkLabel(root, text="Champion: ", font=("Arial", 25))
label.grid(row=1, column=0, sticky="w", pady=10, padx=5)
champion_entry = customtkinter.CTkEntry(root, font=("Arial", 25))
champion_entry.grid(row=1, column=1, sticky="w", pady=10, padx=5)
# Wait for button to be fully created before giving it focus
root.update()
champion_entry.focus()

# OK Button
ok_button = customtkinter.CTkButton(root, width=50, text="OK", font=("Arial", 18), command=ok_button_click)
ok_button.grid(row=3, column=1, sticky="e", padx=5)

# Enter key
root.bind("<Return>", ok_button_click)

root.mainloop()
