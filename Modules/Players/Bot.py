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
        self.chooseDict = {}

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
        maxCount = None
        rankMax = None
        cD = self._getChooseDict()
        chooseDictKeys = cD.keys()

        for k in chooseDictKeys:
            currentLength = len(cD[k])
            if (not maxCount) or (maxCount < currentLength):
                maxCount = currentLength
                rankMax = k

        self.set_chosen_card(Card(rankMax))

    def _random_choice(self):
        import random

        hand = self.get_hand()

        if len(hand) == 0:
            chooseableCards = Card().acceptDict["ranks"]
            self.set_chosen_card(Card(random.choice(chooseableCards)))
        else:
            self.set_chosen_card(random.choice(hand))

    # chooseDict Functionality
    def _getChooseDict(self):
        return self.chooseDict

    def _addChooseDict(self, card):
        # Initializes the card rank key with an array if that key is not
        # 	in `chooseDict`. Then appends the card into the key's array.
        chooseDict = self._getChooseDict()
        cardRank = card.getRank()

        if not cardRank in chooseDict:
            chooseDict[cardRank] = []

        chooseDict[cardRank].append(card)

    def _resetChooseDict(self):
        self.chooseDict = {}

    def choose_card(self):
        # Implement Bot Card Choosing. Game will not work without this. What I eventually want to to is
        #  1. Bot looks through hand for cards they have
        #  2. Of cards that bot has, look for the rank in which you have the most of.
        #  2a. If you have multiple ranks with the same amount, break by choosing randomly
        self._assemble_choose_dict()
        # self._analyzeChooseDict()
        self._random_choice()
