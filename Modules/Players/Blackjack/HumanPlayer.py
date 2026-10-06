import sys

sys.path.append('../');

from Player import Player

class HumanPlayer(Player):
	def __init__(self, name):
		super(HumanPlayer, self).__init__()
		self.gameTotal = 0
		self.money = None

	def victory_statement(self):
		pass

	def defeat_statement(self):
		pass

	def talk(self, reason):
		pass

	def getGameTotal(self):
		return self.gameTotal

	def addGameTotal(self, value):
		self.gameTotal += value;

	def resetGameTotal(self):
		self.gameTotal = 0

	def getHandValue(self):
		

	def makeDecision(self):
		decisionsArray = [];

		if ( self.getGameTotal() < 21 ):
			decisionsArray.append('Hit')
		elif( self.get_hand().length < 3 and )


