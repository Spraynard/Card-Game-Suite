from Modules.Engines.Engine import Engine

class Starter:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def initialize(self) -> None:
        """
        Operations to perform after object creation
        """
        raise Exception("Not Implemented -- Starter.initialize")
    
    def start_game(self) -> None:
        self.engine.set_players(self.players)
        self.engine.initialize()

    def handle_player_init(self):
        pass

