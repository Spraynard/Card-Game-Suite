from random import shuffle as shuffle
from time import sleep as sleep
from Modules.Engines.GoFish.GoFishEngine import GoFishEngine
from Modules.Players.Actions.ActionsGoFish import ActionsGoFish, GoFishBotActions
from Modules.Starters.CardGame import CardGame

class GoFish(CardGame):
    max_players = 6
    min_players = 4
    max_human_players = 1

    def initialize(self) -> None:
        print("Welcome to another round of the famous game, Go Fish!")
        return super().initialize()
    
    def player_actions(self) -> ActionsGoFish:
        return ActionsGoFish()
    
    def bot_actions(self) -> GoFishBotActions:
        return GoFishBotActions()

if __name__ == "__main__":
    GoFish(GoFishEngine()).initialize()
