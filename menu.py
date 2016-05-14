import os

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def menu(game_stat):
	cls()
	print bcolors.OKBLUE + "Welcome to Okey"
	print "enter 's' to start a game"
	print "enter 'h' for help" + bcolors.ENDC

	while (True):
		input = raw_input()
		if (input == 's'):
			break
		elif (input == 'h'):
			help();

	game_stat = True
	cls()

menu(True)