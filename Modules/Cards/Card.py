def cardRankToNum(rank):
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

def cardSuitRank(suit):
	if suit == "Diamonds":
		return 0
	elif suit == "Hearts":
		return 1
	elif suit == "Clubs":
		return 2
	elif suit == "Spades":
		return 3

class Card(object):
	""" Card class, which gives all the behavior of the card object. Takes in a rank (e.g. 2 - Ace) and a 
		suit (e.g. "Spades", "Clubs") and makes a card object off of that with those values
		
	"""

	def __init__(self, rank = None, suit = None):
		self.rank = str(rank)
		self.suit = suit
		self.acceptDict = {
			'suits' : ["Clubs", "Spades", "Diamonds", "Hearts"],
			'ranks' : ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
		}

	def __eq__(self, other):
		return (self.rank == other.rank) and (self.suit == other.suit)

	def isSameRank(self, other):
		return self.rank == other.rank

	def __lt__(self, other):
		c1 = cardSuitRank(self.suit), cardRankToNum(self.rank)
		c2 = cardSuitRank(other.suit), cardRankToNum(other.rank)
		return c1 < c2

	def __gt__(self, other):
		c1 = cardSuitRank(self.suit), cardRankToNum(self.rank)
		c2 = cardSuitRank(other.suit), cardRankToNum(other.rank)
		return c1 > c2

	def __repr__(self):
		return "Card(" + str(self.rank) + ", " + str(self.suit) + ")"

	def __str__(self):
		return self.rank + " of " + self.suit

	def getAcceptDict(self):
		return self.acceptDict

	def getRank(self):
		return self.rank

	def acceptableRank(self):
		return self.getRank() in self.getAcceptDict()['ranks']

	def getSuit(self):
		return self.suit