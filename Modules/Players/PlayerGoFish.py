

# from card_game_suite_types import ActionsT
from typing import Self
from Modules.Cards.Card import Cards
from Modules.Players.Actions.ActionsGoFish import ActionsGoFish
from Modules.Players.Player import Player


class PlayerGoFish(Player, ActionsGoFish):
    def give(self, other: Self) -> None:
        """
        Gives cards to other players
        """
        give_array: Cards = self.get_give_array()
        other.take_cards(give_array)
        self.reset_give_array()