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


def spawnExtraPlayers(playerType, amount, names=None):
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
            return HumanPlayer().random_name()
        else:
            return [HumanPlayer().random_name() for i in range(amount)]


class TestDecisionPhaseEngine:

    def test_decision_phase_human_to_bot_pass(self, human_player, bot_player, engine):
        # Human to bot case
        test_card = Card("2", None)

        f1 = sys.stdin
        f = open("tests/test_data/decision_phase/decision_phase_test_#1.txt", "r")
        sys.stdin = f
        human_player.hand.append(test_card)

        engine.setPlayers([human_player, bot_player])
        engine.initialize()

        assert engine.getPlayerAmount() == 2
        engine.decisionPhase(human_player)

        f.close()
        sys.stdin = f1

        assert human_player.getChosenPlayer() is bot_player
        assert human_player.getChosenCard() == test_card

    def test_decision_phase_human_to_human_pass(self, human_player, bot_player, engine):
        test_card = Card("2", None)
        extraPlayer = spawnExtraPlayers(HumanPlayer(), 1)

        f1 = sys.stdin
        f = open("tests/test_data/decision_phase/decision_phase_test_#2.txt", "r")
        sys.stdin = f
        human_player.hand.append(test_card)

        engine.setPlayers([human_player, extraPlayer])
        engine.initialize()

        assert engine.getPlayerAmount() == 2
        engine.decisionPhase(human_player)

        f.close()
        sys.stdin = f1

        assert human_player.getChosenPlayer() is extraPlayer
        assert human_player.getChosenCard() == test_card

    def test_decision_phase_bot_to_bot_pass(self, human_player, bot_player, engine):
        test_card = Card("2", None)
        extraPlayer = spawnExtraPlayers(Bot(), 1)

        f1 = sys.stdin
        f = open("tests/test_data/decision_phase/decision_phase_test_#3.txt", "r")
        sys.stdin = f
        bot_player.hand.append(test_card)

        engine.setPlayers([bot_player, extraPlayer])
        engine.initialize()

        assert engine.getPlayerAmount() == 2
        engine.decisionPhase(bot_player)

        f.close()
        sys.stdin = f1

        assert bot_player.getChosenPlayer() is extraPlayer
        assert bot_player.getChosenCard() == test_card

    def test_decision_phase_bot_to_human_pass(self, human_player, bot_player, engine):
        test_card = Card("2", "Hearts")

        f1 = sys.stdin
        f = open("tests/test_data/decision_phase/decision_phase_test_#3.txt", "r")
        sys.stdin = f
        bot_player.hand.append(test_card)

        engine.setPlayers([bot_player, human_player])
        engine.initialize()

        assert engine.getPlayerAmount() == 2
        engine.decisionPhase(bot_player)

        f.close()
        sys.stdin = f1

        assert bot_player.getChosenPlayer() is human_player
        assert bot_player.getChosenCard() == test_card

    # How can I do wrong inputs in the decision phase?
    # 	Input a player choice # that is out of the bounds of the array (Player inputs 0 or > len(choiceList))
    # 	Input non valid card values (A card rank that is not applicable, say 11 or 12 (jack or queen))
    def test_decision_phase_fail_player_choice(self, human_player, bot_player, engine):
        acceptOutput = "Error: That is not one of the player choices"
        test_card = Card("2", "Hearts")
        f1 = sys.stdin
        f = open("tests/test_data/decision_phase/decision_phase_test_#4.txt", "r")
        sys.stdin = f

        human_player.hand.append(test_card)
        engine.setPlayers([human_player, bot_player])
        assert engine.getPlayerAmount() == 2
        engine.decisionPhase(human_player)

        output = sys.stdout.getvalue().strip()

        # Error output when choice is 0
        givenErrorOutput1 = output.split("\n")[3]
        # Error output when choice is >= len(choiceList)
        givenErrorOutput2 = output.split("\n")[5]

        f.close()
        sys.stdin = f1

        assert givenErrorOutput1 == acceptOutput
        assert givenErrorOutput2 == acceptOutput

    def test_decision_phase_fail_card_choice(self, human_player, bot_player, engine):
        acceptOutput1 = (
            "Error: That is not an acceptable card rank. Please choose again."
        )
        acceptOutput2 = (
            "Error: You don't even have any of those cards in your hand! Try again."
        )
        test_card = Card("2", "Hearts")

        f1 = sys.stdin
        f = open("tests/test_data/decision_phase/decision_phase_test_#5.txt", "r")
        sys.stdin = f

        human_player.hand.append(test_card)
        engine.setPlayers([human_player, bot_player])
        assert engine.getPlayerAmount() == 2
        engine.decisionPhase(human_player)

        output = sys.stdout.getvalue().strip()

        # Error output when player asks for unacceptable card
        givenErrorOutput1 = output.split("\n")[3]
        # Error output when player asks for card that
        # 	is not even in their hand.
        givenErrorOutput2 = output.split("\n")[5]

        f.close()
        sys.stdin = f1

        assert givenErrorOutput1 == acceptOutput1
        assert givenErrorOutput2 == acceptOutput2
