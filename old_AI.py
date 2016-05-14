from operator import itemgetter, attrgetter
from random import randint
from card import *

doneList = []
waitingList = []
uselessList = []
blackList = []
blueList = []
redList = []
yellowList = []

value = 0

block = card(-1, 'empty')

def printList (list, listname):
	print listname +'(' + str(len(list)) + ')' + ':'
	for index in range(len(list)):
		print str(index) + '\t' + list[index].color + '\t' + str(list[index].num)
	# this function is using when debug

def AI(hand, discard, mode):
	print "AI is thinking..."
	# start to analyis hand
	classifyByColor(hand)
	# doneList is done
	checkUseless(uselessList)
	printList(doneList, "doneList")
	printList(waitingList, "waitingList")
	printList(uselessList, "uselessList")

	# choose draw card from deck or discard
	if (mode == "draw"):
		return "deck"

	# throw a card
	if (mode == "throw"):
		return []

def classifyByColor (hand):
	for index in range(len(hand)):
		if (hand[index].color == 'black'):
			blackList.append(hand[index])
		if (hand[index].color == 'blue'):
			blueList.append(hand[index])
		if (hand[index].color == 'red'):
			redList.append(hand[index])
		if (hand[index].color == 'yellow'):
			yellowList.append(hand[index])
	# seperate different card by color

	blackList.sort(key=attrgetter('num'))
	blueList.sort(key=attrgetter('num'))
	redList.sort(key=attrgetter('num'))
	yellowList.sort(key=attrgetter('num'))
	# sort the colorList

	findCombo(blackList)
	findCombo(blueList)
	findCombo(redList)
	findCombo(yellowList)
	# find number combo in colorList


def findCombo(colorList):
	mark = 1
	if (len(colorList) == 1):
		colorList[0].mark = 1
	for index in range(len(colorList)-1):
		if (colorList[index].num+1 == colorList[index+1].num):
			colorList[index].mark = mark
			colorList[index+1].mark = mark+1
			mark = mark + 1
		elif (colorList[index].num == colorList[index+1].num):
			colorList[index].mark = mark
			colorList[index+1].mark = mark
		else:
			colorList[index].mark = mark
			colorList[index+1].mark = 1
			mark = 1

	p = 0
	select = []
	temp = 0
	while (len(colorList) > 0):
		if (p >= len(colorList)):
			combo(select, colorList)
			p = 0
			temp = 0
		# the head of list
		elif (colorList[p].mark == 1 and len(select) == 0):
			select.append(p)
			temp += 1
			p += 1
		# combo
		elif (colorList[p].mark == temp+1):
			select.append(p)
			temp += 1
			p += 1
		# same num
		elif (colorList[p].mark == temp and colorList[p].mark != 1):
			p += 1
		# combo end
		else:
			# classify to list
			combo(select, colorList)
			p = 0
			temp = 0

def combo(select, colorList):
	if (len(select) > 2):
		for i in range(len(select)):
			doneList.append(colorList[select[i]])
	elif (len(select) == 2):
		for i in range(len(select)):
			waitingList.append(colorList[select[i]])
	else:
		uselessList.append(colorList[select[0]])
	# pop from colorList
	select.reverse()
	for i in range(len(select)):
		colorList.pop(select[i])
	del select[0:len(select)]


def checkUseless (uselessList):
	uselessList.sort(key=attrgetter('num'))
	count = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	colorCount = [[],[],[],[]]
	temp = []

	for i in range(len(uselessList)):
		count[uselessList[i].num-1] += 1

	for index in range(len(count)):

		if (count[index] > 1):
			for search in range(len(uselessList)):
				if (int(uselessList[search].num) == int(index+1)):
					if (uselessList[search].color == 'black'):
						colorCount[0].append(search)
					if (uselessList[search].color == 'blue'):
						colorCount[1].append(search)
					if (uselessList[search].color == 'red'):
						colorCount[2].append(search)
					if (uselessList[search].color == 'yellow'):
						colorCount[3].append(search)

			for i in range(4):
				if (len(colorCount[i]) == 2):
					count[index] -= 1
					if (count[index] == 1):
						count[index] = 0
			if (count[index] >= 2):
				for i in range(4):
					if (len(colorCount[i]) == 1):
						if (count[index] > 2):
							doneList.append(uselessList[colorCount[i][0]])
						elif (count[index] == 2):
							waitingList.append(uselessList[colorCount[i][0]])
					if (len(colorCount[i]) == 2):
						colorCount[i].pop()
						if (count[index] > 2):
							doneList.append(uselessList[colorCount[i][0]])
						elif (count[index] == 2):
							waitingList.append(uselessList[colorCount[i][0]])
					temp.extend(colorCount[i])
				temp.sort(reverse=True)
				for i in range(len(temp)):
					uselessList.pop(temp[i])
				colorCount = [[],[],[],[]]
				temp = []