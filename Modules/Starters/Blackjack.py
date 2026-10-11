# The Following code is a GoFish backend
# Rules:

from random import shuffle as shuffle
from time import sleep as sleep

from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Players.Bot import Bot
from Modules.Engines.GoFish.GoFishEngine import GoFishEngine
from faker import Faker
from .Starter import Starter

class Blackjack(Starter):
    pass


if __name__ == "__main__":
    Blackjack().initialize()
