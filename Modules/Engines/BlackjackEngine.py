from Modules.Engines.Engine import Engine
from Modules.Players.Player import Player

class BlackjackEngine(Engine):
    """
    ### Rules of the game (https://bicyclecards.com/how-to-play/blackjack) ###
    
    Deck: 52 Cards, no Jokers

    Object of the Game
		To beat the dealer, getting as close to 21 without going over. 

	Card Values/scoring
		Face Cards = 10 

		Ace = 1 or 11 

		Number Cards = Personal 

    Setup
		Each player places an initial bet before cards are dealt
        
        Players receive two cards face-up
        The dealer receives one card face-up and one face-down (the "hole" card)
        
    Players Turn
		EVALUATE YOUR HAND 

		Add your two card values together 

		CHOOSE YOUR ACTION 

			Hit: Take another card to add to your total 

			Stand/Stay: Keep your current total. End your turn. 

			Double Down: Double your bet, take one final card, then stand. 

			Split: If you have a pair, split into two hands by placing a second bet equal to your first
            
    Dealer's Turn
		Dealer reveals the hole card. 

		Dealer must hit until reaching 17 or higher. 

		If the dealer busts (goes over 21), all remaining players win. 

	PAYOUTS 

		Win: Paid 1:1. 

		Blackjack (Ace + 10-value card): Paid 3:2. 

		Push (tie): Your bet is returned. 

		Lose: Dealer collects your bet. 
    
    INSURANCE
		Insurance is an optional side bet offered only when the dealer's face-up card is an Ace. 

		You may place an insurance bet equal to half your original wager. 

		This bet pays 2:1 only if the dealer's hidden card is a 10-value card, giving them blackjack. 

		The outcome of your insurance bet is separate from the outcome of your main hand.     
    """
    def take_turn(self, player: Player) -> None:
            return super().take_turn(player)