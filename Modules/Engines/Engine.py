from Modules.Cards.Deck import Deck
from Modules.Cards.Card import Card
from Modules.Players.HumanPlayer import HumanPlayer


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

    def get_players(self):
        return self.players

    def get_player_amount(self):
        return len(self.players)

    def set_players(self, players):
        self.players = players

    def remove_player(self, player):
        players = self.get_players()
        players.remove(player)

    def list_players_hands(self):
        players = self.get_players()

        for p in players:
            print("%s: %s" % (p, player.getHand()))
            # End Player Handling Functionality

    def _getPlayerIndex(self):
        return self.player_index

    def _addPlayerIndex(self):
        players = self.get_players()

        if (self._getPlayerIndex() + 1) == len(players):
            self.player_index = 0
        else:
            self.player_index += 1

    def get_current_player(self):
        return self.get_players()[self._getPlayerIndex()]

    def return_winning_player(self):
        p_l = self.get_players()
        max_tricks = 0
        max_player_array = None
        for p in p_l:
            player_score = p.get_tricks()
            if max_tricks == player_score and (not player_score == 0):
                max_player_array.append(p)
            elif max_tricks < player_score:
                max_tricks = player_score
                max_player_array = []
                max_player_array.append(p)
        if len(max_player_array) == 1:
            return max_player_array[0]
        else:
            return max_player_array

            # All Engines will have a game loop. Unsure if it will be set this way throughout

    def game_loop(self):
        # Will stop when there is a player that has gotten the winning conditions of the game
        while not self.game_over():
            # Getting the current player for the turn
            self.take_turn()

        self.congratulations(self.return_winning_player())

        # All Engines will have a game that will end :)

    def game_over(self):
        return self.end_game

    def toggle_game_over(self):
        self.end_game = not self.end_game

        # All Engines, at end game, will congratulate players

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
                    winning_players += playerobj[i] + ", "
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
        players = self.get_players()

        for p in players:
            p.drawCards(deck, self.game_start_deal_number_of_cards())

    def game_start_deal_number_of_cards(self):
        """Obtain the amount of cards each player should start with at the start of the game."""
        raise Exception("game_start_deal_number_of_cards not implemented")

    def game_start(self):
        """
        Start the game
        """
        self.deal_hands()
        return self.game_loop()

    def initialize(self):
        self.set_deck()
        self.game_start()
