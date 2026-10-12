import random

from Modules.Cards import Card

from .Player import Player
from faker import Faker


class HumanPlayer(Player):
    """Player object, All the commands that the player will use in the game are here."""

    def __init__(self, name=None):
        super().__init__(name)


        # |-------------Talking (Printed Statements)-----------------------------|
        # These statements will be used during the trading phase. Something to look at to
        # 	expand, definitely.

    def random_name(self):
        # Returns a `Player` with a random name from the Faker lib
        # 	can get some pretty funny names :)
        fake = Faker()
        return HumanPlayer(fake.name())

    def victory_statement(self):
        statement_dict = {
            1: '"I sure do not!"',
        }
        print(statement_dict[random.choice(list(statement_dict.keys()))])

    def defeat_statement(self):
        statement_dict = {
            1: '%s: "I do have %s cards. Here they are": %s',
        }
        print(
            statement_dict[random.choice(list(statement_dict.keys()))]
            % (self.get_name(), len(self.get_give_array()), self.get_give_array())
        )

    

    def talk(self, reason):
        reason_dict = {
            "victory": self.victory_statement,
            "defeat": self.defeat_statement,
            "exclaim": self.exclaim,
            "ask": self.ask_other_player,
        }

        reason_dict[reason]()

        # |-------------Player to Player Interaction Functionality---------------|

    def get_chosen_player(self):
        return self.chosen_player

    def set_chosen_player(self, player):
        self.chosen_player = player

    def get_chosen_card(self):
        return self.chosen_card

    def set_chosen_card(self, card):
        self.chosen_card = card

    def reset_chosen_variables(self):
        self.chosen_player = False
        self.chosen_card = False

        # |_____________End Player to Player Interaction Functionality-----------|
        # Guess Functionalty

    def set_guess(self, boolean):
        if not type(boolean) == bool:
            raise Exception("You have to set a boolean value (True/False)")
        self.guess = boolean

    def got_guess(self):
        return self.guess

    def reset_guess(self):
        self.set_guess(False)

    def guessed_correctly(self):
        self.set_guess(True)

    def display_tricks(self):
        if self.has_tricks():
            trick_n = self.get_tricks()
            if trick_n == 1:
                print("You currently have %s trick" % trick_n)
            else:
                print("You currently have %s tricks" % trick_n)
        else:
            print("You currently have 0 tricks")

    def del_trick_from_hand(self, trick):
        hand = self.get_hand()
        for c in trick:
            hand.remove(c)

    def look_for_tricks(self):
        s_d = self.get_sorting_dict()

        for g in s_d.values():
            if len(g) == 4:
                self.add_trick_holder(g)

    def set_tricks(self):
        t_h = self.get_trick_holder()
        tricks_added = 0
        while not len(t_h) == 0:
            self.add_player_trick()
            t = t_h.pop()
            self.del_trick_from_hand(t)
            tricks_added += 1
            # Have to reset the sorting dict here or we're fucked
        self.reset_sorting_dict()
        return tricks_added

    def get_sorting_dict(self):
        return self.sorting_dict

    def reset_sorting_dict(self):
        self.sorting_dict = {}

    def populate_sorting_dict(self):
        sorting_dict = self.get_sorting_dict()
        if self.hand_count() == 0:
            return
        for card in self.get_hand():
            card_rank = card.get_rank()
            if not card_rank in sorting_dict:
                sorting_dict[card_rank] = []
            sorting_dict[card_rank].append(card)

    def format_cards_by_sorting_dict(self):
        s_d = self.get_sorting_dict()
        hand_holder = []
        for g in s_d.values():
            hand_holder += g
        self.set_hand(hand_holder)

    def sort_hand(self):
        # Go through the hand. Will group similar cards within
        # 	sortingDict and then group them. Sorting dict may be used
        # 	to find out if a group can become a trick. I don't know
        self.populate_sorting_dict()
        self.format_cards_by_sorting_dict()

        # End Player Hand Functionality

        # Code for player specific TRADING PHASE operations

    def has_card(self, flag_card):
        """
        Checks to see if player has a card in their 
        hand
        """
        # Non variant version of hasCard.
        # This version just plain checks to see if the player has
        # 	any cards of given rank in their hands.
        hand = self.get_hand()
        flag_card_rank = flag_card.get_rank()
        rank_hand = []
        for c in hand:
            rank_hand.append(c.get_rank())
        return flag_card_rank in rank_hand

        # self.giveArray Helpers

    

    def remove_card(self, card):
        self.hand.remove(card)

    def remove_relevant_cards(self):
        give_array = self.get_give_array()
        for c in give_array:
            self.remove_card(c)



        # Player => Player Card Interaction

    def give_to_player(self, other: Player) -> None:
        other.take_relevant_cards(self.get_give_array())
        self.reset_give_array()

    def concede_defeat(self, chosen_card: Card) -> None:
        self.populate_give_array(chosen_card)

        # End TRADING PHASE operation code
