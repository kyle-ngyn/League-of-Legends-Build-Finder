#import time
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

Player = namedtuple("Player", ["name", "tag", "rank", "LP", "winrate", "games_played"])

# The "best" player is the one with the highest rank and LP. If ranks are equal, choose the one with the
# highest LP. If ranks and LP are equal, choose the one with the higher winrate. If winrates are equal,
# choose the one with the most games played.
def sorting_key(player):
    rank_order = {"challenger": 0, "grandmaster": 1, "master": 2, "diamond 1": 3, "diamond 2": 4}
    return (
        -int(player.LP),
        rank_order.get(player.rank.lower(), float("inf")),
        -float(player.winrate.strip("%")),
        -int(player.games_played)
    )

def block_resources(route, request):
    if request.resource_type in ["image", "font", "stylesheet", "media"]:
        route.abort()
    else:
        route.continue_()

def ok_button_click(event=None):
    #start_time = time.time()
    region = combo_box.get()
    championName = champion_entry.get()
    root.destroy()

    whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    champion = ''.join(filter(whitelist.__contains__, championName))

    url = f"https://www.op.gg/lol/leaderboards/champions/{champion.lower()}?region={region.lower()}"

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.on("route", block_resources)
        page.goto(url, wait_until="commit")

        # Since this is a dynamically changing page, we must wait for some elements to appear.
        page.locator("li.flex:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1)").wait_for()

        # Temporary lists to hold player data.
        names = page.locator("td:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)").all_text_contents()[:5]
        tags = page.locator("td:nth-child(2) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(2)").all_text_contents()[:5]
        ranks = page.locator("td:nth-child(3) > div:nth-child(1)").all_text_contents()[:5]
        LPs = page.locator("td:nth-child(4)").all_text_contents()[:5]
        winrates = page.locator("td:nth-child(7) > div:nth-child(1) > span:nth-child(2)").all_text_contents()[:5]
        games_played = page.locator("td:nth-child(6) > div:nth-child(1)").all_text_contents()[:5]

        # Create Player objects.
        players = [Player(name,
                          tag.strip("#"),
                          rank,
                          LP.replace(",", ""),
                          winrate,
                          games.replace(",", ""))
                          for name, tag, rank, LP, winrate, games in zip(names, tags, ranks, LPs, winrates, games_played)]

        # Open the OP.GG webpage for the "best" player.
        players.sort(key=sorting_key)

        '''
        print()
        for player in players:
            print(f"{player.name}#{player.tag}: {player.rank} {player.LP} LP, {player.winrate} winrate, {player.games_played} games")
        '''

        best_player = players[0]
        player_url = f"https://www.op.gg/lol/summoners/{region.lower()}/{urllib.parse.quote(best_player.name)}-{urllib.parse.quote(best_player.tag)}"

        webbrowser.open(player_url, new=2, autoraise=False)
        browser.close()

    '''
    end_time = time.time()
    execution_time = end_time - start_time
    print("\nExecution Time:", execution_time, "seconds\n")
    '''

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
