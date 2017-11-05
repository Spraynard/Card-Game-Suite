import sys
import unittest

sys.path.append('../../../Modules/Players/')
sys.path.append('../../../Modules/Engines/')
sys.path.append('../../../Modules/Cards/')

from Bot import Bot
from HumanPlayer import HumanPlayer
from GoFishCard import GoFishCard as Card
from GoFish.TestGoFishEngine import TestGoFishEngine

class InitialPhaseEngineTests(unittest.TestCase):
	
	def setUp(self):
		self.humanPlayer = HumanPlayer().randomName()
		self.botPlayer = Bot()
		self.engine = TestGoFishEngine(True)

	def test_initial_phase(self):
		# What is necessary for the initial phase to pass?
		# 1. Initially, since I am setting no tricks, the output must show that there are 0 tricks
		# 2. I will give a custom hand, but the output must
		self.engine.setPlayers([self.humanPlayer])
		self.engine.initialize()

		# Make sure only one player
		self.assertIs(self.engine.getPlayerAmount(), 1);
		# Want to get the first hand that could possibly be dealt.
		# 	this will be the hand that the player gets, supposedly
		acceptHand = self.engine.returnFirstHand()

		# Make sure I'm not actually drawing from the deck before the player draws
		self.assertIs(self.engine.getDeck().currentAmount(), 52)

		# These variables contain strings which will will be what
		# 	this test is looking to assert equality to
		acceptTrickOutput = "You currently have 0 tricks"
		acceptHandOutput = "%s" % acceptHand

		# Deal out the hands now
		self.engine.dealHands()

		# This goes through the initial phase of the engine
		self.engine.initialPhase(self.humanPlayer)

		# Full output
		output = sys.stdout.getvalue().strip()

		# Splitting the output is a nice parse to apply to
		# 	variables
		givenTrickOutput = output.split('\n')[0]
		givenHandOutput = output.split('\n')[1]

		self.assertEqual(givenTrickOutput, acceptTrickOutput)
		self.assertEqual(givenHandOutput, acceptHandOutput)

	def test_initial_phase_multiple_tricks(self):
		# Player is going to start out with 2 tricks on this initial phase test
		for i in range(2):
			self.humanPlayer.addPlayerTrick()

		self.engine.setPlayers([self.humanPlayer])
		self.engine.initialize()

		acceptTrickOutput = "You currently have 2 tricks"

		self.engine.dealHands()
		self.engine.initialPhase(self.humanPlayer)

		givenTrickOutput = sys.stdout.getvalue().strip().split('\n')[0]

		self.assertEqual(givenTrickOutput, acceptTrickOutput)

	def tearDown(self):
		self.humanPlayer = None
		self.botPlayer = None
		self.engine = None
		
if __name__ == '__main__':
	unittest.main(verbosity=2, buffer=True)