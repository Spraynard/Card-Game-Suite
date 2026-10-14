from typing import Self
from Modules.Cards.Card import Card
from Modules.Cards.Deck import Deck
from Modules.Players import Player

class ActionsCard:
    hand: list[Card] = []
    
    def get_hand(self):
        return self.hand

    def set_hand(self, hand):
        self.hand = hand

    def has_hand(self):
        return self.hand_count() > 0

        # Gives the length of a player's hand.

    def hand_count(self):
        return len(self.get_hand())

        # |---------Drawing or Taking Cards Functionality--------|

    def draw_card(self, deck: Deck) -> Card:
        # Summary: Draws a single card from the deck and then adds it to the player's hand
        # Input: `Deck` - The deck being used by the players.
        # Return: Void if everything goes alright. False if shit is messed up
        card = deck.card_from_top()

        if card:
            self.take_card(card)
            
        return card

    def draw_cards(self, deck: Deck, amount: int) -> list:
        cards = []
        for i in range(amount):
            cards.append(self.draw_card(deck))
        return cards

    def take_card(self, card) -> None:
        self.hand.append(card)

    def take_cards(self, cards: list[Card]) -> None:
        for card in cards:
            self.take_card(card)

    def reset_hand(self) -> None:
        self.hand = []

    def get_sorting_dict(self):
        return self.sorting_dict

    def reset_sorting_dict(self):
        self.sorting_dict = {}
        
    def populate_sorting_dict(self):
        sorting_dict = self.get_sorting_dict()
        if self.hand_count() == 0:
            return
        for card in self.get_hand():
            card_rank = card.get_rank()
            if not card_rank in sorting_dict:
                sorting_dict[card_rank] = []
            sorting_dict[card_rank].append(card)

    def format_cards_by_sorting_dict(self):
        s_d = self.get_sorting_dict()
        hand_holder = []
        for g in s_d.values():
            hand_holder += g
        self.set_hand(hand_holder)

    def sort_hand(self):
        # Go through the hand. Will group similar cards within
        # 	sortingDict and then group them. Sorting dict may be used
        # 	to find out if a group can become a trick. I don't know
        self.populate_sorting_dict()
        self.format_cards_by_sorting_dict()

        # End Player Hand Functionality

        # Code for player specific TRADING PHASE operations

    def has_card(self, card: Card):
        """
        Checks to see if player has a card in their 
        hand
        """
        hand = self.get_hand()
        flag_card_rank = card.get_rank()
        rank_hand = []
        for c in hand:
            rank_hand.append(c.get_rank())
        return flag_card_rank in rank_hand

    def remove_card(self, card: Card):
        self.hand.remove(card)

    def remove_relevant_cards(self):
        give_array = self.get_give_array()
        for c in give_array:
            self.remove_card(c)