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

Player = namedtuple("Player", ["URI", "rank", "LP", "winrate", "games"])

# The "best" player is the one with the highest rank and LP. If ranks are equal, choose the one with the
# highest LP. If ranks and LP are equal, choose the one with the higher winrate. If winrates are equal,
# choose the one with the most games played.
def sorting_key(player):
    rank_order = {"challenger": 0, "grandmaster": 1, "master": 2, "diamond 1": 3, "diamond 2": 4}
    return (
        -int(player.LP),
        rank_order.get(player.rank.lower(), float("inf")),
        -float(player.winrate.strip("%")),
        -int(player.games)
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

    whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\'')
    champion = ''.join(filter(whitelist.__contains__, championName))

    if region == "NA" or region == "EUW" or region == "EUN" or region == "BR" or region == "JP" or region == "TR" or region == "ME":
        region += "1"
    elif region == "OCE":
        region = "oc1"
    elif region == "LAN":
        region = "la1"
    elif region == "LAS":
        region = "la2"
    elif region == "PH" or region == "SG" or region == "TH" or region == "TW" or region == "VN":
        region += "2"
    else:
        pass

    url = f"https://u.gg/lol/champion-leaderboards/{champion.lower()}?region={region.lower()}"

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.on("route", block_resources)
        page.goto(url, wait_until="commit")

        # Since this is a dynamically changing page, we must wait for some elements to appear.
        page.locator("div.top-five_ranking:nth-child(2)").wait_for()

        # Temporary lists to hold player data.
        URIs = page.locator(".ranking-user-row").get_by_role("link").all()
        URIs += page.locator(".ranking-user-column").get_by_role("link").all()
        #names = page.locator(".ranking-user-row").all_text_contents()
        #names += page.locator(".ranking-user-column > a").all_text_contents()
        ranks = page.locator(".rank-display > span > strong").all_text_contents()[:5]

        # The locator outputs to something like:
        # ["/",  "950 LP", "/", "950 LP", "/",  "800 LP", "/", "800 LP"]
        # We only want the LP numbers. So we are going to start at index 1, skip by 4,
        # and get the first 5 values we see. We skip by 4 because the LPs repeat.
        LPs = page.locator(".rank-display > span > span").all_text_contents()[1:40:4]

        # Winrates and games played repeat as well.
        winrates = page.locator(".wr-text_win-rate").all_text_contents()[1:10:2]
        games_played = page.locator(".wr-text_games").all_text_contents()[1:10:2]

        # Create Player objects.
        players = [Player(URI.get_attribute("href").strip(" "),
                          rank.strip(),
                          LP.strip(" LP").replace(",", ""),
                          winrate.strip(),
                          "".join(filter(str.isdigit, games)))
                          for URI, rank, LP, winrate, games in zip(URIs, ranks, LPs, winrates, games_played)]

        # Open the U.GG webpage for the "best" player.
        players.sort(key=sorting_key)

        '''
        print()
        for player in players:
            print(f"{player.rank} {player.LP} LP, {player.winrate} winrate, {player.games} games")
        '''

        best_player = players[0]
        player_url = f"https://u.gg{urllib.parse.quote(best_player.URI)}"

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
root.title("U.GG Build Finder")

# Region
label = customtkinter.CTkLabel(root, text="Region: ", font=("Arial", 25))
label.grid(row=0, column=0, sticky="w", pady=10, padx=5)
# Dropdown list
combo_box = customtkinter.CTkComboBox(root, values=["World", "NA", "EUW", "EUN", "KR", "BR", "JP", "RU",
                                                    "OCE", "TR", "LAN", "LAS", "PH", "SG", "TH", "TW",
                                                    "VN", "ME"],
                                                    font=("Arial", 25), state="readonly")
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
