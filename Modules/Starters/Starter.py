from Modules.Engines.Engine import Engine

class Starter:
    players = []
    min_bots = 0
    max_players = 0
    min_players = 0
    min_bots = 0
    human_amount = 0
    bot_amount = 0
    max_human_players = 0
    human_players = False

    """
    Starters perform all of the operations for getting all information
    needed before we can start a game
    """
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def initialize(self) -> None:
        """
        Operations to perform after object creation.

        This would be stuff like asking how many players there will 
        be etc
        """
        raise Exception("Not Implemented -- Starter.initialize")
    
    def start_game(self) -> None:
        self.engine.start(self.players)

    def handle_player_init(self):
        pass

