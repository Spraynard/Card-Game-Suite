from Modules.Cards.Card import Cards
from Modules.Cards.Deck import Deck
from .Player import Player

class Dealer(Player):
   
   def deal(self, player: Player, deck: Deck, amount: int) -> None:
      """
      Deals a specified amount of cards from the deck 
      to a player
      
      Parameters:
      player   - The player to deal cards to
      deck     - The deck of cards to deal from
      amount   - The amount of cards to deal to each player
      """
      cards: Cards = [ deck.draw() for _ in range(0, amount) ]
      player.take_cards(cards)