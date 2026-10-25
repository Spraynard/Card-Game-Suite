# The Following code is a GoFish backend
# Rules:

from random import shuffle as shuffle
from time import sleep as sleep

from Modules.Engines.BlackjackEngine import BlackjackEngine
from Modules.Players.Actions.ActionsBlackjack import ActionsBlackjack
from Modules.Players.Dealer import Dealer
from Modules.Players.Player import Player
from Modules.Starters.CardGame import CardGame

class Blackjack(CardGame):
    def initialize(self):
        print("You are going to play a game of Blackjack")
        return super().initialize()
    
    def create_player(self) -> Player:
        return super().create_player()
    
    def create_bot(self) -> Player:
        return super().create_bot()

    def create_dealer(self) -> Player:
        return Dealer()
    
if __name__ == "__main__":
    Blackjack(BlackjackEngine()).initialize()
