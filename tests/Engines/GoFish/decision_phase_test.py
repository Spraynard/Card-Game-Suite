import sys
import unittest

sys.path.append('../../../Modules/Players/')
sys.path.append('../../../Modules/Engines/')
sys.path.append('../../../Modules/Cards/')

from Bot import Bot
from HumanPlayer import HumanPlayer
from GoFishCard import GoFishCard as Card
from GoFish.TestGoFishEngine import TestGoFishEngine

def spawnExtraPlayers(playerType, amount, names = None):
	# Returns: Array with amount of players specified. Returns object if amount == 1
	if isinstance(playerType, Bot):
		# Spawn bots
		if amount == 1:
			return Bot()
		else:
			return [Bot() for i in range(amount)]

	else:
		# Spawn humans
		if amount == 1:
			return HumanPlayer().randomName()
		else:
			return [HumanPlayer().randomName() for i in range(amount)]

class DecisionPhaseEngineTests(unittest.TestCase):
	
	def setUp(self):
		self.humanPlayer = HumanPlayer().randomName()
		self.botPlayer = Bot()
		self.engine = TestGoFishEngine(True)

	def test_decision_phase_human_to_bot_pass(self):
		# Human to bot case
		test_card = Card("2", "Hearts")

		f1 = sys.stdin
		f = open('../../test_data/decision_phase/decision_phase_test_#1.txt', 'r')
		sys.stdin = f
		self.humanPlayer.hand.append(test_card)

		self.engine.setPlayers([self.humanPlayer, self.botPlayer])
		self.engine.initialize()

		self.assertIs(self.engine.getPlayerAmount(), 2)
		self.engine.decisionPhase(self.humanPlayer)
		
		f.close()
		sys.stdin = f1

		self.assertIs(self.humanPlayer.getChosenPlayer(), self.botPlayer)
		self.assertEqual(self.humanPlayer.getChosenCard(), test_card)

	def test_decision_phase_human_to_human_pass(self):
		test_card = Card("2", "Hearts")
		extraPlayer = spawnExtraPlayers(HumanPlayer(), 1)

		f1 = sys.stdin
		f = open('../../test_data/decision_phase/decision_phase_test_#2.txt', 'r')
		sys.stdin = f
		self.humanPlayer.hand.append(test_card)

		self.engine.setPlayers([self.humanPlayer, extraPlayer])
		self.engine.initialize()

		self.assertIs(self.engine.getPlayerAmount(), 2)
		self.engine.decisionPhase(self.humanPlayer)
		
		f.close()
		sys.stdin = f1

		self.assertIs(self.humanPlayer.getChosenPlayer(), extraPlayer)
		self.assertEqual(self.humanPlayer.getChosenCard(), test_card)

	def test_decision_phase_bot_to_bot_pass(self):
		test_card = Card("2", "Hearts")
		extraPlayer = spawnExtraPlayers(Bot(), 1)

		f1 = sys.stdin
		f = open('../../test_data/decision_phase/decision_phase_test_#3.txt', 'r')
		sys.stdin = f
		self.botPlayer.hand.append(test_card)

		self.engine.setPlayers([self.botPlayer, extraPlayer])
		self.engine.initialize()

		self.assertIs(self.engine.getPlayerAmount(), 2)
		self.engine.decisionPhase(self.botPlayer)
		
		f.close()
		sys.stdin = f1

		self.assertIs(self.botPlayer.getChosenPlayer(), extraPlayer)
		self.assertEqual(self.botPlayer.getChosenCard(), test_card)

	def test_decision_phase_bot_to_human_pass(self):
		test_card = Card("2", "Hearts")

		f1 = sys.stdin
		f = open('../../test_data/decision_phase/decision_phase_test_#3.txt', 'r')
		sys.stdin = f
		self.botPlayer.hand.append(test_card)

		self.engine.setPlayers([self.botPlayer, self.humanPlayer])
		self.engine.initialize()

		self.assertIs(self.engine.getPlayerAmount(), 2)
		self.engine.decisionPhase(self.botPlayer)
		
		f.close()
		sys.stdin = f1

		self.assertIs(self.botPlayer.getChosenPlayer(), self.humanPlayer)
		self.assertEqual(self.botPlayer.getChosenCard(), test_card)

# How can I do wrong inputs in the decision phase?
# 	Input a player choice # that is out of the bounds of the array (Player inputs 0 or > len(choiceList))
#	Input non valid card values (A card rank that is not applicable, say 11 or 12 (jack or queen))
	def test_decision_phase_fail_player_choice(self):
		acceptOutput = "Error: That is not one of the player choices"
		test_card = Card("2", "Hearts")		
		f1 = sys.stdin
		f = open('../../test_data/decision_phase/decision_phase_test_#4.txt', 'r')
		sys.stdin = f

		self.humanPlayer.hand.append(test_card)
		self.engine.setPlayers([self.humanPlayer, self.botPlayer])
		self.assertIs(self.engine.getPlayerAmount(), 2)
		self.engine.decisionPhase(self.humanPlayer)

		output = sys.stdout.getvalue().strip()

		# Error output when choice is 0
		givenErrorOutput1 = output.split('\n')[3]
		# Error output when choice is >= len(choiceList)
		givenErrorOutput2 = output.split('\n')[5]

		f.close()
		sys.stdin = f1

		self.assertEqual(givenErrorOutput1, acceptOutput)
		self.assertEqual(givenErrorOutput2, acceptOutput)


	def test_decision_phase_fail_card_choice(self):
		acceptOutput1 = "Error: That is not an acceptable card rank. Please choose again."
		acceptOutput2 = "Error: You don't even have any of those cards in your hand! Try again."
		test_card = Card("2", "Hearts")

		f1 = sys.stdin
		f = open('../../test_data/decision_phase/decision_phase_test_#5.txt', 'r')
		sys.stdin = f

		self.humanPlayer.hand.append(test_card)
		self.engine.setPlayers([self.humanPlayer, self.botPlayer])
		self.assertIs(self.engine.getPlayerAmount(), 2)
		self.engine.decisionPhase(self.humanPlayer)

		output = sys.stdout.getvalue().strip()

		# Error output when player asks for unacceptable card
		givenErrorOutput1 = output.split('\n')[3]
		# Error output when player asks for card that
		# 	is not even in their hand.
		givenErrorOutput2 = output.split('\n')[5]
		
		f.close()
		sys.stdin = f1

		self.assertEqual(givenErrorOutput1, acceptOutput1)
		self.assertEqual(givenErrorOutput2, acceptOutput2)

	def tearDown(self):
		self.humanPlayer = None
		self.botPlayer = None
		self.engine = None
		
if __name__ == '__main__':
	unittest.main(verbosity=2, buffer=True)