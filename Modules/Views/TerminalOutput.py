from Modules.Players.Player import Player


class TerminalOutput:
    @staticmethod
    def header(text, width=46, fill="=", margin=1):
        """Center text with `margin` spaces on each side."""
        text = f"{' ' * margin}{text}{' ' * margin}"
        return text.center(width, fill)

    @staticmethod
    def hand(player: Player) -> list:
        # Prints out the hand legibly in a line!
        hand = player.getHand()
        cards = [str(c) for c in hand]
        rows = [", ".join(cards[i : i + 3]) for i in range(0, len(cards), 3)]
        TerminalOutput.header("HAND")
        print()
        print("\n".join(rows) + "\n")
