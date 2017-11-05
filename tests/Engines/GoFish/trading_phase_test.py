import sys
import unittest

sys.path.append('../../../Modules/Players/')
sys.path.append('../../../Modules/Engines/')
sys.path.append('../../../Modules/Cards/')

from Bot import Bot
from HumanPlayer import HumanPlayer
from Card import Card
from GoFish.TestGoFishEngine import TestGoFishEngine

# Lets ask what the trading phase should do?:
# 	1. Based on the player and card selected from the decision phase, you should
#

def checkStringForBullshit(string):
	string = string.split(" ")
	for w in string:
		if w == "False":
			return True
	return False

class TradingPhaseEngineTests(unittest.TestCase):
	
	def setUp(self):
		self.humanPlayer = HumanPlayer().randomName()
		self.botPlayer = Bot()
		self.engine = TestGoFishEngine(True)

	def test_trading_phase_accept_single_card(self):
# Steps:
# 1. Player initialization 
# 	a. Set Chosen Player
#	b. Set Chosen Card
# 	c. Initialize Chosen Player's hand with chosen card
# 	d. run tests

		# The ole 5 of clubs :)

		ask_card = Card(5, "Clubs")
		self.humanPlayer.setChosenPlayer(self.botPlayer)
		self.humanPlayer.setChosenCard(ask_card)
		self.botPlayer.hand.append(ask_card)
		self.engine.tradingPhase(self.humanPlayer)

		output = sys.stdout.getvalue().strip()
		split_output = output.split('\n')
		output1 = split_output[0]
		output2 = split_output[1]

		acceptOutput1 = "%s: \"Hey %s, Do you have any %ss?\"" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank())
		self.assertTrue(output1 == acceptOutput1, "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank()))
		
		self.assertFalse(checkStringForBullshit(output2), "You got some bullshit in your output 2")
		self.assertTrue(len(self.botPlayer.getGiveArray()) == 0, "Bot Player's Give Array: %s" % self.botPlayer.getGiveArray())
		self.assertTrue(len(self.botPlayer.getHand()) == 0, "Bot Player's Hand %s" % self.botPlayer.showHand())

		self.assertFalse(len(self.humanPlayer.getHand()) == 0, "Human Player's hand %s" % self.humanPlayer.showHand())
	
	def test_trading_phase_accept_multiple_cards(self):
		# The chosen player should have multiple of the `same` card.
		# 	I do not expect this to work right off the bat, but you know.
		ask_card = Card(5, "Hearts")
		bot_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]
		self.botPlayer.takeRelevantCards(bot_card_array)

		self.humanPlayer.setChosenPlayer(self.botPlayer)
		self.humanPlayer.setChosenCard(ask_card)
		self.engine.tradingPhase(self.humanPlayer)

		output = sys.stdout.getvalue().strip()
		split_output = output.split('\n')
		output1 = split_output[0]
		output2 = split_output[1]

		acceptOutput1 = "%s: \"Hey %s, Do you have any %ss?\"" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank())
		self.assertTrue(output1 == acceptOutput1, "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank()))
		
		self.assertTrue(len(self.botPlayer.getGiveArray()) == 0, "Bot Player's Give Array: %s" % self.botPlayer.getGiveArray())
		self.assertTrue(self.botPlayer.countHand() == 0, "Bot Player's Hand %s" % self.botPlayer.showHand())
		
		self.assertFalse(self.humanPlayer.countHand() == 0, "Human Player's hand is not empty, as it should be")

	def test_trading_phase_reject_no_cards(self):
		# Player should draw a card from the deck after this.
		# 	Don't forget to load up the engine with a deck.
		self.engine.setDeck()

		ask_card = Card(10, "Clubs")
		bot_hand_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]
		self.botPlayer.takeRelevantCards(bot_hand_card_array)

		self.humanPlayer.setChosenPlayer(self.botPlayer)
		self.humanPlayer.setChosenCard(ask_card)

		self.assertTrue(self.humanPlayer.countHand() == 0)

		self.engine.tradingPhase(self.humanPlayer)

		output = sys.stdout.getvalue().strip()
		split_output = output.split('\n')
		output1 = split_output[0]
		output2 = split_output[1]

		acceptOutput1 = "%s: \"Hey %s, Do you have any %ss?\"" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank())
		self.assertTrue(output1 == acceptOutput1, "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank()))

		self.assertTrue(self.humanPlayer.countHand() == 1)
		self.assertTrue(self.botPlayer.countHand() == 3)

	def test_trading_phase_reject_player_loss(self):
		from Deck import Deck

		self.engine.deck = Deck()
		self.engine.setPlayers([self.humanPlayer, self.botPlayer])

		self.assertTrue(self.humanPlayer in self.engine.getPlayers())
		
		ask_card = Card(10, "Clubs")

		bot_hand_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]

		self.botPlayer.takeRelevantCards(bot_hand_card_array)

		self.humanPlayer.setChosenPlayer(self.botPlayer)

		self.humanPlayer.setChosenCard(ask_card)

		self.assertTrue(self.humanPlayer.countHand() == 0)

		self.engine.tradingPhase(self.humanPlayer)

		output = sys.stdout.getvalue().strip()
		split_output = output.split('\n')
		
		output1 = split_output[0]
		output2 = split_output[1]
		output3 = split_output[2]

		acceptOutput1 = "%s: \"Hey %s, Do you have any %ss?\"" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank())
		self.assertTrue(output1 == acceptOutput1, "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (self.humanPlayer.getName(), self.botPlayer, ask_card.getRank()))

		acceptOutput3 = "Hey everyone, laugh at %s! They got kicked out of the game for losing!" % self.humanPlayer
		self.assertTrue(output3 == acceptOutput3)

		self.assertTrue(not self.humanPlayer in self.engine.getPlayers())

	def tearDown(self):
		self.humanPlayer = None
		self.botPlayer = None
		self.engine = None
		
if __name__ == '__main__':
	unittest.main(verbosity = 2, buffer = True)