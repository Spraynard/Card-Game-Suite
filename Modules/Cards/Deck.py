import random

class Deck(object):
	""" The deck object which holds all the cards the players will be using"""
	def __init__(self):
		import uuid

		self.cards = []
		self.id = uuid.uuid4()

	def __eq__(self, other):
		return self.id == other.id

	def _shuffleCards(self):
		random.shuffle(self.getCards())

	def _addCard(self, card):
		self.getCards().append(card)

	def _buildDeck(self):
		from Card import Card

		ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
		suits = ["Clubs", "Spades", "Diamonds", "Hearts"]

		for s in suits:
			for r in ranks:
				card = Card(r, s)
				self._addCard(card)

	# Drawing from the deck
	def draw(self):
		return self.getCards().pop()

	def getCards(self):
		return self.cards

	def currentAmount(self):
		return len(self.getCards())

	def listCards(self):
		for i in range(0, len(self.getCards())):
			print self.getCards()[i]

	def hasCard(self, card):
		if card in self.getCards():
			return True
		return False

	def initialize(self):
		self._buildDeck()
		self._shuffleCards()
