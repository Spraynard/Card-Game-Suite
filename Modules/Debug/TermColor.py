from colorama import init, Fore, Back, Style

init(autoreset=True)

def printGreenBG(string):
	print Back.GREEN + "%s" % string

def printBlueBG(string):
	print Back.BLUE + "%s" % string

def printYellowBG(string):
	print Back.YELLOW + "%s" % string