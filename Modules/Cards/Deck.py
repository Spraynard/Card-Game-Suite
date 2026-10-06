import random
from .Card import Card
import uuid


class Deck(object):
    """The deck object which holds all the cards the players will be using"""

    def __init__(self):
        self.cards = []
        self.id = uuid.uuid4()

    def __eq__(self, other):
        return self.id == other.id

    def _shuffleCards(self):
        random.shuffle(self.get_cards())

    def _addCard(self, card):
        self.get_cards().append(card)

    def _buildDeck(self):
        ranks = [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
            "Ace",
        ]
        suits = ["Clubs", "Spades", "Diamonds", "Hearts"]

        for s in suits:
            for r in ranks:
                card = Card(r, s)
                self._addCard(card)

                # Presents a card from the top of the deck.

    def card_from_top(self):
        if not self.current_amount():
            print("Why is my length 0?")
            return None
        card = self.get_cards().pop()
        return card

    def get_cards(self):
        return self.cards

    def current_amount(self):
        return len(self.get_cards())

    def list_cards(self):
        for i in range(0, len(self.get_cards())):
            print(self.get_cards()[i])

    def has_card(self, card):
        if card in self.get_cards():
            return True
        return False

    def initialize(self):
        self._buildDeck()
        self._shuffleCards()
