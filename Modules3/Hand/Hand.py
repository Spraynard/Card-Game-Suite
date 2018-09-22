class Hand(object):
	def __init__(self):
		self.cardArray = []
		self.handValue = 0

	def addCard(self, card):
		self.cardArray.append(card)
		self.addHandValue(int(card.getRank()))

	def removeCard(self, card):
		self.cardArray.remove(card)

