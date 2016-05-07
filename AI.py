from operator import itemgetter, attrgetter
from random import randint
from card import *

##########################################
doneList = []
waitingList = []
uselessList = []
handPool = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

block = card(0, 'empty')
##########################################

def printList (list, listname):
	print listname +'(' + str(len(list)) + ')' + ':'
	for index in range(len(list)):
		print str(index) + '\t' + list[index].color + '\t' + str(list[index].number)
	# this function is using when debug

def printHandPool():
	for i in range(13):
		print ("%2d" % int(i+1)),
	print ""
	for color in range(4):
		for number in range(13):
			print ("%2d" % handPool[color][number+1]),
		print ""

def cleanList():
	del doneList[0:len(doneList)]
	del waitingList[0:len(waitingList)]
	del uselessList[0:len(uselessList)]


def handCompare(handPool, card):
	tempPool1 = handPool
	tempPool2 = handPool
	if (card.color == "black"):
		tempPool2[0][card.number] += 1
	elif (card.color == "blue"):
		tempPool2[1][card.number] += 1
	elif (card.color == "red"):
		tempPool2[2][card.number] += 1
	elif (card.color == "yellow"):
		tempPool2[3][card.number] += 1

	handPoolAnalysis(tempPool1)
	print len(doneList)*10 + len(waitingList)*5 + len(uselessList)*1
	cleanList()
	handPoolAnalysis(tempPool2)
	print len(doneList)*10 + len(waitingList)*5 + len(uselessList)*1

##########################################

def AI(hand, CARD, mode, memory):
	print "AI is thinking..."
	for card in hand:
		if (card.color == "black"):
			handPool[0][card.number] += 1
		elif (card.color == "blue"):
			handPool[1][card.number] += 1
		elif (card.color == "red"):
			handPool[2][card.number] += 1
		elif (card.color == "yellow"):
			handPool[3][card.number] += 1

	printHandPool()
	#get a card
	action = ""

	if (mode == "get"):
		handPoolAnalysis(handPool)

		printList(doneList, "doneList")
		printList(waitingList, "waitingList")
		printList(uselessList, "uselessList")
		if (CARD.color == "empty"):
			action = "draw"
		else:
			handCompare(handPool, CARD)
		# choose draw card from deck or discard
		cleanList()
		return action

	# throw a card
	elif (mode == "throw"):
		handPoolAnalysis(handPool)
		printList(doneList, "doneList")
		printList(waitingList, "waitingList")
		printList(uselessList, "uselessList")
		returnList = []
		index = randint(0,len(uselessList)-1)
		print "throw", uselessList[index].color, uselessList[index].number
		uselessList.pop(index)
		for i in range(len(doneList)):
			returnList.append(dict({'color' : doneList[i].color, 'number' : doneList[i].number}))
		for i in range(len(waitingList)):
			returnList.append(dict({'color' : waitingList[i].color, 'number' : waitingList[i].number}))
		for i in range(len(uselessList)):
			returnList.append(dict({'color' : uselessList[i].color, 'number' : uselessList[i].number}))
		while (len(returnList) != 24):
			returnList.append(dict({'color' : 'empty', 'number' : 0}))
		cleanList()
		return returnList


def handPoolAnalysis(handPool):
	for color in range(len(handPool)):
		for number in range(len(handPool[color])):
			while (handPool[color][number] > 0):
				print "Card dealing...", color, number
				numCombo = checkNumCombo(handPool[color], number)
				colorCombo = checkColorCombo(handPool, number)
				print numCombo, colorCombo
				# compare two combo
				if (numCombo == 0 and colorCombo == 0):
					pass
				elif (numCombo > colorCombo):
					numComboClassify(color, number, numCombo)
				elif (colorCombo > numCombo):
					colorComboClassify(color, number, colorCombo)
				else:
					if (randint(0,1) == 0):
						numComboClassify(color, number, numCombo)
					else:
						colorComboClassify(color, number, colorCombo)
					#conflict handle

##########################################

def numComboClassify(color, number, combo):
	if (color == 0):
		colorStr = "black"
	elif (color == 1):
		colorStr = "blue"
	elif (color == 2):
		colorStr = "red"
	elif (color == 3):
		colorStr = "yellow"
	if (combo > 2):
		print "doneList"
		for i in range(combo):
			print number+i,
			doneList.append(card(number+i, colorStr))
			handPool[color][number+i] -= 1
		doneList.append(card(0, "empty"))
	elif (combo == 2):
		print "waitingList"
		for i in range(combo):
			print number+i,
			waitingList.append(card(number+i, colorStr))
			handPool[color][number+i] -= 1
	elif (combo == 1):
		print "uselessList"
		uselessList.append(card(number, colorStr))
		handPool[color][number] -= 1
	print ""

def colorComboClassify(color, number, combo):
	if (combo > 2):
		print "doneList"
		for i in range(len(handPool)):
			if (handPool[i][number] > 0):
				if (i == 0):
					print "black",
					doneList.append(card(number, "black"))
					handPool[i][number] -= 1
				elif (i == 1):
					print "blue",
					doneList.append(card(number, "blue"))
					handPool[i][number] -= 1
				elif (i == 2):
					print "red",
					doneList.append(card(number, "red"))
					handPool[i][number] -= 1
				elif (i == 3):
					print "yellow",
					doneList.append(card(number, "yellow"))
					handPool[i][number] -= 1
		doneList.append(card(0, "empty"))
	elif (combo == 2):
		print "waitingList"
		for i in range(len(handPool)):
			if (handPool[i][number] > 0):
				if (i == 0):
					print "black",
					waitingList.append(card(number, "black"))
					handPool[i][number] -= 1
				elif (i == 1):
					print "blue",
					waitingList.append(card(number, "blue"))
					handPool[i][number] -= 1
				elif (i == 2):
					print "red",
					waitingList.append(card(number, "red"))
					handPool[i][number] -= 1
				elif (i == 3):
					print "yellow",
					waitingList.append(card(number, "yellow"))
					handPool[i][number] -= 1
	elif (combo == 1):
		if (color == 0):
			uselessList.append(card(number, "black"))
		elif (color == 1):
			uselessList.append(card(number, "blue"))
		elif (color == 2):
			uselessList.append(card(number, "red"))
		elif (color == 3):
			uselessList.append(card(number, "yellow"))
		handPool[color][number] -= 1
	print ""
##########################################

def checkNumCombo(colorList, number):
	comboLen = 1
	search = 1
	while (number+search < 13):
		if (colorList[number+search] > 0):
			comboLen += 1
		else:
			break
		search += 1
	return comboLen

def checkColorCombo(handPool, number):
	comboLen = 0
	for color in range(len(handPool)):
		if (handPool[color][number] > 0):
			comboLen += 1
	return comboLen

##########################################