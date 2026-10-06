class Hand(object):
    def __init__(self):
        self.card_array = []
        self.hand_value = 0

    def add_card(self, card):
        self.card_array.append(card)
        self.addHandValue(int(card.get_rank()))

    def remove_card(self, card):
        self.card_array.remove(card)
