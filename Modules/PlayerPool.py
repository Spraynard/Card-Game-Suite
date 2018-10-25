class PlayerPool:
	players = [];

	def __init__(self, max_players):
		self.max_players = max_players;

	def _getPlayers(self):
		return self.players

	def _returnHumanPlayers(self):
		human_player_bucket = [];

		for player in self.players:
			if isinstance( player, HumanPlayer ):
				human_player_bucket.append( player )

		return human_player_bucket

	def checkIfHumanPlayers(self):
		return len(self._returnHumanPlayers())