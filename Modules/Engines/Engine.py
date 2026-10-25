from Modules.Cards.Deck import Deck
from Modules.Players.Actions.ActionsCard import ActionsCard
from Modules.Players.Bot import Bot
from Modules.Players.Dealer import Dealer
from Modules.Players.Player import Player, Players
from Modules.Views.TerminalOutput import TerminalOutput

class Engine:
    dealer = Dealer()
    deck = Deck()
    end_game: bool = False
    players: Players = []
    player_index: int = 0

    def __init__(self):
        self.deck.shuffle()

    def card_deal_amount(self):
        raise Exception("card_deal_amount not implemented")

    def display_current_player_info(self, player: Player):
        raise Exception("Not Implemented -- display_current_player_info")

    def get_players(self) -> Players:
        return self.players

    def get_player_amount(self) -> int:
        return len(self.players)

    def set_players(self, players):
        self.players = players

    def remove_player(self, player):
        players = self.get_players()
        players.remove(player)

    def list_players_hands(self):
        players = self.get_players()

        for player in players:
            print("%s: %s" % (player, player.getHand()))
            # End Player Handling Functionality

    def add_player_index(self):
        players = self.get_players()

        if (self.player_index() + 1) == len(players):
            self.player_index = 0
        else:
            self.player_index += 1

    def get_current_player(self):
        player_index = self.player_index
        players = self.players
        try:
            return players[player_index]
        except IndexError:
            print("Error: List Index Out of Range")

    def return_winning_player(self):
        player_list = self.get_players()
        max_tricks = 0
        max_player_array = None
        for player in player_list:
            player_score = player.get_tricks()
            if max_tricks == player_score and (not player_score == 0):
                max_player_array.append(player)
            elif max_tricks < player_score:
                max_tricks = player_score
                max_player_array = []
                max_player_array.append(player)
        if len(max_player_array) == 1:
            return max_player_array[0]
        else:
            return max_player_array

            # All Engines will have a game loop. Unsure if it will be set this way throughout
    def take_turn(self, player: Player) -> None:
        """
        General abstraction over one turn of the card game

        Arguments:
        player - Player that is taking the turn
        """
        raise Exception("take_turn -- Not Implemented")
    
    def game_loop(self) -> None:
        """
        This is the main game loop. Every run tests if the game 
        is 'over'
        """
        raise Exception("Not Implemented -- game_loop")

    def deal_hands(self, players: Players, deck: Deck, amount: int):
        """
        Makes the dealer deal the hands.
        The dealer might be part of the game, but they also might not be
        """
        for player in players:
            self.dealer.deal(player, deck, amount)

    def start(self, players: Players) -> None:
        """
        Start the game with given players
        """
        self.players = players
        self.deal_hands(self.players, self.deck, self.card_deal_amount())
        return self.game_loop()
