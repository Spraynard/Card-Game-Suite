def cardRankToNum(rank, variant = None):
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
		if (rank == "Jack" or rank == "Queen" or rank == "King"):
			return 10
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