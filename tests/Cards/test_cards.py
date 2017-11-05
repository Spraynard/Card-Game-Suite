import os
import sys
import unittest

sys.path.append('../Modules/Cards/')

from Card import Card

class CardTests(unittest.TestCase):

	def setUp(self):
		self.card_1 = False
		self.card_2 = False

	def test_two_same_cards_equal(self):
		self.card_1 = Card(2, "Clubs")
		self.card_2 = Card(2, "Clubs")
		self.assertEqual(self.card_1, self.card_2)

	def test_two_different_cards_not_equal(self):
		self.card_1 = Card(2, "Clubs")
		self.card_2 = Card(2, "Spades")
		self.assertNotEqual(self.card_1, self.card_2)

	def tearDown(self):
		self.card_1 = False
		self.card_2 = False

if __name__ == '__main__':
	unittest.main(verbosity=2)