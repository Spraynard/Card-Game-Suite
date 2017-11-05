import sys

from Menu import Menu
from config.menuConfig import * 

class MainMenu(Menu):
	def __init__(self):
		super(MainMenu, self).__init__()
		self.gameList = []

	def populateGameList(self):
		for value in games.keys():
			self.gameList.append(games[value]['title'])

	def displayGameList(self):
		pass


	def start(self):
		self.populateGameList()
		print "Hello and welcome. These are the games that\
		You are able to play!", self.gameList