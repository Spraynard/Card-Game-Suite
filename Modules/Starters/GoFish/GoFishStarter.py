#The Following code is a GoFish backend
#Rules:
# * Use 1 Deck of 52 Cards
# * Players are dealt seven random cards

# * Remaining cards make up the pool for users to Go Fish from

# * A turn consists of the current player selecting a card from their hand, and asking an opponent if they have any cards of the same rank
# * If the opponent has a card(s) of that rank, the opponent must give the card(s) to the player who requested it and that player gets another turn
# * If the opponent does not have any cards of that rank, the requesting player must Go Fish and draw a random card from the pool; ending that player's turn
# * As soon as a player collects a book of four cards of the same rank (ex. four Jacks or four 3s), they must lay their book down; removing the cards from their hand
# * If a player has no cards in their hand, they must draw from the pool; if the pool is empty, that player is out of the game
# * The game is over when all 13 sets of four, books, have been matched
# * The player with the most books is determined the winner
from random import shuffle as shuffle
from time import sleep as sleep

import sys

sys.path.append('../../../Modules/')
sys.path.append('../../../Modules/Cards/')
sys.path.append('../../../Modules/Players/')
sys.path.append('../../../Modules/Engines/')
sys.path.append('../../../Modules/Engines/GoFish/')

from Card import Card
from HumanPlayer import HumanPlayer
from Bot import Bot
from GoFishEngine import GoFishEngine

class GoFishStarter:
	def __init__(self, test = False):
		self.players = []
		self.engine = GoFishEngine()
		self.player_no = False
		self.test = test
		self.maxPlayers = 10
		self.humanPlayers = False

	# Code for addition of players and general player code
	def getPlayers(self):
		return self.players

	def getPlayerN(self):
		return self.player_no

	def getMaxPlayerN(self):
		return self.maxPlayers

	def getIfHumanPlayers(self):
		# Returns true if there are any human players in the game.
		# 	False if not.
		return self.humanPlayers

	def setIfHumanPlayers(self, boolean):
		# Setting the self.humanPlayers init variable.
		if not type(boolean) == bool:
			raise Exception("You are only supposed to put in a boolean indicating true if there is at least one human player, false if not.")
		self.humanPlayers == boolean

	def setPlayerN(self, n):
		self.player_no = n

	def askPlayerNames(self, player_n):
		names = False
		while not names and self.getIfHumanPlayers():
			name_flag = str(raw_input("Would you like to name yourselves (Y/N)?: ")).lower()
			# if not (name_flag == 'y') or not (name_flag == 'n'):
			# 	print "Please input 'y' or 'n'"
			# else:
			names = []
			if name_flag == 'y':
				print "Okay, please input the names for each player: "
				for i in range(player_n):
					i_name = raw_input("Player #%s: " % (i + 1))
					names.append(i_name)

					if (i == player_n - 1):
						break
			else:
				return


		return names

	def addPlayer(self, player):
		self.players.append(player)

	def addAllPlayers(self, player_n, bot_n):
		player_bucket = []
		player_names = self.askPlayerNames(player_n)

		for i in range(player_n):
			if player_names:
				player_bucket.append(HumanPlayer(player_names[i]))
			else:
				player_bucket.append(HumanPlayer())

		for i in range(bot_n):
			player_bucket.append(Bot().randomName())

		if not self.test:
			shuffle(player_bucket)

		for p in player_bucket:
			self.addPlayer(p)

	def askBotN(self):
		# Asks the players how many bots people want in their game.
		# 	Returns the number given.
		bot_n = False
		# The number to fill up the card table
		try:
			tot_bots = self.getMaxPlayerN() - self.getPlayerN()
		except:
			raise Exception("Error with getting the # of players")
		if tot_bots == 0:
			return False
		while True:
			try:
				t_bot_n = int(raw_input("Please enter the number of bots: "))
			except:
				print "Nope, need to enter a number between 1 and %s" % tot_bots
				continue
			if not t_bot_n:
				bot_n = 0
				break
			else:
				if t_bot_n > tot_bots:
					print "You can't have more than %s bots right now" % tot_bots
				else:
					bot_n = t_bot_n
					break
		return bot_n

	def askPlayerN(self):
		player_n = False
		
		while True:
			t_player_n = False
			try:
				t_player_n = int(raw_input("Please enter the number of human players: "))
			except:
				print "Nope need to enter a # between 0 and 4"
				continue
			if not t_player_n:
				print "Haha, you're playing an all bot game. That's pretty nice!"
				break
			else:
				if t_player_n > 10:
					print "You can't have more than ten players"
				else:
					# Limiting the amount of players to 1 right now
					# player_n = 1
					player_n = t_player_n
					self.setIfHumanPlayers(True)
					break
		return player_n

	def handlePlayerInit(self):
		# Returns: Void
		try:
			player_n = self.askPlayerN()
			self.setPlayerN(player_n)
			return self.getPlayerN()
		except:
			raise Exception("There is a problem in `handlePlayerInit()`")
	
	def handleBotInit(self):
		try:
			bot_n = self.askBotN()
			return bot_n
		except:
			raise Exception("There was an error initializing the bots")

	# End Code for Addition of Players

	def startGame(self):
		self.engine.setPlayers(self.getPlayers())
		self.engine.initialize()

	def initializeGoFish(self):
		if self.test:
			print "This is now in test mode"
			sleep(2)
		print "Welcome to another round of the famous game, Go Fish!"
		player_n = self.handlePlayerInit()
		bot_n = self.handleBotInit()
		self.addAllPlayers(player_n, bot_n)
		self.startGame()

if __name__ == "__main__":
	GoFishStarter().initializeGoFish()