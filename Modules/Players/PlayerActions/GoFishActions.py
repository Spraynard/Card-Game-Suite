from random import random
from Modules.Players.PlayerActions.CardActions import CardActions

class GoFishActions(CardActions):
    def __init__(self) -> None:
        super.__init__(self)

        self.tricks = 0
        # Internal Player's Responses to questions posed by engine
        self.guess = None
        self.chosen_player = None
        self.chosen_card = None

        # Array used to give cards to other players
        self.give_array = []
        self.sorting_dict = {}
        self.trick_holder = []

    def get_give_array(self):
        return self.give_array

    def add_give_array(self, card):
        self.give_array.append(card)

    def reset_give_array(self):
        self.give_array = []

    def populate_give_array(self, chosen_card):
        """
        Giving cards means finding the cards of the specific rank
        in the hand, taking them out of the hand,
        and putting them in the give array, which
        removes said cards from hand.
        """
        for card in self.hand:
            if card.is_same_rank(chosen_card):
                # Appending it to the array of cards you're going to give
                self.add_give_array(card)
                # Removing it from the player's hand
        self.remove_relevant_cards()

    
    def get_trick_holder(self):
        return self.trick_holder

    def add_trick_holder(self, trick):
        self.get_trick_holder().append(trick)

    def reset_trick_holder(self):
        self.trick_holder = []

    def add_player_trick(self):
        self.tricks += 1

    def add_total_trick(self, trick_ref):
        trick_ref += 1

    def get_tricks(self):
        return self.tricks

    def has_tricks(self):
        return not (self.get_tricks == 0)
    
    def ask_other_player(self):
        statement_dict = {
            1: '%s: "Hey %s, Do you have any %ss?"',
        }
        print(
            statement_dict[random.choice(list(statement_dict.keys()))]
            % (
                self.get_name(),
                self.get_chosen_player(),
                self.get_chosen_card().get_rank(),
            )
        )

    def exclaim(self):
        if len(self.get_give_array()) == 1:
            statement_dict = {
                1: '%s: "Dammit, I have %s card of that rank. Here it is: %s"',
                2: '%s: "Wow, you\'re really good at this! I have %s card of that rank. Here it is you scallywag: %s"',
                3: '%s: "Are you cheating? I have %s card of that rank. Take it ya dingus!: %s"',
            }
        else:
            statement_dict = {
                1: '%s: "Dammit, I have %s cards of that rank. Here\'s your damn cards: %s"',
                2: '%s: "Wow, you\'re really good at this! I have %s cards of that rank. Here they are you scallywag: %s"',
                3: '%s: "Are you cheating? I have %s cards of that rank. Take em ya dingus! %s"',
            }
        print(
            statement_dict[random.choice(list(statement_dict.keys()))]
            % (self.get_name(), len(self.get_give_array()), self.get_give_array())
        )