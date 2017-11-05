import sys
import unittest

sys.path.append('../../../Modules/Players/')
sys.path.append('../../../Modules/Engines/')
sys.path.append('../../../Modules/Cards/')

from Bot import Bot
from HumanPlayer import HumanPlayer
from Card import Card
from GoFish.TestGoFishEngine import TestGoFishEngine

# Question: How can I test the end phase?
# 
# 	First, what does the end phase of the Go Fish program do? Steps listed below:
# 
# 		1. If Player was able to correctly guess a card in another player's hand:
# 			- Internal player class state relating to guesses is RESET.
# 			- Any tricks in the player's hand are taken out.
# 			- The same player is able to take another turn of the game if the game is not ended
# 			- If the game is ended we end that shit.
# 		
# 		2. If Player did not correctly guess a card in another player's hand:
# 			- Player sorts their hand; populating internal player sortDict in the process
# 			- Player then `looks for tricks` within the sort Dict (any grouping that has 4 cards)
# 			- Player then `sets the tricks`. Upticking internal player trick count, as well as
# 				the engine's master trick count.
# 			- Player index is upticked, causing the next player to be available for the next turn
# 
# 		3. Game ends if 13 tricks are made. 13 * 4 = 52 so that means that all cards are down on the table
# 			- The player with the most tricks wins the game!
#

def spawnDupCards(cardList, suitList):
	cardArray = []
	for card in cardList:
		for suit in suitList:
			cardArray.append(Card(card, suit))

	return cardArray

class EndPhaseEngineTests(unittest.TestCase):
	
	def setUp(self):
		self.humanPlayer = HumanPlayer().randomName()
		self.botPlayer = Bot()
		self.engine = TestGoFishEngine(True)

	# Insert Tests Here
	def testEndPhaseCorrect(self):
		# Set a player up with a correct guess, then test and see if that guess got reset.
		# 	This needs to happen before a player takes a turn
		self.humanPlayer.setGuess(True)

		self.engine.endPhase(self.humanPlayer)

		self.assertTrue(self.humanPlayer.gotGuess() == False)

	def testEndPhaseCorrectOneTrick(self):
		# Set a player up with a correct guess and a hand that contains one trick.
		hand = [
			Card("A", "Spades"),
			Card("A", "Hearts"),
			Card("A", "Diamonds"),
			Card("A", "Clubs")
		]

		self.humanPlayer.takeRelevantCards(hand)
		self.assertTrue(self.humanPlayer.countHand() == 4)
		self.humanPlayer.setGuess(True)
		self.assertTrue(self.humanPlayer.gotGuess() == True)

		self.engine.endPhase(self.humanPlayer)

		self.assertTrue(self.humanPlayer.gotGuess() == False)
		self.assertTrue(self.humanPlayer.countHand() == 0)
		self.assertTrue(self.humanPlayer.getTricks() == 1)
		print self.engine.getMasterTrickCount()
		self.assertTrue(self.engine.getMasterTrickCount() == 1)

	def testEndPhaseCorrectMultipleTricks(self):
		hand = spawnDupCards(["A", "J", "K", "Q"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		self.humanPlayer.takeRelevantCards(hand)
		self.assertTrue(self.humanPlayer.countHand() == 16)
		self.humanPlayer.setGuess(True)

		self.assertTrue(self.humanPlayer.gotGuess() == True)

		self.engine.endPhase(self.humanPlayer)

		self.assertTrue(self.humanPlayer.gotGuess() == False)
		self.assertTrue(self.humanPlayer.countHand() == 0)
		self.assertTrue(self.humanPlayer.getTricks() == 4)
		print self.engine.getMasterTrickCount()
		self.assertTrue(self.engine.getMasterTrickCount() == 4)

	def testEndPhaseCorrectEndGame(self):
		hand = spawnDupCards(["3"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		self.humanPlayer.takeRelevantCards(hand)
		self.assertTrue(self.humanPlayer.countHand() == 4)
		self.humanPlayer.setGuess(True)

		self.assertTrue(self.humanPlayer.gotGuess() == True)

		self.engine.trickCount = 12
		self.assertTrue(self.engine.getMasterTrickCount() == 12)
		self.engine.setPlayers([self.humanPlayer])


		self.engine.endGameLoop(self.humanPlayer)
		self.assertTrue(self.engine.getMasterTrickCount() == 13)
		self.assertTrue(self.engine.endGame == True)

		output = sys.stdout.getvalue().strip()


		winningPhrase = """Congratulations %s, you have won the epic game of Go Fish with a trick count of %s. Make sure to tell all of your other friends (if you have any) that you won one of the most childish games in all the land!""" % (self.humanPlayer, 1)
		self.assertEquals(output, winningPhrase)

	def testEndPhaseIncorrectNoTricks(self):
		self.humanPlayer.takeRelevantCards([Card("A", "Spades")])
		self.engine.setPlayers([self.humanPlayer, self.botPlayer])
		self.assertTrue(self.engine.getPlayerAmount() == 2)
		self.assertTrue(self.engine._getPlayerIndex() == 0)
		self.engine.endPhase(self.humanPlayer)
		self.assertTrue(self.engine._getPlayerIndex() == 1)


	def testEndPhaseIncorrectOneTrick(self):
		hand = [
			Card("A", "Spades"),
			Card("A", "Hearts"),
			Card("A", "Diamonds"),
			Card("A", "Clubs")
		]

		self.humanPlayer.takeRelevantCards(hand)
		self.engine.setPlayers([self.humanPlayer, self.botPlayer])
		self.assertTrue(self.humanPlayer.countHand() == 4)
		self.assertTrue(not self.humanPlayer.gotGuess())

		self.engine.endPhase(self.humanPlayer)

		self.assertTrue(not self.humanPlayer.gotGuess())
		self.assertTrue(self.humanPlayer.countHand() == 0)
		self.assertTrue(self.humanPlayer.getTricks() == 1)
		print self.engine.getMasterTrickCount()
		self.assertTrue(self.engine.getMasterTrickCount() == 1)

	def testEndPhaseIncorrectMultipleTricks(self):
		hand = spawnDupCards(["A", "J", "K", "Q"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		self.humanPlayer.takeRelevantCards(hand)
		self.engine.setPlayers([self.humanPlayer, self.botPlayer])
		self.assertTrue(self.humanPlayer.countHand() == 16)
		self.assertTrue(not self.humanPlayer.gotGuess())

		self.engine.endPhase(self.humanPlayer)

		self.assertTrue(not self.humanPlayer.gotGuess())
		self.assertTrue(self.humanPlayer.countHand() == 0)
		self.assertTrue(self.humanPlayer.getTricks() == 4)
		print self.engine.getMasterTrickCount()
		self.assertTrue(self.engine.getMasterTrickCount() == 4)

	def testEndPhaseIncorrectEndGame(self):
		hand = spawnDupCards(["3"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		self.humanPlayer.takeRelevantCards(hand)
		self.assertTrue(self.humanPlayer.countHand() == 4)

		self.assertTrue(not self.humanPlayer.gotGuess())

		self.engine.trickCount = 12
		self.assertTrue(self.engine.getMasterTrickCount() == 12)
		self.engine.setPlayers([self.humanPlayer])


		self.engine.endGameLoop(self.humanPlayer)
		self.assertTrue(self.engine.getMasterTrickCount() == 13)
		self.assertTrue(self.engine.endGame == True)

		output = sys.stdout.getvalue().strip()


		winningPhrase = """Congratulations %s, you have won the epic game of Go Fish with a trick count of %s. Make sure to tell all of your other friends (if you have any) that you won one of the most childish games in all the land!""" % (self.humanPlayer, 1)
		self.assertEquals(output, winningPhrase)

	
	def tearDown(self):
		self.humanPlayer = None
		self.botPlayer = None
		self.engine = None

if __name__ == '__main__':
	unittest.main(verbosity = 2, buffer = True)