import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def menu(game_stat):
	print "Welcome to Okey"
	print "enter 's' to start a game"
	print "enter 'h' for help"

	while (True):
		input = raw_input()
		if (input == 's'):
			break
		elif (input == 'h'):
			help();

	game_stat = True
	cls()
