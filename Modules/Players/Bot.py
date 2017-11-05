import sys
import time

sys.path.append('../Cards/')

from HumanPlayer import HumanPlayer

class Bot(HumanPlayer):
	"""Bot object, which is a player. There are taunts available to bots to rouse up the player whenver they make a mistake"""
	def __init__(self, name = None):
		super(Bot, self).__init__()
		self.taunts = ["You're going to have to try harder than that!\"" ,
						"I thought that I was playing a real person, not a bot!\"" ,
						"What the heck are you doing?\"" ,
						"Dang, I didn't know I was playing a baby tonight\"" ]
		
		self.rejections = ["%s: \"No", "%s: \"Nope", "%s: \"I sure do not", "%s: \"Hahaha, no", "%s: \"You wish!"]
		
		self.chooseDict = {}
		self.name = name

	def __repr__(self):
		return "Bot #: %s" % self.id

	def __str__(self):
		return "Bot - %s" % self.name

	def __eq__(self, other):
		return self.id == other.id

	def randomName(self):
		from faker import Faker
		fake = Faker()
		return Bot(fake.name())

	def tauntPlayer(self):
		import random
		return random.choice(self.rejections) % self.getName() + '. ' + random.choice(self.taunts)

	# Hand Evaluation Functionality
	def _assembleChooseDict(self):
		hand = self.getHand()
		for c in hand:
			self._addChooseDict(c)

	def _analyzeChooseDict(self):
		# Haha, this is laughably bad AI for the bots.
		#	Might as well have a random card generator for now
		from Card import Card
		maxCount = None
		rankMax = None
		cD = self._getChooseDict()
		chooseDictKeys = cD.keys()

		for k in chooseDictKeys:
			currentLength = len(cD[k])
			if (not maxCount) or (maxCount < currentLength):
				maxCount = currentLength
				rankMax = k

		self.setChosenCard(Card(rankMax))

	def _randomChoice(self):
		import random

		hand = self.getHand()

		if len(hand) == 0:
			from Card import Card
			chooseableCards = Card().acceptDict['ranks']
			self.setChosenCard(Card(random.choice(chooseableCards)))
		else:
			self.setChosenCard(random.choice(hand))
	
	# chooseDict Functionality
	def _getChooseDict(self):
		return self.chooseDict

	def _addChooseDict(self, card):
		# Initializes the card rank key with an array if that key is not
		# 	in `chooseDict`. Then appends the card into the key's array.
		chooseDict = self._getChooseDict()
		cardRank = card.getRank()

		if not cardRank in chooseDict:
			chooseDict[cardRank] = []

		chooseDict[cardRank].append(card)

	def _resetChooseDict(self):
		self.chooseDict = {}

	def chooseCard(self):
	# Implement Bot Card Choosing. Game will not work without this. What I eventually want to to is
		#  1. Bot looks through hand for cards they have
		#  2. Of cards that bot has, look for the rank in which you have the most of.
		#  2a. If you have multiple ranks with the same amount, break by choosing randomly
		self._assembleChooseDict()
		# self._analyzeChooseDict()
		self._randomChoice()