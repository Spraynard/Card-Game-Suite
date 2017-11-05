import unittest

import os
import sys

sys.path.append('../') 
sys.path.append('../Modules/Players/')
sys.path.append('../Modules/Cards/')

from GoFishStarter import GoFishStarter
from Player import Player
from Bot import Bot

class PlayerInitTests(unittest.TestCase):
	def setUp(self):
		self.starter = GoFishStarter(True)
		self.assertEqual(self.starter.test, True,
			"This Go Fish game is not in test mode :<")

	def test_init_player_names(self):
		print "Testing if players can be added \n"
		test_accept = [Player("George"), Bot()]

		f1 = sys.stdin
		f = open('test_data/single_player_name.txt', 'r')
		sys.stdin = f
		self.starter.initializeGoFish()
		f.close()
		sys.stdin = f1

		game_players = self.starter.getPlayers()
		self.assertEqual(game_players, test_accept,
			"Player building is not working correctly.\
			 The current game players are...: %s" % game_players)

if __name__ == '__main__':
	unittest.main()


