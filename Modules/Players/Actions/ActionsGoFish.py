import random
from typing import Self
from Modules.Cards.Card import Card
from Modules.Players.Actions.ActionsCard import ActionsCard
from Modules.Players.Player import Player, PlayerTalkReason
class ActionsGoFish(ActionsCard):
    tricks = 0
    # Internal Player's Responses to questions posed by engine
    guess = None
    chosen_player = None
    chosen_card = None

    # Array used to give cards to other players
    give_array: Cards = []
    sorting_dict = {}
    trick_holder = []

    def get_give_array(self):
        return self.give_array

    def add_give_array(self, card: Card):
        self.give_array.append(card)

    def reset_give_array(self):
        self.give_array = []

    def populate_give_array(self, chosen_card: Card):
        """
        Giving cards means finding the cards of the specific rank
        in the hand, taking them out of the hand,
        and putting them in the give array, which
        removes said cards from hand.
        """
        for card in self.hand:
            if card.is_same_rank(chosen_card):
                self.give_array.append(card)
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
    
    def ask_other_player(self, name: str):
        statement_dict = {
            1: '%s: "Hey %s, Do you have any %ss?"',
        }
        print(
            statement_dict[random.choice(list(statement_dict.keys()))]
            % (
                name,
                self.get_chosen_player(),
                self.get_chosen_card().get_rank(),
            )
        )

    def exclaim(self, name: str):
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

        return statement_dict[random.choice(list(statement_dict.keys()))] % (name, len(self.get_give_array()), self.get_give_array())
    
    def victory_statement(self, name: str) -> str:
        statement_dict = {
            1: '"I sure do not!"',
        }
        return statement_dict[random.choice(list(statement_dict.keys()))]

    def defeat_statement(self, name:str):
        statement_dict = {
            1: f'{name}: "I do have {len(self.get_give_array())} cards. Here they are": {self.get_give_array()}'
        }
        return statement_dict[random.choice(list(statement_dict.keys()))]

    def talk(self, talker: Player, reason: PlayerTalkReason):
        reason_dict = {
            PlayerTalkReason.VICTORY: self.victory_statement,
            PlayerTalkReason.DEFEAT: self.defeat_statement,
            PlayerTalkReason.EXCLAIM: self.exclaim,
            PlayerTalkReason.ASK: self.ask_other_player,
        }

        reason_dict[reason](talker.get_name())
    
    def get_chosen_player(self) -> Player[Self]:
        return self.chosen_player

    def set_chosen_player(self, player: Player[Self]):
        self.chosen_player = player

    def get_chosen_card(self) -> Card:
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

    def concede_defeat(self, chosen_card: Card) -> None:
        self.populate_give_array(chosen_card)

class GoFishBotActions(ActionsGoFish):
    """Bot object, which is a player. There are taunts available to bots to rouse up the player whenver they make a mistake"""
    choose_dict = {}

    taunts = [
        "You're going to have to try harder than that!\"",
        'I thought that I was playing a real person, not a bot!"',
        'What the heck are you doing?"',
        "Dang, I didn't know I was playing a baby tonight\"",
    ]

    rejections = [
        '%s: "No',
        '%s: "Nope',
        '%s: "I sure do not',
        '%s: "Hahaha, no',
        '%s: "You wish!',
    ]

    def taunt_player(self, name: str) -> str:
        import random

        return (
            random.choice(self.rejections) % name
            + ". "
            + random.choice(self.taunts)
        )

        # Hand Evaluation Functionality

    def _assemble_choose_dict(self):
        hand = self.get_hand()
        for c in hand:
            self._addChooseDict(c)

    def _analyze_choose_dict(self):
        # Haha, this is laughably bad AI for the bots.
        # 	Might as well have a random card generator for now
        max_count = None
        rank_max = None
        c_d = self._getChooseDict()
        choose_dict_keys = c_d.keys()

        for k in choose_dict_keys:
            current_length = len(c_d[k])
            if (not max_count) or (max_count < current_length):
                max_count = current_length
                rank_max = k

        self.set_chosen_card(Card(rank_max))

    def _random_choice(self):
        import random

        hand = self.get_hand()

        if len(hand) == 0:
            chooseable_cards = Card().accept_dict["ranks"]
            self.set_chosen_card(Card(random.choice(chooseable_cards)))
        else:
            self.set_chosen_card(random.choice(hand))

            # chooseDict Functionality

    def _getChooseDict(self):
        return self.choose_dict

    def _addChooseDict(self, card):
        # Initializes the card rank key with an array if that key is not
        # 	in `chooseDict`. Then appends the card into the key's array.
        choose_dict = self._getChooseDict()
        card_rank = card.get_rank()

        if not card_rank in choose_dict:
            choose_dict[card_rank] = []

        choose_dict[card_rank].append(card)

    def _resetChooseDict(self):
        self.choose_dict = {}

    def choose_card(self):
        # Implement Bot Card Choosing. Game will not work without this. What I eventually want to to is
        #  1. Bot looks through hand for cards they have
        #  2. Of cards that bot has, look for the rank in which you have the most of.
        #  2a. If you have multiple ranks with the same amount, break by choosing randomly
        self._assemble_choose_dict()
        # self._analyzeChooseDict()
        self._random_choice()