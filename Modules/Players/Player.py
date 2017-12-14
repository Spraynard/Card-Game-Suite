import random
import uuid
import sys

sys.path.append('../')

from Modules.Debug.TermColor import *

class Player(object):

	################
	# INITIALIZATION
	################

	def __init__(self, name = None):
		self.hand = []
		self.name = name
		# Internal Player's ID
		self.id = uuid.uuid4()

	def __eq__(self, other):
		return self.id == other.id

	def __repr__(self):
		return str(self.name) or "Player"

	def __str__(self):
		if not self.name:
			return "'%s'" % self.name
		else:
			return "Player"

	def randomName(self):
		# Returns a `Player` with a random name from the Faker lib
		#	can get some pretty funny names :)
		from faker import Faker
		fake = Faker()
		return Player(fake.name())

	def getName(self):
		return self.name

	#######################################
	# Player Printed Statements ( Talking )
	#	These statements are required by every player class that will
	#	be a child of this class (which should be all of em). Game specific printed statements
	#	shall be implemented in the respective player class
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

	def showHand(self):
		# Prints out the hand legibly in a line!
		hand = self.getHand()

		for c in hand:
			print c,

	def handCount(self):
		return len(self.getHand())

	def drawCard(self, card):
		# Summary: Draws a single card from the deck and then adds it to the player's hand
		# Input: `Deck` - The deck being used by the players. 
		# Return: Void if everything goes alright. False if shit is messed up		
		if not card:
			return
		self.takeCard(card)

	#|---------Drawing or Taking Cards Functionality--------|

	def takeCard(self, card):
		self.hand.append(card)

	def takeRelevantCards(self, cardArray):
		for c in cardArray:
			self.takeCard(c)

	# |--------End Drawing or Taking Cards Functionality-----|

	def drawHand(self, deck, **gameType):
		blackjack = None
		goFish = None
		handSize = None

		if 'blackjack' in gameType:
			blackjack = gameType['blackjack']
			# Oh wait, does blackjack even have a hand size?
			# 	This can be used for other games though.
		elif 'goFish' in gameType:
			goFish = gameType['goFish']
			# 4 or more players
			handSize = 5
			if goFish:
				# 3 or less players
				handSize = 7

		for i in range(handSize):
			drawnCard = deck.draw()
			self.drawCard(drawnCard)

	def resetHand(self):
		self.hand = []


 	##########################
 	# Go Fish specific methods
 	##########################




