import random
import uuid
import sys

sys.path.append('../')

# from Modules.Debug.TermColor import *

class Player(object):

	################
	# INITIALIZATION
	################

	def __init__(self, name = None):
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

		print 'Hand: [',
		for i in range(len(hand)):
			if ( i < ( len(hand) - 1 ) ):
				print str(hand[i]) + ',',
			else:
				print str(hand[i]),
		print ']'

	# Gives the length of a player's hand.
	def handCount(self):
		return len(self.getHand())

	#|---------Drawing or Taking Cards Functionality--------|

	def drawCard(self, deck):
		# Summary: Draws a single card from the deck and then adds it to the player's hand
		# Input: `Deck` - The deck being used by the players.
		# Return: Void if everything goes alright. False if shit is messed up
		self.takeCard(deck.cardFromTop())


	def takeCard(self, card):
		self.hand.append(card)

	def takeRelevantCards(self, cardArray):
		for c in cardArray:
			self.takeCard(c)

	# |--------End Drawing or Taking Cards Functionality-----|

	def drawCards(self, deck, amount):
		for i in range(amount):
			self.drawCard(deck)

	def resetHand(self):
		self.hand = []


 	##########################
 	# Go Fish specific methods
 	##########################




