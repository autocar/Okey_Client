import json
from AI import *
from card import *

hand = []

memory = [[0,2,2,2,2,2,2,2,2,2,2,2,2,2],
		  [0,2,2,2,2,2,2,2,2,2,2,2,2,2],
		  [0,2,2,2,2,2,2,2,2,2,2,2,2,2],
		  [0,2,2,2,2,2,2,2,2,2,2,2,2,2]]

def hand_clear():
	del hand[0:len(hand)]

def draw_card(card):
	hand.append(card)

def getCardInHand(item):
	color = str(item['color'])
	number = int(item['number'])
	if (color != 'empty' and number != -1):
		draw_card(card(number, color))
		writeIntoMemory(card(number, color))

def writeIntoMemory(card):
	if (card.color == 'black'):
		memory[0][card.number]-=1
	elif (card.color == 'blue'):
		memory[1][card.number]-=1
	elif (card.color == 'red'):
		memory[2][card.number]-=1
	elif (card.color == 'yellow'):
		memory[3][card.number]-=1

##########################################################

def playerGet(rev, CARD, action):
	for line in rev:
		for index in line:
			getCardInHand(index)
	CARD = card(CARD['number'], CARD['color'])
	writeIntoMemory(CARD)
	AI_response = AIGet(hand, CARD, action, memory)
	return AI_response

def playerThrow(CARD):
	getCardInHand(CARD)
	AI_response = AIThrow(hand, memory)
	return AI_response