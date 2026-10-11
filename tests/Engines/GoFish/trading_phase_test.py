import sys

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


class TestTradingPhase:
    def test_trading_phase_accept_single_card(self, human_player: HumanPlayer, bot_player: Bot, engine: DebugGoFishEngine):
        # Steps:
        # 1. Player initialization
        # 	a. Set Chosen Player
        # 	b. Set Chosen Card
        # 	c. Initialize Chosen Player's hand with chosen card
        # 	d. run tests

        # The ole 5 of clubs :)

        ask_card = Card(5, "Clubs")
        human_player.set_chosen_player(bot_player)
        human_player.set_chosen_card(ask_card)
        bot_player.hand.append(ask_card)
        engine.trading_phase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")
        output1 = split_output[0]
        output2 = split_output[1]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.get_name(),
            bot_player,
            ask_card.get_rank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.get_name(), bot_player, ask_card.get_rank())
        )

        assert len(bot_player.getGiveArray()) == 0, (
            "Bot Player's Give Array: %s" % bot_player.get_give_array()
        )
        
        assert len(bot_player.getHand()) == 0

        assert len(human_player.getHand()) != 0
    def test_trading_phase_accept_multiple_cards(self, human_player: HumanPlayer, bot_player: Bot, engine: DebugGoFishEngine):
        # The chosen player should have multiple of the `same` card.
        # 	I do not expect this to work right off the bat, but you know.
        ask_card = Card(5, "Hearts")
        bot_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]
        bot_player.take_relevant_cards(bot_card_array)

        human_player.set_chosen_player(bot_player)
        human_player.set_chosen_card(ask_card)
        engine.trading_phase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")
        output1 = split_output[0]
        output2 = split_output[1]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.get_name(),
            bot_player,
            ask_card.get_rank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.get_name(), bot_player, ask_card.get_rank())
        )

        assert len(bot_player.get_give_array()) == 0, (
            "Bot Player's Give Array: %s" % bot_player.get_give_array()
        )
        assert bot_player.hand_count() == 0

        assert human_player.hand_count() != 0

    def test_trading_phase_reject_no_cards(self, human_player: HumanPlayer, bot_player: Bot, engine: DebugGoFishEngine):
        # Player should draw a card from the deck after this.
        # 	Don't forget to load up the engine with a deck.
        engine.set_deck()

        ask_card = Card(10, "Clubs")
        bot_hand_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]
        bot_player.take_relevant_cards(bot_hand_card_array)

        human_player.set_chosen_player(bot_player)
        human_player.set_chosen_card(ask_card)

        assert human_player.hand_count() == 0

        engine.trading_phase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")
        output1 = split_output[0]
        output2 = split_output[1]

        acceptOutput1 = '%s: "Hey %s, Do you have any %ss?"' % (
            human_player.get_name(),
            bot_player,
            ask_card.get_rank(),
        )
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.get_name(), bot_player, ask_card.get_rank())
        )

        assert human_player.hand_count() == 1
        assert bot_player.hand_count() == 3

    def test_trading_phase_reject_player_loss(self, human_player: HumanPlayer, bot_player: Bot, engine: DebugGoFishEngine):

        engine.deck = Deck()
        engine.set_players([human_player, bot_player])

        assert human_player in engine.get_players()

        ask_card = Card(10, "Clubs")

        bot_hand_card_array = [Card(5, "Clubs"), Card(5, "Spades"), Card(5, "Diamonds")]

        bot_player.take_relevant_cards(bot_hand_card_array)

        human_player.set_chosen_player(bot_player)

        human_player.set_chosen_card(ask_card)

        assert human_player.hand_count() == 0

        engine.trading_phase(human_player)

        output = sys.stdout.getvalue().strip()
        split_output = output.split("\n")

        output1 = split_output[0]
        output2 = split_output[1]
        output3 = split_output[2]

        acceptOutput1 = f"{human_player.get_name}: \"Hey {bot_player}, Do you have any {ask_card.get_rank}\""
        
        assert output1 == acceptOutput1, (
            "Your output is not the same as what I am expecting\
												\nPlayer: %s\n\
												Chosen Player: %s\n\
												Chosen Card: %s" % (human_player.get_name(), bot_player, ask_card.get_rank())
        )

        acceptOutput3 = (
            "Hey everyone, laugh at %s! They got kicked out of the game for losing!"
            % human_player
        )
        assert output3 == acceptOutput3

        assert not human_player in engine.get_players()
