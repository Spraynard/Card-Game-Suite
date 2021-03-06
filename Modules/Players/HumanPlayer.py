import sys
import random

from Player import Player

class HumanPlayer(Player):
	"""Player object, All the commands that the player will use in the game are here."""
	def __init__(self, name = None):
		super(HumanPlayer, self).__init__()

		self.tricks = 0
		# Internal Player's Responses to questions posed by engine
		self.guess = None
		self.chosenPlayer = None
		self.chosenCard = None

		# Array used to give cards to other players
		self.giveArray = []
		self.sortingDict = {}
		self.trickHolder = []

	# |-------------Talking (Printed Statements)-----------------------------|
	# These statements will be used during the trading phase. Something to look at to
	# 	expand, definitely.
	def randomName(self):
		# Returns a `Player` with a random name from the Faker lib
		#	can get some pretty funny names :)
		from faker import Faker
		fake = Faker()

		return HumanPlayer(fake.name())

	def victoryStatement(self):
		statementDict = {
			1 : "\"I sure do not!\"",
		}
		print statementDict[random.choice(statementDict.keys())]

	def defeatStatement(self):
		statementDict = {
			1 : "%s: \"I do have %s cards. Here they are\": %s",
		}
		print statementDict[random.choice(statementDict.keys())] % (self.getName(), len(self.getGiveArray()), self.getGiveArray())

	def askOtherPlayer(self):
		statementDict = {
			1 : "%s: \"Hey %s, Do you have any %ss?\"",
		}
		print statementDict[random.choice(statementDict.keys())] % (self.getName(), self.getChosenPlayer(), self.getChosenCard().getRank())

	def exclaim(self):
		if len(self.getGiveArray()) == 1:
			statementDict = {
				1 : "%s: \"Dammit, I have %s card of that rank. Here it is: %s\"",
				2 : "%s: \"Wow, you're really good at this! I have %s card of that rank. Here it is you scallywag: %s\"",
				3 : "%s: \"Are you cheating? I have %s card of that rank. Take it ya dingus!: %s\""
			}
		else:
			statementDict = {
				1 : "%s: \"Dammit, I have %s cards of that rank. Here's your damn cards: %s\"",
				2 : "%s: \"Wow, you're really good at this! I have %s cards of that rank. Here they are you scallywag: %s\"",
				3 : "%s: \"Are you cheating? I have %s cards of that rank. Take em ya dingus! %s\""
			}
		print statementDict[random.choice(statementDict.keys())] % (self.getName(), len(self.getGiveArray()), self.getGiveArray())

	def talk(self, reason):
		reasonDict = {
			'victory' : self.victoryStatement,
			'defeat' : self.defeatStatement,
			'exclaim' : self.exclaim,
			'ask' : self.askOtherPlayer,
		}

		reasonDict[reason]()
	# |-------------Player to Player Interaction Functionality---------------|

	def getChosenPlayer(self):
		return self.chosenPlayer

	def setChosenPlayer(self, player):
		self.chosenPlayer = player

	def getChosenCard(self):
		return self.chosenCard

	def setChosenCard(self, card):
		self.chosenCard = card

	def resetChosenVariables(self):
		self.chosenPlayer = False
		self.chosenCard = False

	# |_____________End Player to Player Interaction Functionality-----------|
	# Guess Functionalty

	def setGuess(self, boolean):
		if not type(boolean) == bool:
			raise Exception("You have to set a boolean value (True/False)")
		self.guess = boolean

	def gotGuess(self):
		return self.guess

	def resetGuess(self):
		self.setGuess(False)

	def guessedCorrectly(self):
		self.setGuess(True)

	# End Guess Functionality

	# Trick functionality

	def addPlayerTrick(self):
		self.tricks += 1

	def addTotalTrick(self, trickRef):
		trickRef += 1

	def getTricks(self):
		return self.tricks

	def hasTricks(self):
		return not (self.getTricks == 0)

	def getTrickHolder(self):
		return self.trickHolder

	def addTrickHolder (self, trick):
		self.getTrickHolder().append(trick)

	def resetTrickHolder(self):
		self.trickHolder = []

	def displayTricks(self):
		if self.hasTricks():
			trick_n = self.getTricks()
			if trick_n == 1:
				print "You currently have %s trick" % trick_n
			else:
				print "You currently have %s tricks" % trick_n
		else:
			print "You currently have 0 tricks"

	def delTrickFromHand(self, trick):
		hand = self.getHand()
		for c in trick:
			hand.remove(c)

	def lookForTricks(self):
		sD = self.getSortingDict()

		for g in sD.values():
			if len(g) == 4:
				self.addTrickHolder(g)

	def setTricks(self):
		tH = self.getTrickHolder()
		tricks_added = 0
		while not len(tH) == 0:
			self.addPlayerTrick()
			t = tH.pop()
			self.delTrickFromHand(t)
			tricks_added += 1
		# Have to reset the sorting dict here or we're fucked
		self.resetSortingDict()
		return tricks_added

	# End Trick Functionality

	# NEEDS ATTENTION - OCTOBER 17th, 2017
	def getSortingDict(self):
		return self.sortingDict

	def resetSortingDict(self):
		self.sortingDict = {}

	def populateSortingDict(self):
		sortingDict = self.getSortingDict()
		hand = self.getHand()
		if self.handCount() == 0:
			return
		for c in self.getHand():
			cardRank = c.getRank()
			if not cardRank in sortingDict:
				sortingDict[cardRank] = []
			sortingDict[cardRank].append(c)

	def formatCardsBySortingDict(self):
		sD = self.getSortingDict()
		handHolder = []
		for g in sD.values():
			handHolder += g
		self.setHand(handHolder)

	def sortHand(self):
		# Go through the hand. Will group similar cards within
		# 	sortingDict and then group them. Sorting dict may be used
		# 	to find out if a group can become a trick. I don't know
		self.populateSortingDict()
		self.formatCardsBySortingDict()

	# End Player Hand Functionality

	# Code for player specific TRADING PHASE operations
	def hasCard(self, flagCard):
		# Non variant version of hasCard.
		# This version just plain checks to see if the player has
		# 	any cards of given rank in their hands.
		hand = self.getHand()
		flagCardRank = flagCard.getRank()
		rank_hand = []
		for c in hand:
			rank_hand.append(c.getRank())
		return flagCardRank in rank_hand

	# self.giveArray Helpers
	def getGiveArray(self):
		return self.giveArray

	def addGiveArray(self, card):
		self.giveArray.append(card)

	def resetGiveArray(self):
		self.giveArray = []

	def removeCard(self, card):
		self.hand.remove(card)

	def removeRelevantCards(self):
		giveArray = self.getGiveArray()
		for c in giveArray:
			self.removeCard(c)

	def populateGiveArray(self, chosenCard):
		# Giving cards means finding the cards of the specific rank
		# 	in the hand, taking them out of the hand,
		# 	and putting them in the give array, which
		# 	removes said cards from hand.
		hand = self.getHand()
		for c in hand:
			if c.isSameRank(chosenCard):
				# Appending it to the array of cards you're going to give
				self.addGiveArray(c)
		# Removing it from the player's hand
		self.removeRelevantCards()

	# Player => Player Card Interaction
	def giveToPlayer(self, other):
		other.takeRelevantCards(self.getGiveArray())
		self.resetGiveArray()

	def concedeDefeat(self, chosenCard):
		self.populateGiveArray(chosenCard)



	# End TRADING PHASE operation code