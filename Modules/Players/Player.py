import random
import uuid

from Modules.Cards.Card import Card
from Modules.Cards.Deck import Deck
from faker import Faker


class Player(object):
    ################
    # INITIALIZATION
    ################
    name = ""

    def __init__(self, name=None):
        self.hand = []
        self.name = name
        # Internal Player's ID
        self.id = uuid.uuid4()

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

    def getName(self):
        return self.name

    #######################################
    # Player Printed Statements ( Talking )
    # 	These statements are required by every player class that will
    # 	be a child of this class (which should be all of em). Game specific printed statements
    # 	shall be implemented in the respective player class
    #######################################

    def victoryStatement(self):
        raise NotImplementedError("Victory Statement")

    def defeatStatement(self):
        raise NotImplementedError("Defeat Statement")

    def talk(self, reason):
        raise NotImplementedError("Talk")

    ##########################
    # Global Hand Helpers
    ##########################

    def getHand(self):
        return self.hand

    def setHand(self, hand):
        self.hand = hand

    def hasHand(self):
        return self.handCount() > 0

    # Gives the length of a player's hand.
    def handCount(self):
        return len(self.getHand())

    #|---------Drawing or Taking Cards Functionality--------|

    def drawCard(self, deck: Deck) -> Card:
        # Summary: Draws a single card from the deck and then adds it to the player's hand
        # Input: `Deck` - The deck being used by the players.
        # Return: Void if everything goes alright. False if shit is messed up
        card = deck.cardFromTop()
        self.takeCard(card)
        return card

    def drawCards(self, deck: Deck, amount: int) -> list:
        cards = []
        for i in range(amount):
            cards.append(self.drawCard(deck))
        return cards

    def takeCard(self, card) -> None:
        self.hand.append(card)

    def takeRelevantCards(self, cardArray) -> None:
        for c in cardArray:
            self.takeCard(c)

    # |--------End Drawing or Taking Cards Functionality-----|
    def resetHand(self) -> None:
        self.hand = []
