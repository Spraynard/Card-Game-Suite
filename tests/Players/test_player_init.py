import os
import sys

from Modules.Starters.GoFish.GoFishStarter import GoFishStarter
from Modules.Players.Player import Player
from Modules.Players.Bot import Bot


class TestPlayerInit:
    def test_init_player_names(self):
        starter = GoFishStarter()
        test_accept = [Player("George"), Bot()]

        f1 = sys.stdin
        f = open("tests/test_data/single_player_name.txt", "r")
        sys.stdin = f
        starter.initialize_go_fish()
        f.close()
        sys.stdin = f1

        game_players = starter.getPlayers()
        assert game_players == test_accept, "Player building is not working correctly.\
			 The current game players are...: %s" % game_players
