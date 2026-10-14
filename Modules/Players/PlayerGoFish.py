

# from card_game_suite_types import ActionsT
from typing import Self
from Modules.Cards.Card import Card
from Modules.Players.Actions.ActionsGoFish import ActionsGoFish
from Modules.Players.Player import Player


class PlayerGoFish(Player, ActionsGoFish):
    def give_to_player(self, other: Self) -> None:
        give_array: list[Card] = self.get_give_array()
        other.take_cards(give_array)
        self.reset_give_array()