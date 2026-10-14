from Modules.Cards.Deck import Deck
from Modules.Players.Actions.CardActions import CardActions
from Modules.Players.Bot import Bot
from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Players.Player import Player
from Modules.Players.HumanPlayer import HumanPlayer
from Modules.Views.TerminalOutput import TerminalOutput

class Engine:
    # Controls the start, turn, and checks of the actual game.
    def __init__(self, test=False):
        self.players = None
        self.deck = None
        # Index of the current player
        self.player_index = 0
        self.variant = None
        self.test = test
        self.end_game = False

        # All Engines will have this obtaining and setting deck functionality

    def display_current_player_info(self, player: HumanPlayer):
        if isinstance(player, Bot):
            return
        player.display_tricks()
        TerminalOutput.hand(player)

    def get_deck(self) -> Deck:
        # Summary: Gives the deck object out.
        # Returns: `self.deck` - Deck Object
        return self.deck

    def set_deck(self):
        # Summary: Sets
        # Input: `new_deck` - The new value of the deck object I want to set to
        # Returns: Void
        self.deck = Deck()
        self.get_deck().initialize()

        # All Engines will handle getting and setting current players with this functionality

    def get_players(self) -> list[Player]:
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
            print("%s: %s" % (p, player.getHand()))
            # End Player Handling Functionality

    def _get_player_index(self):
        return self.player_index

    def add_player_index(self):
        players = self.get_players()

        if (self._get_player_index() + 1) == len(players):
            self.player_index = 0
        else:
            self.player_index += 1

    def get_current_player(self):
        try:
            return self.get_players()[self._get_player_index()]
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
        while not self.end_game:
            player = self.get_current_player()
            # Getting the current player for the turn
            self.take_turn(player)

        self.congratulations(self.return_winning_player())

    def congratulations(self, player_obj):

        winning_players = ""
        winning_trick_amount = None

        if isinstance(player_obj, HumanPlayer):
            winning_players = player_obj
            winning_trick_amount = player_obj.get_tricks()
        elif type(player_obj) == list:
            player_amt = len(player_obj)
            for i in range(player_obj):
                if i == (player_obj - 1):
                    winning_players += player_obj[i]
                    winning_trick_amount = player_obj[i].get_tricks()
                else:
                    winning_players += player_obj[i] + ", "
        else:
            raise Exception(
                "What the hell are you putting in here, man? That ain't cool."
            )

        print(
            """Congratulations %s, you have won the epic game of Go Fish with a trick count of %s. Make sure to tell all of your other friends (if you have any) that you won one of the most childish games in all the land!"""
            % (winning_players, winning_trick_amount)
        )

    def deal_hands(self):
        deck = self.get_deck()
        players: list[Player[CardActions]] = self.get_players()

        for player in players:
            player.actions.draw_cards(deck, self.game_start_deal_number_of_cards())

    def game_start_deal_number_of_cards(self):
        """Obtain the amount of cards each player should start with at the start of the game."""
        raise Exception("game_start_deal_number_of_cards not implemented")

    def game_start(self) -> None:
        """
        Start the game
        """
        self.deal_hands()
        return self.game_loop()

    def initialize(self):
        self.set_deck()
        self.game_start()
