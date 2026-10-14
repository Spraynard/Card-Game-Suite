import random

from .Player import Player
from faker import Faker

class HumanPlayer(Player):
    """Player object, All the commands that the player will use in the game are here."""
    
    def random_name(self):
        # Returns a `Player` with a random name from the Faker lib
        # 	can get some pretty funny names :)
        fake = Faker()
        return HumanPlayer(fake.name())

    def victory_statement(self):
        statement_dict = {
            1: '"I sure do not!"',
        }
        print(statement_dict[random.choice(list(statement_dict.keys()))])

    def defeat_statement(self):
        statement_dict = {
            1: '%s: "I do have %s cards. Here they are": %s',
        }
        print(
            statement_dict[random.choice(list(statement_dict.keys()))]
            % (self.get_name(), len(self.get_give_array()), self.get_give_array())
        )

    def talk(self, reason):
        reason_dict = {
            "victory": self.victory_statement,
            "defeat": self.defeat_statement,
            "exclaim": self.exclaim,
            "ask": self.ask_other_player,
        }

        reason_dict[reason]()