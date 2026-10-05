import sys

from Modules.Players.Bot import Bot
from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Cards.Card import Card
from Modules.Engines.GoFish.DebugGoFishEngine import DebugGoFishEngine

import pytest

@pytest.fixture
def human_player():
    return HumanPlayer()

@pytest.fixture
def bot_player():
    return Bot()

@pytest.fixture
def engine():
    return DebugGoFishEngine(True)

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

class TestEndPhase():	
	# Insert Tests Here
	def testEndPhaseCorrect(self, human_player, bot_player, engine):
		# Set a player up with a correct guess, then test and see if that guess got reset.
		# 	This needs to happen before a player takes a turn
		human_player.setGuess(True)

		engine.endPhase(human_player)

		assert human_player.gotGuess() == False

	def testEndPhaseCorrectOneTrick(self, human_player, bot_player, engine):
		# Set a player up with a correct guess and a hand that contains one trick.
		hand = [
			Card("A", "Spades"),
			Card("A", "Hearts"),
			Card("A", "Diamonds"),
			Card("A", "Clubs")
		]

		human_player.takeRelevantCards(hand)
		assert human_player.handCount() == 4
		human_player.setGuess(True)
		assert human_player.gotGuess() == True

		engine.endPhase(human_player)

		assert human_player.gotGuess() == False
		assert human_player.handCount() == 0
		assert human_player.getTricks() == 1
		assert engine.getMasterTrickCount() == 1

	def testEndPhaseCorrectMultipleTricks(self, human_player, bot_player, engine):
		hand = spawnDupCards(["A", "J", "K", "Q"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		human_player.takeRelevantCards(hand)
		assert human_player.handCount() == 16
		human_player.setGuess(True)

		assert human_player.gotGuess() == True

		engine.endPhase(human_player)

		assert human_player.gotGuess() == False
		assert human_player.handCount() == 0
		assert human_player.getTricks() == 4
		assert engine.getMasterTrickCount() == 4

	def testEndPhaseCorrectEndGame(self, human_player, bot_player, engine):
		hand = spawnDupCards(["3"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		human_player.takeRelevantCards(hand)
		assert human_player.handCount() == 4
		human_player.setGuess(True)

		assert human_player.gotGuess() == True

		engine.trickCount = 12
		assert engine.getMasterTrickCount() == 12
		engine.setPlayers([human_player])


		engine.endGameLoop(human_player)
		assert engine.getMasterTrickCount() == 13
		assert engine.endGame == True

		output = sys.stdout.getvalue().strip()


		winningPhrase = """Congratulations %s, you have won the epic game of Go Fish with a trick count of %s. Make sure to tell all of your other friends (if you have any) that you won one of the most childish games in all the land!""" % (human_player, 1)
		self.assertEquals(output, winningPhrase)

	def testEndPhaseIncorrectNoTricks(self, human_player, bot_player, engine):
		human_player.takeRelevantCards([Card("A", "Spades")])
		engine.setPlayers([human_player, bot_player])
		assert engine.getPlayerAmount() == 2
		assert engine._getPlayerIndex() == 0
		engine.endPhase(human_player)
		assert engine._getPlayerIndex() == 1


	def testEndPhaseIncorrectOneTrick(self, human_player, bot_player, engine):
		hand = [
			Card("A", "Spades"),
			Card("A", "Hearts"),
			Card("A", "Diamonds"),
			Card("A", "Clubs")
		]

		human_player.takeRelevantCards(hand)
		engine.setPlayers([human_player, bot_player])
		assert human_player.handCount() == 4
		assert not human_player.gotGuess()

		engine.endPhase(human_player)

		assert not human_player.gotGuess()
		assert human_player.handCount() == 0
		assert human_player.getTricks() == 1
		assert engine.getMasterTrickCount() == 1

	def testEndPhaseIncorrectMultipleTricks(self, human_player, bot_player, engine):
		hand = spawnDupCards(["A", "J", "K", "Q"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		human_player.takeRelevantCards(hand)
		engine.setPlayers([human_player, bot_player])
		assert human_player.handCount() == 16
		assert not human_player.gotGuess()

		engine.endPhase(human_player)

		assert not human_player.gotGuess()
		assert human_player.handCount() == 0
		assert human_player.getTricks() == 4
		assert engine.getMasterTrickCount() == 4

	def testEndPhaseIncorrectEndGame(self, human_player, bot_player, engine):
		hand = spawnDupCards(["3"], ["Diamonds", "Spades", "Hearts", "Clubs"])
		human_player.takeRelevantCards(hand)
		assert human_player.handCount() == 4

		assert not human_player.gotGuess()

		engine.trickCount = 12
		assert engine.getMasterTrickCount() == 12
		engine.setPlayers([human_player])


		engine.endGameLoop(human_player)
		assert engine.getMasterTrickCount() == 13
		assert engine.endGame == True

		output = sys.stdout.getvalue().strip()


		winningPhrase = """Congratulations %s, you have won the epic game of Go Fish with a trick count of %s. Make sure to tell all of your other friends (if you have any) that you won one of the most childish games in all the land!""" % (human_player, 1)
		self.assertEquals(output, winningPhrase)

	
