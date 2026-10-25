from random import shuffle

from faker import Faker

from Modules.Players.Player import Player, Players
from Modules.Starters.Starter import Starter

class CardGame(Starter):
    """
    Kind of like a mixin class for all card games
    that's helpful to pass around.
    """    
    def initialize(self):
        try:
            self.human_amount = self.prompt_for_players()
        except Exception as e:
            raise Exception(f"There is a problem in `handle_player_init()` - {e}")

        try:
            self.bot_amount = self.prompt_for_bots()
        except:
            raise Exception(f"There was an error initializing the bots - {e}")

        self.players = self.create_players(self.human_amount, self.bot_amount)
        self.start_game()
    
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

    def prompt_for_players(self) -> int:
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
                self.human_players = True
                break
        return player_n

    def create_player(self) -> Player:
        raise Exception("Not Implemented -- create_player()")
    
    def create_bot(self) -> Player:
        raise Exception("Not Implemented -- create_bot()")
    
    def create_players(self, human_amount: int, bot_amount: int):
        faker = Faker()
        player_names = self.get_players_names_prompt(human_amount)
        players: Players = []

        for i in range(human_amount):
            name = None
            if player_names:
                name = player_names[i]
            else:
                name = faker.name()
            player = self.create_player()
            player.name = name
            players.append(player)

        for i in range(bot_amount):
            bot = self.create_bot()
            bot.name = faker.name()
            players.append(bot)

        return players
    
    def get_players_names_prompt(self, player_n) -> int:
        names = False
        while not names and self.human_players:
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