from .HumanPlayer import HumanPlayer
from Modules.Cards.Card import Card
from faker import Faker


class Bot(HumanPlayer):
    """Bot object, which is a player. There are taunts available to bots to rouse up the player whenver they make a mistake"""

    def __init__(self, name="[Empty]"):
        super().__init__(name)

        # These are needed for bot specific functionality
        self.taunts = [
            "You're going to have to try harder than that!\"",
            'I thought that I was playing a real person, not a bot!"',
            'What the heck are you doing?"',
            "Dang, I didn't know I was playing a baby tonight\"",
        ]

        self.rejections = [
            '%s: "No',
            '%s: "Nope',
            '%s: "I sure do not',
            '%s: "Hahaha, no',
            '%s: "You wish!',
        ]
        self.choose_dict = {}

    def __repr__(self):
        return "[Bot] %s" % self.id

    def __str__(self):
        return "[Bot] %s" % self.name

    def random_name(self):
        fake = Faker()
        return Bot(fake.name())

    def taunt_player(self):
        import random

        return (
            random.choice(self.rejections) % self.get_name()
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
