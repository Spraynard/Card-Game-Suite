from Modules.Cards.Card import Card
from Modules.Engines.Engine import Engine
from Modules.Players import HumanPlayer
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

    def add_master_trick_count(self, amount):
        # Add the amount referenced in the amount param to the total trick count
        self.trick_count += amount

    def display_current_player_info(self, player: HumanPlayer):
        # Give
        if isinstance(player, Bot):
            # No need to display if
            # 	the player is a bot
            return
        player.display_tricks()
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
        choice_list = list(self.get_players())
        choice_list.remove(player)
        choice = False

        if isinstance(player, Bot):
            import random

            bot = player
            bot.set_chosen_player(random.choice(choice_list))
        else:
            # Implement Player() player to ask
            print("Which player will you ask a card from?")
            for i in range(len(choice_list)):
                print(f"{i + 1}: {choice_list[i]}")
            choice = self.player_ask_loop(len(choice_list))

        player.set_chosen_player(choice_list[choice])

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

    def ask_for_card_rank(self, player: HumanPlayer) -> Card:
        """
        Summary: Once the player chooses a card rank and another player to ask,
                       those values are stored in the player object and extracted in other code later on.
        Input: `player` - a player object, can be a humanplayer or a bot
        """
        chosen_player = player.get_chosen_player()
        chosen_card = player.get_chosen_card()

        player.talk("ask")

        if chosen_player.has_card(chosen_card):
            # Count how many cards there are of that cardRank in the player's hand
            # 	give feedback based on the amount of cards.
            player.guessed_correctly()
            chosen_player.concede_defeat(chosen_card)
            if isinstance(chosen_player, Bot):
                bot = chosen_player
                bot.talk("exclaim")
            else:
                chosen_player.talk("defeat")
            # cardsToChangePlayers = chosenPlayer.
            chosen_player.give_to_player(player)
        else:
            if isinstance(chosen_player, Bot):
                # If the other player is a bot, they will taunt you
                # 	and probably make you really sad af.
                bot = chosen_player
                print(bot.taunt_player())
            else:
                chosen_player.talk("victory")

        return chosen_card

    # End Game Action Functionality
    def game_start_deal_number_of_cards(self):
        # Three Players or more
        return 5 if len(self.players) > 3 else 7

    # Game Phases Here
    def initial_phase(self, player):
        self.display_current_player_info(player)

    def decision_phase(self, player):
        self.choose_player_to_ask(player)
        self.choose_card(player)

    def trading_phase(self, player: Player):
        chosen_card = self.ask_for_card_rank(player)
        # Player state is valuable after they ask for card.
        deck = self.get_deck()

        if not player.got_guess():
            if (player.hand_count() == 0) and (deck.current_amount() == 0):
                print(
                    "Hey everyone, laugh at %s! They got kicked out of the game for losing!"
                    % player
                )
                self.removePlayer(player)
            else:
                drawn_card = player.draw_card(deck)

                if drawn_card == chosen_card:
                    self.take_turn()

        player.reset_chosen_variables()

    def win_conditions_met(self):
        return self.getMasterTrickCount() == 13

    def end_phase(self, player: Player):
        player.sort_hand()
        player.look_for_tricks()
        tricks_added = player.set_tricks()
        self.add_master_trick_count(tricks_added)

        if player.got_guess():
            # If the player has a good guess (e.g. they asked another player for a card that they
            # 	had in their hand and they actually had one or more of those cards in their hand)

            # Resetting the player's guess for next turn :)
            player.reset_guess()
            self.take_turn()
        else:
            # If the player had to draw from the pile because they guessed badly.
            self._add_player_index()

        if self.win_conditions_met():
            self.toggle_game_over()

    # End Game Phases
    def take_turn(self):
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
