from Modules.Cards.Card import Card
from Modules.Engines.Engine import Engine
from Modules.Players.Bot import Bot
from Modules.Players.Player import Player
from Modules.Views.TerminalOutput import TerminalOutput

"""
Right now the engine and the UI are mixed together.

In order to implement a TUI I am going to have to 
remove the print statements and have the engine control the 
TUI
"""


class GoFishEngine(Engine):
    trick_count = 0

    # Game Action Functionality
    def getMasterTrickCount(self):
        # Return Engine's total trick count
        return self.trick_count

    def addMasterTrickCount(self, amount):
        # Add the amount referenced in the amount param to the total trick count
        self.trick_count += amount

    def display_current_player_info(self, player):
        # Give
        if isinstance(player, Bot):
            # No need to display if
            # 	the player is a bot
            return
        player.displayTricks()
        TerminalOutput.hand(player)
    
    def player_ask_loop(self, choice_list_length):
        """Asks the current player which player they want to choose"""
        choice = None
        while True:
            choice = int(input("Please enter your choice: ")) - 1
            if (choice < 0) or (choice >= choiceListLength):
                print("\nError: That is not one of the player choices")
            else:
                break
        return choice

    def choose_player_to_ask(self, player: Player):
        # Summary: Instructs the player to choose another player to ask for a card. This code also handles bots.
        # Input: `Player` - A player object
        # Returns: Void
        choice_list = list(self.getPlayers())
        choice_list.remove(player)
        choice = False

        if isinstance(player, Bot):
            import random

            bot = player
            bot.setChosenPlayer(random.choice(choice_list))
        else:
            # Implement Player() player to ask
            print("Which player will you ask a card from?")
            for i in range(len(choice_list)):
                print(f"{i + 1}: {choice_list[i]}")
            choice = self.player_ask_loop(len(choice_list))

        player.setChosenPlayer(choice_list[choice])

    def choose_card(self, player):
        """
        Summary: Instructs players to choose a rank of card that they also have in their hand to eventually ask another player
        that is chosen.

        If a bot, Implement Bot Card Choosing. Game will not work without this. What I eventually want to to is
              1. Bot looks through hand for cards they have
              2. Of cards that bot has, look for the rank in which you have the most of.
              2a. If you have multiple ranks with the same amount, break by choosing randomly
              3. As for the selected rank from an opponent.
        """
        if isinstance(player, Bot):
            bot = player
            bot.choose_card()
        else:
            rank = None

            if not self.variant:
                while True:
                    rank = (
                        input("What card rank do you want to ask for (e.g. 2 - Ace)?: ")
                        .lower()
                        .title()
                    )
                    flagCard = Card(rank)
                    if not flagCard.acceptableRank():
                        print(
                            "\nError: That is not an acceptable card rank. Please choose again."
                        )
                    elif not player.hasCard(flagCard):
                        print(
                            "\nError: You don't even have any of those cards in your hand! Try again."
                        )
                    else:
                        player.setChosenCard(Card(rank))
                        break
            # This code is for when I implement any variants within the game. Do not pay attention to now.
            # if self.variant == 1:
            # 	suit = None
            # 	while True:
            # 		suit = str(input("What card suit do you want to ask for (e.g. 'Clubs', 'Spades')?: ")).lower().title()
            # 		if not suit in correctInputDict['suits']:
            # 			print("That is not an acceptable card suit. Please choose again")
            # 		else:
            # 			break

    def askForCardRank(self, player):
        """
        Summary: Once the player chooses a card rank and another player to ask,
                       those values are stored in the player object and extracted in other code later on.
        Input: `player` - a player object, can be a humanplayer or a bot
        """
        chosenPlayerGiveArray = False

        chosenPlayer = player.getChosenPlayer()
        chosenCard = player.getChosenCard()

        player.talk("ask")

        if chosenPlayer.hasCard(chosenCard):
            # Count how many cards there are of that cardRank in the player's hand
            # 	give feedback based on the amount of cards.
            player.guessedCorrectly()
            chosenPlayer.concedeDefeat(chosenCard)
            if isinstance(chosenPlayer, Bot):
                bot = chosenPlayer
                bot.talk("exclaim")
            else:
                chosenPlayer.talk("defeat")
            # cardsToChangePlayers = chosenPlayer.
            chosenPlayer.giveToPlayer(player)
        else:
            if isinstance(chosenPlayer, Bot):
                # If the other player is a bot, they will taunt you
                # 	and probably make you really sad af.
                bot = chosenPlayer
                print(bot.taunt_player())
            else:
                chosenPlayer.talk("victory")

        return chosenCard

    # End Game Action Functionality
    def game_start_deal_number_of_cards(self):
        # Three Players or more
        return  5 if len(self.players) > 3 else 7

    # Game Phases Here
    def initial_phase(self, player):
        self.display_current_player_info(player)

    def decision_phase(self, player):
        self.choose_player_to_ask(player)
        self.choose_card(player)

    def trading_phase(self, player: Player):
        chosenCard = self.askForCardRank(player)
        # Player state is valuable after they ask for card.
        deck = self.getDeck()

        if not player.gotGuess():
            if (player.handCount() == 0) and (deck.currentAmount() == 0):
                print(
                    "Hey everyone, laugh at %s! They got kicked out of the game for losing!"
                    % player
                )
                self.removePlayer(player)
            else:
                drawnCard = player.drawCard(deck)

                if drawnCard == chosenCard:
                    self.takeTurn()

        player.resetChosenVariables()

    def winConditionsMet(self):
        return self.getMasterTrickCount() == 13

    def end_phase(self, player):
        player.sortHand()
        player.lookForTricks()
        tricks_added = player.setTricks()
        self.addMasterTrickCount(tricks_added)

        if player.gotGuess():
            # If the player has a good guess (e.g. they asked another player for a card that they
            # 	had in their hand and they actually had one or more of those cards in their hand)

            # Resetting the player's guess for next turn :)
            player.resetGuess()
            self.takeTurn()
        else:
            # If the player had to draw from the pile because they guessed badly.
            self._addPlayerIndex()

        if self.winConditionsMet():
            self.toggleGameOver()

    # End Game Phases
    def takeTurn(self):
        # Turn consists of:
        # 	INITIAL PHASE
        # 	- Displaying player's hand and amount of tricks (if any)
        # 	DECISION PHASE
        # 	- choosing which player to ask for a card
        #  	- choosing which card to ask of them
        # 	TRADING PHASE
        # 	- If other player has card, give card(s) to asking player
        # 	- If other player does not have card, asking player draws one card from deck
        # 	END PHASE
        # 	- Scan hand to see if there are any tricks available
        # 	- If four tricks, player wins
        player = self.get_current_player()
        self.initial_phase(player)
        self.decision_phase(player)
        self.trading_phase(player)
        self.end_phase(player)
