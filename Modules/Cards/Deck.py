import random
from typing import Self
from .Card import Card, Cards
import uuid


class Deck(object):
    """The deck object which holds all the cards the players will be using"""

    cards: Cards = []
    id = uuid.uuid4()

    def __init__(self) -> None:
        """
        Initially create the actual deck from all
        suits and ranks
        """
        for suit in Card.suits:
            for rank in Card.ranks:
                card = Card(rank, suit)
                self.cards.append(card)
        
    def __eq__(self, other: Self):
        return self.id == other.id

    def shuffle(self) -> None:
        """
        Shuffles the entire deck of cards.
        Make sure there are some cards
        """
        return random.shuffle(self.cards)

    def draw(self) -> Card | None:
        """
        Draw a card from the top of the deck
        """

        if (len(self.cards) == 0):
            return None
        
        return self.cards.pop()

    def list_cards(self) -> None:
        [print(self.cards[i]) for i in range(len(self.cards))]

    def has_card(self, card: Card):
        return card in self.cards

    def initialize(self):
        self._buildDeck()
        self.shuffle()
