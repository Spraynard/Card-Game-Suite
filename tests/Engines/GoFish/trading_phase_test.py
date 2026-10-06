import sys
import unittest

from Modules.Players.Bot import Bot
from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Cards.Card import Card
from Modules.Cards.Deck import Deck
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


# Lets ask what the trading phase should do?:
# 	1. Based on the player and card selected from the decision phase, you should
#


def checkStringForBullshit(string):
    string = string.split(" ")
    for w in string:
        if w == "False":
            return True
    return False


class TestTradingPhase:
    def test_trading_phase_accept_single_card(self, human_player, bot_player, engine):
        # Steps:
        # 1. Player initialization
        # 	a. Set Chosen Player
        # 	b. Set Chosen Card
        # 	c. Initialize Chosen Player's hand with chosen card
        # 	d. run tests

        # The ole 5 of clubs :)

        ask_card = Card(5, "Clubs")
        human_player.setChosenPlayer(bot_player)
        human_player.setChosenCard(ask_card)
        bot_player.hand.append(ask_card)
        engine.tradingPhase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")
        output1 = split_output[0]
        output2 = split_output[1]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.getName(),
            bot_player,
            ask_card.getRank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.getName(), bot_player, ask_card.getRank())
        )

        assert (
            checkStringForBullshit(output2) == False
        ), "You got some bullshit in your output 2"
        assert len(bot_player.getGiveArray()) == 0, (
            "Bot Player's Give Array: %s" % bot_player.getGiveArray()
        )
        assert len(bot_player.getHand()) == 0, (
            "Bot Player's Hand %s" % bot_player.showHand()
        )

        assert len(human_player.getHand()) != 0, (
            "Human Player's hand %s" % human_player.showHand()
        )

    def test_trading_phase_accept_multiple_cards(
        self, human_player, bot_player, engine
    ):
        # The chosen player should have multiple of the `same` card.
        # 	I do not expect this to work right off the bat, but you know.
        ask_card = Card(5, "Hearts")
        bot_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]
        bot_player.takeRelevantCards(bot_card_array)

        human_player.setChosenPlayer(bot_player)
        human_player.setChosenCard(ask_card)
        engine.tradingPhase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")
        output1 = split_output[0]
        output2 = split_output[1]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.getName(),
            bot_player,
            ask_card.getRank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.getName(), bot_player, ask_card.getRank())
        )

        assert len(bot_player.getGiveArray()) == 0, (
            "Bot Player's Give Array: %s" % bot_player.getGiveArray()
        )
        assert bot_player.handCount() == 0, (
            "Bot Player's Hand %s" % bot_player.showHand()
        )

        assert (
            human_player.handCount() != 0
        ), "Human Player's hand is not empty, as it should be"

    def test_trading_phase_reject_no_cards(self, human_player, bot_player, engine):
        # Player should draw a card from the deck after this.
        # 	Don't forget to load up the engine with a deck.
        engine.setDeck()

        ask_card = Card(10, "Clubs")
        bot_hand_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]
        bot_player.takeRelevantCards(bot_hand_card_array)

        human_player.setChosenPlayer(bot_player)
        human_player.setChosenCard(ask_card)

        assert human_player.handCount() == 0

        engine.tradingPhase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")
        output1 = split_output[0]
        output2 = split_output[1]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.getName(),
            bot_player,
            ask_card.getRank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.getName(), bot_player, ask_card.getRank())
        )

        assert human_player.handCount() == 1
        assert bot_player.handCount() == 3

    def test_trading_phase_reject_player_loss(self, human_player, bot_player, engine):

        engine.deck = Deck()
        engine.setPlayers([human_player, bot_player])

        assert human_player in engine.getPlayers()

        ask_card = Card(10, "Clubs")

        bot_hand_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]

        bot_player.takeRelevantCards(bot_hand_card_array)

        human_player.setChosenPlayer(bot_player)

        human_player.setChosenCard(ask_card)

        assert human_player.handCount() == 0

        engine.tradingPhase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")

        output1 = split_output[0]
        output2 = split_output[1]
        output3 = split_output[2]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.getName(),
            bot_player,
            ask_card.getRank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.getName(), bot_player, ask_card.getRank())
        )

        acceptOutput3 = (
            "Hey everyone, laugh at %s! They got kicked out of the game for losing!"
            % human_player
        )
        assert output3 == acceptOutput3

        assert not human_player in engine.getPlayers()
