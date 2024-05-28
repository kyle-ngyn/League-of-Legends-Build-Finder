class Player:
    def __init__(self, name, tag, rank, winrate, games_played):
        self.name = name
        self.tag = tag
        self.rank = rank
        self.winrate = winrate
        self.games_played = games_played

    def showDescription(self):
        print("Name: " + self.name + " #" + self.tag + "\n" +
              "Rank: " + self.rank + "\n" +
              "Winrate: " + self.winrate + "\n" +
              "Games Played: " + self.games_played + "\n")
