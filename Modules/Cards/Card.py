def card_rank_to_num(rank, variant=None):
    if not variant:
        if rank == "Ace":
            return 14
        elif rank == "King":
            return 13
        elif rank == "Queen":
            return 12
        elif rank == "Jack":
            return 11
        else:
            return int(rank)
    elif variant == "blackjack":
        if rank == "Jack" or rank == "Queen" or rank == "King":
            return 10
        else:
            return int(rank)


def card_suit_rank(suit):
    if suit == "Diamonds":
        return 0
    elif suit == "Hearts":
        return 1
    elif suit == "Clubs":
        return 2
    elif suit == "Spades":
        return 3


class Card(object):
    """Card class, which gives all the behavior of the card object. Takes in a rank (e.g. 2 - Ace) and a
    suit (e.g. "Spades", "Clubs") and makes a card object off of that with those values

    """

    def __init__(self, rank=None, suit=None, variant=None):
        self.rank = str(rank)
        self.suit = suit
        self.variant = variant
        self.accept_dict = {
            "suits": ["Clubs", "Spades", "Diamonds", "Hearts"],
            "ranks": [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Jack",
                "Queen",
                "King",
                "Ace",
            ],
        }

    def __eq__(self, other):
        if not self or not other:
            return None
        return (self.rank == other.rank) and (self.suit == other.suit)

    def is_same_rank(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        c1 = card_suit_rank(self.suit), card_rank_to_num(self.rank)
        c2 = card_suit_rank(other.suit), card_rank_to_num(other.rank)
        return c1 < c2

    def __gt__(self, other):
        c1 = card_suit_rank(self.suit), card_rank_to_num(self.rank)
        c2 = card_suit_rank(other.suit), card_rank_to_num(other.rank)
        return c1 > c2

    def __repr__(self):
        return "Card(" + str(self.rank) + ", " + str(self.suit) + ")"

    def __str__(self):
        return self.rank + " of " + self.suit

    def card_suit_to_num(suit):
        pass

    def get_accept_dict(self):
        return self.accept_dict

    def get_rank(self):
        return self.rank

    def acceptable_rank(self):
        return self.get_rank() in self.get_accept_dict()["ranks"]

    def get_suit(self):
        return self.suit
