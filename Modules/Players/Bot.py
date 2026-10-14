from Modules.Players.Player import Player


class Bot(Player):
    def __repr__(self):
        return "[Bot] %s" % self.id

    def __str__(self):
        return "[Bot] %s" % self.name