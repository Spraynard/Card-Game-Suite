# The Following code is a GoFish backend
# Rules:
# * Use 1 Deck of 52 Cards
# * Players are dealt seven random cards

# * Remaining cards make up the pool for users to Go Fish from

# * A turn consists of the current player selecting a card from their hand, and asking an opponent if they have any cards of the same rank
# * If the opponent has a card(s) of that rank, the opponent must give the card(s) to the player who requested it and that player gets another turn
# * If the opponent does not have any cards of that rank, the requesting player must Go Fish and draw a random card from the pool; ending that player's turn
# * As soon as a player collects a book of four cards of the same rank (ex. four Jacks or four 3s), they must lay their book down; removing the cards from their hand
# * If a player has no cards in their hand, they must draw from the pool
# * If the pool is empty:
#       * If the player has no cards, they are out of the game.
#       * Play without drawing cards otherwise.
# * The game is over when all 13 sets of four, books, have been matched
# * The player with the most books is determined the winner
from random import shuffle as shuffle
from time import sleep as sleep

from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Players.Bot import Bot
from Modules.Engines.GoFish.GoFishEngine import GoFishEngine
from faker import Faker

from Modules.Starters.CardGame import CardGame
from .Starter import Starter

class GoFish(Starter, CardGame):
    max_players = 6
    min_players = 4
    max_human_players = 1

    def __init__(self, test=False):
        super.__init__(self, GoFishEngine())
        self.test = test
        # If there are human players in the game
        self.humanPlayers = False

    def get_if_human_players(self):
        """Returns true if there are any human players in the game"""
        return self.humanPlayers

    def set_human_players(self, flag: bool):
        self.humanPlayers = flag

    
    def initialize(self) -> None:
        print("Welcome to another round of the famous game, Go Fish!")
        return super().initialize()


if __name__ == "__main__":
    GoFish().initialize()
