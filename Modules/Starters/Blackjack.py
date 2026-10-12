# The Following code is a GoFish backend
# Rules:

from random import shuffle as shuffle
from time import sleep as sleep

from Modules.Engines.BlackjackEngine import BlackjackEngine
from Modules.Starters.CardGame import CardGame

class Blackjack(CardGame):
    pass

if __name__ == "__main__":
    Blackjack(BlackjackEngine()).initialize()
