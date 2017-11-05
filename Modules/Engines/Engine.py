import sys

sys.path.append('../../Modules/Cards/')
sys.path.append('../../Modules/Players/')

from Deck import Deck
from Card import Card

class Engine(object):
	# Controls the start, turn, and checks of the actual game.
	def __init__(self, test = False):
		self.players = None
		self.deck = None
		self.playerIndex = 0
		self.variant = None
		self.test = test
		self.endGame = False


# All Engines will have this obtaining and setting deck functionality
	def getDeck(self):
		# Summary: Gives the deck object out.
		# Returns: `self.deck` - Deck Object
		return self.deck

	def setDeck(self):
		# Summary: Sets
		# Input: `new_deck` - The new value of the deck object I want to set to
		# Returns: Void
		self.deck = Deck()
		self.getDeck().initialize()

# All Engines will handle getting and setting current players with this functionality
	def getPlayers(self):
		return self.players

	def getPlayerAmount(self):
		return len(self.players)
		
	def setPlayers(self, players):
		self.players = players

	def removePlayer(self, player):
		players = self.getPlayers()
		players.remove(player)

	def _getPlayerIndex(self):
		return self.playerIndex

	def _addPlayerIndex(self):
		players = self.getPlayers()

		if (self._getPlayerIndex() + 1) == len(players):
			self.playerIndex = 0
		else:
			self.playerIndex += 1

	def getCurrentPlayer(self):
		return self.getPlayers()[self._getPlayerIndex()]

	def returnWinningPlayer(self):
		pL = self.getPlayers()
		max_tricks = 0
		max_player_array = None
		for p in pL:
			player_score = p.getTricks()
			if (max_tricks == player_score and (not player_score == 0)):
				max_player_array.append(p)
			elif (max_tricks < player_score):
				max_tricks = player_score
				max_player_array = []
				max_player_array.append(p)
		if len(max_player_array) == 1:
			return max_player_array[0]
		else:
			return max_player_array

# All Engines will have a game loop. Unsure if it will be set this way throughout
	def gameLoop(self):
		# Will stop when there is a player that has gotten the winning conditions of the game
		while not self.gameOver():
			# Getting the current player for the turn
			self.takeTurn()

		self.congratulations(self.returnWinningPlayer())

# All Engines will have a game that will end :)
	def gameOver(self):
		return self.endGame

	def toggleGameOver(self):
		self.endGame = (not self.endGame)


# All Engines, at end game, will congratulate players
	def congratulations(self, playerObj):
		from HumanPlayer import HumanPlayer

		winning_players = ""
		winning_trick_amount = None

		if isinstance(playerObj, HumanPlayer):
			winning_players = playerObj
			winning_trick_amount = playerObj.getTricks()
		elif type(playerObj) == list:
			playerAmt = len(playerObj)
			for i in range(playerObj):
				if i == (playerObj - 1):
					winning_players += playerObj[i]
					winning_trick_amount = playerObj[i].getTricks()
				else:
					winning_players += playerobj[i] + ", "
		else:
			raise Exception("What the hell are you putting in here, man? That ain't cool.")

		print """Congratulations %s, you have won the epic game of Go Fish with a trick count of %s. Make sure to tell all of your other friends (if you have any) that you won one of the most childish games in all the land!""" % (winning_players, winning_trick_amount)


	def gameStart(self):
		self.dealHands()
		return self.gameLoop()

	def initialize(self):
		self.setDeck()
		self.gameStart()