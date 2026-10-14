import uuid

from faker import Faker
from typing import Generic, TypeVar, Optional

from Modules.Players.Actions.CardActions import CardActions


ActionsT = TypeVar("ActionsT", bound="CardActions")

class Player(Generic[ActionsT]):
    ################
    # INITIALIZATION
    ################
    name = ""
    actions: Optional[ActionsT]
    def __init__(self, name=None, actions: Optional[ActionsT] = None):
        self.name = name
        # Internal Player's ID
        self.id = uuid.uuid4()
        self.actions = actions

        # Defines equality from one player to the other based on the internal ID that they have.

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return str(self.name) or "Player"

    def __str__(self):
        if not self.name:
            return "'%s'" % self.name
        else:
            return "Player"

    def random_name(self):
        # Returns a `Player` with a random name from the Faker lib
        # 	can get some pretty funny names :)
        fake = Faker()
        return Player(fake.name())

    def get_name(self):
        return self.name

        #######################################
        # Player Printed Statements ( Talking )
        # 	These statements are required by every player class that will
        # 	be a child of this class (which should be all of em). Game specific printed statements
        # 	shall be implemented in the respective player class
        #######################################

    def victory_statement(self):
        raise NotImplementedError("Victory Statement")

    def defeat_statement(self):
        raise NotImplementedError("Defeat Statement")

    def talk(self, reason):
        raise NotImplementedError("Talk")
