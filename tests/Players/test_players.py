import os
import sys
import inspect

from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Players.Bot import Bot

from Modules.Cards.Deck import Deck
class TestPlayer():
    def test_player_1_is_not_bot(self):
        player_1 = HumanPlayer
        player_2 = Bot

        assert not isinstance(player_1, player_2)

    def test_two_diff_not_equal(self):
        player_1 = HumanPlayer("Jeffery")
        player_2 = HumanPlayer("Robert")
        assert player_1 !=  player_2

    def test_two_diff_same_name_not_equal(self):
        player_1 = HumanPlayer("Jeffery")
        player_2 = HumanPlayer("Jeffery")
        assert player_1 != player_2

    def test_draw_hand(self):
        deck = Deck()
        deck.initialize()

        player_1 = HumanPlayer()

        # Make sure the deck is 52 cards (one full deck)
        assert deck.currentAmount() == 52

        # Player draws a full seven card hand from the deck
        player_1.draw_cards(deck, 7)

        # Make sure after drawing that the deck takes 7
        # 	cards away from its full total
        assert deck.currentAmount() == 45

        # Assert that the player actually has a hand
        assert player_1.hand_count() > 0

        # At least for Go Fish, the hand should be 7
        # 	cards big when the player is starting out
        assert player_1.hand_count() == 7

class TestBot():
    def test_if_player_class(self):
        player_1 = HumanPlayer
        player_2 = Bot()

        assert isinstance(player_2, player_1)

    def test_type_difference(self):
        player_1 = HumanPlayer()
        player_2 = Bot()

        assert type(player_2) != "HumanPlayer.HumanPlayer","Player 1 type %s, Player 2 type %s"

    def test_two_diff_not_equal(self):
        player_1 = Bot("Jeffery")
        player_2 = Bot("Robert")
        assert player_1 != player_2

    def test_two_diff_same_name_not_equal(self):
        player_1 = Bot("Jeffery")
        player_2 = Bot("Jeffery")
        assert player_1 != player_2
