import socket
import sys
import json
import time
from player import *
from AI import *
from card import *

#########################################################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_IP = '140.113.123.225'
SERVER_PORT = 7975
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
sock.connect(SERVER_ADDRESS)
######################################################### set the net connection
msg = ""			# the messenge you send to server
rev = ""			# the messenge you receive from server
player_id = ""
game_id = ""
No = 0
#########################################################

def listen():
	revList = []
	rev = sock.recv(2048)
	if ("}{" in rev):
		revList = rev.split("}{")
		for i in range(len(revList)):
			if (revList[i][-1] != '}'):
				revList[i] = revList[i] + "}"
			if (revList[i][0] != '{'):
				revList[i] = "{" + revList[i]
			while (revList[i].count('{') != revList[i].count('}')):
				if (revList[i].count('{') > revList[i].count('}')):
					revList[i] = revList[i] + "}"
				else:
					revList[i] = "{" + revList[i]
			print revList[i]
	else:
		revList.append(rev)
	while (len(revList) != 0):
		print "rev", "(", len(revList), ")", revList[0]
		try:
			rev = json.loads(revList[0])
		except:
			print revList
		if ('game_id' in rev):
			global game_id
			game_id = rev['game_id']
		if ('msg' in rev):
			print "player", No, "receives:", rev['msg']
		if ('action' in rev):
			if (rev['action'] == 'get'):
				print rev['hand']
				action = playerGet(rev['hand'], rev['discard'], rev['action'])
				playerMove(action)
			if (rev['action'] == 'throw'):
				action = playerThrow(rev['get'])
				playerMove(action)
		revList.pop(0)

def playerMove(action):
	if (action == "draw"):
		msg = json.dumps({"action":"game", "command":"draw", "game_id":game_id})
	elif (action == "take"):
		msg = json.dumps({"action":"game", "command":"take", "game_id":game_id})
	else:
		msg = json.dumps({"action":"game", "command":"draw", "game_id":game_id, "hand":action})
	print "player", No, "send", msg
	sock.sendall(msg)
#########################################################

No = raw_input("player No:")
if (int(No) == 1):
	msg = json.dumps({"action":"room", "command":"create"})
	sock.sendall(msg)
else:
	game_id = raw_input("game_id:")
	msg = json.dumps({"action":"room", "command":"join", "game_id":game_id})
	sock.sendall(msg)

while (1):
	listen()
	time.sleep(1)

sock.close()