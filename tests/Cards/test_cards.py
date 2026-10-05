from Modules.Cards.Card import Card


def test_two_same_cards_equal():
    card_1 = Card(2, "Clubs")
    card_2 = Card(2, "Clubs")
    assert card_1 == card_2


def test_two_different_cards_not_equal():
    card_1 = Card(2, "Clubs")
    card_2 = Card(2, "Spades")
    assert card_1 != card_2
