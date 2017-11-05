import os
import sys

import unittest

sys.path.append('../../Modules/Players/')
sys.path.append('../../Modules/Cards/')

from HumanPlayer import HumanPlayer
from Bot import Bot

from Deck import Deck

class PlayerTests(unittest.TestCase):

	def setUp(self):
		self.player_1 = False
		self.player_2 = False
		self.deck = False

	def test_human_player_is_not_bot(self):
		self.player_1 = HumanPlayer()
		self.player_2 = Bot

		self.assertFalse(isinstance(self.player_1, self.player_2))

	def test_two_diff_not_equal(self):
		self.player_1 = HumanPlayer("Jeffery")
		self.player_2 = HumanPlayer("Robert")
		self.assertNotEqual(self.player_1, self.player_2)

	def test_two_diff_same_name_not_equal(self):
		self.player_1 = HumanPlayer("Jeffery")
		self.player_2 = HumanPlayer("Jeffery")
		self.assertNotEqual(self.player_1, self.player_2)

	def test_draw_hand(self):
		self.deck = Deck()
		self.deck.initialize()

		self.player_1 = HumanPlayer()

		# Make sure the deck is 52 cards (one full deck)
		self.assertIs(self.deck.currentAmount(), 52)

		# Player draws a full hand from the deck
		self.player_1.drawHand(self.deck)

		# Make sure after drawing that the deck takes 7
		# 	cards away from its full total
		self.assertIs(self.deck.currentAmount(), 45)

		# Assert that the player actually has a hand
		self.assertIsNot(self.player_1.getHand(), []) 

		# At least for Go Fish, the hand should be 7
		# 	cards big when the player is starting out
		self.assertIs(self.player_1.countHand(), 7)

	def tearDown(self):
		self.player_1 = False
		self.player_2 = False
		self.deck = False

class BotTests(unittest.TestCase):
	def setUp(self):
		self.player_1 = False
		self.player_2 = False

	def test_if_player_class(self):
		self.player_1 = HumanPlayer
		self.player_2 = Bot()

		self.assertTrue(isinstance(self.player_2, self.player_1))

	def test_type_difference(self):
		self.player_1 = HumanPlayer()
		self.player_2 = Bot()

		self.assertFalse(type(self.player_2) == 'HumanPlayer.HumanPlayer',
			"Player 1 type %s, Player 2 type %s")

	def test_two_diff_not_equal(self):
		self.player_1 = Bot("Jeffery")
		self.player_2 = Bot("Robert")
		self.assertNotEqual(self.player_1, self.player_2)

	def test_two_diff_same_name_not_equal(self):
		self.player_1 = Bot("Jeffery")
		self.player_2 = Bot("Jeffery")
		self.assertNotEqual(self.player_1, self.player_2)

	def tearDown(self):
		self.player_1 = False
		self.player_2 = False

if __name__ == '__main__':
	unittest.main(verbosity=2)