# The Following code is a GoFish backend
# Rules:

from random import shuffle as shuffle
from time import sleep as sleep

from Modules.Engines.BlackjackEngine import BlackjackEngine
from Modules.Starters.CardGame import CardGame

class Blackjack(CardGame):
    def initialize(self):
        print("You are going to play a game of Blackjack")
        return super().initialize()

if __name__ == "__main__":
    Blackjack(BlackjackEngine()).initialize()
