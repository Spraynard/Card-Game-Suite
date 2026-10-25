from random import shuffle as shuffle
from time import sleep as sleep
from Modules.Engines.Engine import Engine
from Modules.Engines.GoFish.GoFishEngine import GoFishEngine
from Modules.Players.PlayerGoFish import PlayerGoFish
from Modules.Players.BotGoFish import BotGoFish
from Modules.Players.Player import Player
from Modules.Starters.CardGame import CardGame

class GoFish(CardGame):
    max_players = 6
    min_players = 4
    max_human_players = 1

    def __init__(self) -> None:
        super().__init__(GoFishEngine())

    def initialize(self) -> None:
        print("Welcome to another round of the famous game, Go Fish!")
        return super().initialize()

    def create_player(self) -> Player:
        return PlayerGoFish()
    
    def create_bot(self) -> Player:
        return BotGoFish()

if __name__ == "__main__":
    GoFish().initialize()
