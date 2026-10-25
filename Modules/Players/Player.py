from enum import Enum
from typing import Self, List
import uuid

from faker import Faker

from Modules.Players.Actions.ActionsCard import ActionsCard

class PlayerTalkReason(Enum):
    VICTORY = "victory"
    DEFEAT  = "defeat"
    EXCLAIM = "exclaim"
    ASK     = "ask"

# from card_game_suite_types import ActionsT
class Player(ActionsCard):
    ################
    # INITIALIZATION
    ################
    name = ""
    def __init__(self):
        # Internal Player's ID
        self.id = uuid.uuid4()


        # Defines equality from one player to the other based on the internal ID that they have.

    def __eq__(self, other: object):
        return self.id == other.id

    def __repr__(self):
        return str(self.name) or "Player"

    def __str__(self):
        if not self.name:
            return "'%s'" % self.name
        else:
            return "Player"

    def random_name(self) -> Self:
        # Returns a `Player` with a random name from the Faker lib
        # 	can get some pretty funny names :)
        fake = Faker()
        return self(fake.name)

    def get_name(self):
        return self.name

Players = List[Player]