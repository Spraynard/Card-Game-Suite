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


class TestInitialPhase:
    def test_initial_phase(self, human_player, bot_player, engine):
        # What is necessary for the initial phase to pass?
        # 1. Initially, since I am setting no tricks, the output must show that there are 0 tricks
        # 2. I will give a custom hand, but the output must
        engine.setPlayers([human_player])
        engine.initialize()

        # Make sure only one player
        assert engine.getPlayerAmount() == 1
        # Want to get the first hand that could possibly be dealt.
        # 	this will be the hand that the player gets, supposedly
        acceptHand = engine.returnFirstHand()

        # Make sure I'm not actually drawing from the deck before the player draws
        assert engine.getDeck().currentAmount() == 52

        # These variables contain strings which will will be what
        # 	this test is looking to assert equality to
        acceptTrickOutput = "You currently have 0 tricks"
        acceptHandOutput = "%s" % acceptHand

        # Deal out the hands now
        engine.dealHands()

        # This goes through the initial phase of the engine
        engine.initialPhase(human_player)

        # Full output
        output = sys.stdout.getvalue().strip()

        # Splitting the output is a nice parse to apply to
        # 	variables
        givenTrickOutput = output.split("\n")[0]
        givenHandOutput = output.split("\n")[1]

        assert givenTrickOutput == acceptTrickOutput
        assert givenHandOutput == acceptHandOutput

    def test_initial_phase_multiple_tricks(self, human_player, bot_player, engine):
        # Player is going to start out with 2 tricks on this initial phase test
        for i in range(2):
            # Add a trick to a hand.
            human_player.addPlayerTrick()

        engine.setPlayers([human_player])
        engine.initialize()

        acceptTrickOutput = "You currently have 2 tricks"

        engine.dealHands()
        engine.initialPhase(human_player)

        givenTrickOutput = sys.stdout.getvalue().strip().split("\n")[0]

        assert givenTrickOutput == acceptTrickOutput
