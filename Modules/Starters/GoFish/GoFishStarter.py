# The Following code is a GoFish backend
# Rules:
# * Use 1 Deck of 52 Cards
# * Players are dealt seven random cards

# * Remaining cards make up the pool for users to Go Fish from

# * A turn consists of the current player selecting a card from their hand, and asking an opponent if they have any cards of the same rank
# * If the opponent has a card(s) of that rank, the opponent must give the card(s) to the player who requested it and that player gets another turn
# * If the opponent does not have any cards of that rank, the requesting player must Go Fish and draw a random card from the pool; ending that player's turn
# * As soon as a player collects a book of four cards of the same rank (ex. four Jacks or four 3s), they must lay their book down; removing the cards from their hand
# * If a player has no cards in their hand, they must draw from the pool; if the pool is empty, that player is out of the game
# * The game is over when all 13 sets of four, books, have been matched
# * The player with the most books is determined the winner
from random import shuffle as shuffle
from time import sleep as sleep

import sys

from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Players.Bot import Bot
from Modules.Engines.GoFish.GoFishEngine import GoFishEngine
from faker import Faker


class GoFishStarter:
    def __init__(self, test=False):
        self.players = []
        self.engine = GoFishEngine()
        self.test = test
        self.max_human_players = 1
        self.max_players = 6
        self.min_players = 4
        self.min_bots = 0
        self.human_amount = 0
        self.bot_amount = 0
        # If there are human players in the game
        self.humanPlayers = False

    def get_if_human_players(self):
        """Returns true if there are any human players in the game"""
        return self.humanPlayers

    def set_human_players(self, flag: bool):
        self.humanPlayers = flag

    def get_players_names_prompt(self, player_n) -> int:
        names = False
        while not names and self.get_if_human_players():
            name_flag = str(input("Would you like to name yourselves (Y/N)?: ")).lower()

            names = []
            if name_flag == "y":
                print("Okay, please input the names for each player: ")
                for i in range(player_n):
                    i_name = input("Player #%s: " % (i + 1))
                    names.append(i_name)

                    if i == player_n - 1:
                        break
            else:
                return

        return names

    def add_player(self, player):
        self.players.append(player)

    def add_all_players(self, human_amount, bot_amount):
        player_bucket = []
        player_names = self.get_players_names_prompt(human_amount)

        for i in range(human_amount):
            if player_names:
                player_bucket.append(HumanPlayer(player_names[i]))
            else:
                player_bucket.append(HumanPlayer())

        for i in range(bot_amount):
            fake = Faker()
            bot = Bot(fake.name())
            player_bucket.append(bot)

        if not self.test:
            shuffle(player_bucket)

        for p in player_bucket:
            self.add_player(p)

    def prompt_for_bots(self):
        # Asks the players how many bots people want in their game.
        # 	Returns the number given.
        bot_n = False
        # The number to fill up the card table
        try:
            # The amount of bots that can be used to fill empty slots in this game
            max_bots = self.max_players - self.human_amount
        except:
            raise Exception("Error with getting the # of players")
        if max_bots == 0:
            return False
        while True:
            try:
                input_bot_amount = int(
                    input(f"Please enter the number of bots (Max: {max_bots}): ")
                )
            except:
                print(
                    "You entered something I can't understand, probably a non-numerical"
                )
                continue

            total_player_amount = input_bot_amount + self.human_amount
            bare_min_player_amt = (
                self.max_players - self.human_amount - input_bot_amount
            )

            if input_bot_amount > 0 and bare_min_player_amt > 0:
                print(f"The amount you gave is less than {bare_min_player_amt}")
                print(
                    "We're going to fill bots up to the amount of player slots you need..."
                )

                return bare_min_player_amt

            if input_bot_amount > max_bots:
                print("You can't have more than %s bots right now" % max_bots)
            else:
                return input_bot_amount

    def promptForPlayers(self) -> int:
        player_n = False

        while True:
            human_player_amount_input = False
            try:
                human_player_amount_input = int(
                    input(
                        f"Please enter the number of human players (max: {self.max_human_players}): "
                    )
                )
            except:
                print(f"Nope need to enter a # between 0 and {self.max_human_players}")
                continue

            if human_player_amount_input == 0:
                print("Haha, you're playing an all bot game. That's pretty nice!")
                break

            if human_player_amount_input > self.max_human_players:
                print(f"You can't have more than {self.max_human_players} players")
            else:
                player_n = human_player_amount_input
                self.set_human_players(True)
                break
        return player_n

    def handle_player_init(self):
        pass

    def start_game(self):
        self.engine.set_players(self.players)
        self.engine.initialize()

    def initialize_go_fish(self):
        if self.test:
            print("This is now in test mode")
            sleep(2)
        print("Welcome to another round of the famous game, Go Fish!")
        # Returns: Void
        try:
            self.human_amount = self.promptForPlayers()
        except Exception as e:
            raise Exception(f"There is a problem in `handle_player_init()` - {e}")

        try:
            self.bot_amount = self.prompt_for_bots()
        except:
            raise Exception(f"There was an error initializing the bots - {e}")

        self.add_all_players(self.human_amount, self.bot_amount)
        self.start_game()


if __name__ == "__main__":
    GoFishStarter().initialize_go_fish()
