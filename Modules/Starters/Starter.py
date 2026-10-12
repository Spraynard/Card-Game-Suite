from Modules.Engines.Engine import Engine

class Starter:
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
        self.engine.set_players(self.players)
        self.engine.initialize()

    def handle_player_init(self):
        pass

