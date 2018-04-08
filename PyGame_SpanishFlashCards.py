# -*- coding: utf-8 -*-
import pygame
import time
import random
pygame.init()
import button
import sys
import ctypes

random.seed(time.time())

try:
	gamefile = sys.argv[1]
except Exception as e:
	print('missing datafile\npython PyGame_SpanishFlashCards.py <datafile.csv>')
	sys.exit(1)

if 'win' in sys.platform:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
#gamefile = 'chapter11vocab.csv'

class Colors:
    white = (255,255,255)
    gray = (200,200,200)
    gray180 = (180,180,180)
    black = (0,0,0)
    dgray = (100,100,100)

def resetData(index,spanish,english,sp_scores, en_scores,mode):
    dataFile = open(gamefile,'w',encoding='utf-8')

    for i in range(len(spanish)):
        dataFile.write(spanish[i]+','+english[i]+',0,0\n')
        sp_scores[i] = 0
        en_scores[i] = 0
    
        
    dataFile.close()
    return True

def compareWords(word1,word2):
    return word1 == word2

def getWord(index,english,spanish,mode):
    if mode == 0:
        return spanish[index]
    else:
        return english[index]
    
def text_objects(text, font,color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

def display_message(surface,text,color,coord_tuple):
        rect = surface.get_rect()
        disp_x = rect.right
        disp_y = rect.bottom
        font_file = pygame.font.match_font('setofont')
        largeText = pygame.font.Font(font_file,60)
        x_offset = disp_x/2
        y_offset = disp_y/5
        TextSurf, TextRect = text_objects(text, largeText,color)
        TextRect.center = coord_tuple
        surface.blit(TextSurf,TextRect)
        return TextRect

def toggleScoreTrue(index,scoreList):
    if scoreList[index] == 0:
        scoreList[index] = 1
    return True

def getTotalScore(ScoreList):
    good = 0
    for i in range(len(ScoreList)):
        #print(ScoreList[i])
        if int(ScoreList[i]) == 1:
            #print('found')
            good += 1
    #print(str(good)+' of '+str(len(ScoreList)))
    return float(good/len(ScoreList))
   
# function(list,list,list,list,int) -> boolean
# index: random shuffled list of indexes
# spanish: list of spanish words
# english: list of english words
# scores: list of scores 0 or 1
# mode: 0 for spanish -> english, 1 for english -> spanish
def saveGame(sp2EnScoreList,en2SpScoreList):
    dataFile = open(gamefile,'w',encoding='utf-8')
    for i in range(len(spanishWords)):
        dataFile.write(spanishWords[i]+','+englishWords[i]+','+str(sp2EnScoreList[i])+','+str(en2SpScoreList[i])+'\n')
    dataFile.close()
    
def simpleAnswerMode(index,spanish,english,sp_scores,en_scores,mode):
	dispInfo = pygame.display.Info()
	#disp_x = int(dispInfo.current_w * 0.8) #1600
	#disp_y = int(dispInfo.current_h * 0.8) #1200
	display = pygame.display.set_mode((disp_x,disp_y))
	display.fill(Colors.white)
	buttonRectangleList = []
	buttonList = []
	buttonMap = {}
	#Exit list[0]
	buttonRectangleList.append(pygame.Rect(disp_x-90,0,90,50))
	buttonList.append(button.Button(display,buttonRectangleList[0],'Exit'))
	#Yes list[1]
	buttonRectangleList.append(pygame.Rect(disp_x*0.50-300,disp_y*0.75,150,50))
	buttonList.append(button.Button(display,buttonRectangleList[1],'Yes',toggleScoreTrue))
	#No list[2]
	buttonRectangleList.append(pygame.Rect(disp_x*0.50+50,disp_y*0.75,150,50))
	buttonList.append(button.Button(display,buttonRectangleList[2],'No'))
	#Show list[3]
	showButtonRect = pygame.Rect(disp_x*0.50-110,disp_y*0.75,150,50)
	showButton = button.Button(display,showButtonRect,'Show',getWord)
    
	for i in range(len(buttonRectangleList)):
		buttonMap[tuple(buttonRectangleList[i])] = buttonList[i]


	for i in index:
		display.fill(Colors.white)
		pygame.display.update()
		
		if mode == 0:
			#display_text
			scores = sp_scores
			display_message(display,spanish[i],Colors.black,(disp_x*0.5,disp_y*0.5))
		else:
			#display_text
			scores = en_scores
			display_message(display,english[i],Colors.black,(disp_x*0.5,disp_y*0.5))
		if scores[i] == 1: #if already correct skip
			continue    
		display_message(display,'Do you know this word?',Colors.black,(disp_x*0.5,disp_y*0.10))
		#create a yes and no button
		for buttons in buttonList:
			buttons.buttonUp()
		showButton.buttonUp()
		isButtonClicked = False
		
		while isButtonClicked == False:
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if showButtonRect.collidepoint(event.pos):
						showButton.buttonDown()
					for rect in buttonRectangleList:
						if rect.collidepoint(event.pos):
						   buttonMap[tuple(rect)].buttonDown()
				if event.type == pygame.MOUSEBUTTONUP:
					showButton.buttonUp()
					if showButtonRect.collidepoint(event.pos):
							   display_message(display,showButton.click(i,spanish,english,mode),Colors.black,(disp_x * 0.5, disp_y * 0.9))
					if buttonRectangleList[0].collidepoint(event.pos):
						   return False
					for rect in buttonRectangleList:
						   buttonMap[tuple(rect)].buttonUp()
					for rect in buttonRectangleList:
						if rect.collidepoint(event.pos):
							buttonMap[tuple(rect)].click(i,scores)
							isButtonClicked = True
	saveGame(sp_scores,en_scores)
            
def multipleChoice(index,spanish,english,sp_scores, en_scores,mode):
	#dispInfo = pygame.display.Info()
	#disp_x = int(dispInfo.current_w * 0.8) #1600
	#disp_y = int(dispInfo.current_h * 0.8) #1200
	display = pygame.display.set_mode((disp_x,disp_y))
	display.fill(Colors.white)
	#create the exit button
	#display the word
	#create 5 buttons, 1 with the right word, 4 with randomwords
	if mode == 0:
		sourceWords = spanish
		targetWords = english
		scores = sp_scores
	else:
		sourceWords = english
		targetWords = spanish
		scores = en_scores

	exitRect = pygame.Rect(disp_x-50,0,50,50)
	exitButton = button.Button(display,exitRect,'Exit')
	btnRectList = []
	btnMap = {}
	for i in range(7):
		btnRectList.append(pygame.Rect(disp_x-410,i*50+100,400,50))
		btnMap[tuple(btnRectList[i])]=button.Button(display,btnRectList[i],'btn',compareWords)

	for i in index:
		display.fill(Colors.white)
		if scores[i] == 1:
			continue
		sourceWord = sourceWords[i]
		targetWord = targetWords[i]
	   
		reshuffle = list(targetWords)
		random.shuffle(reshuffle)
		#get some wrong words
		incorrectWords = []
		for j in range(7):
			incorrectWords.append(reshuffle[j])
		


		for j in range(len(btnRectList)):
			btnMap[tuple(btnRectList[j])].setLabel(incorrectWords[j])
		btnMap[tuple(btnRectList[0])].setLabel(targetWord)

		bntListIndexes = list(range(len(btnRectList)))
		random.shuffle(bntListIndexes)
		btnRectCopy = list(btnRectList)
		for i in range(len(bntListIndexes)):
			btnRectList[i] = btnRectCopy[bntListIndexes[i]]
					   
		
		display_message(display,sourceWord,Colors.black,(disp_x*0.5,disp_y*0.1))
		pygame.display.update()
		buttonClicked = False
		answer = False
		exitButton.buttonUp()
		for key in btnMap:
				btnMap[key].buttonUp()
		pygame.display.update()
		while not buttonClicked:
			
			
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if exitRect.collidepoint(event.pos):
						exitButton.buttonDown()
					for r in btnRectList:
						if r.collidepoint(event.pos):
							btnMap[tuple(r)].buttonDown()
					pygame.display.update()

				if event.type == pygame.MOUSEBUTTONUP:
					exitButton.buttonUp()
					for key in btnMap:
						btnMap[key].buttonUp()
					pygame.display.update()
					if exitRect.collidepoint(event.pos):
						return False
					for r in btnRectList:
						if r.collidepoint(event.pos):
							answer=btnMap[tuple(r)].click(btnMap[tuple(r)].label,targetWord)
							#print(btnMap[tuple(r)].label)
							buttonClicked = True
							if answer:
								display_message(display,'Correct',Colors.black,(disp_x*0.25,disp_y*0.5))
								toggleScoreTrue(targetWords.index(targetWord),scores)
								answer = False
							else:
								display_message(display,'Incorrect',Colors.black,(disp_x*0.25,disp_y*0.5))

							wait = True
							pygame.display.update()
							while wait:
								for event in pygame.event.get():
									if event.type == pygame.QUIT:
										saveGame(sp2EnScoreList,en2SpScoreList)
										return False
									if event.type == pygame.MOUSEBUTTONUP:
										if exitRect.collidepoint(event.pos):
											saveGame(sp2EnScoreList,en2SpScoreList)
											return False
										wait = False
	saveGame(sp2EnScoreList,en2SpScoreList)
                

dataFile = open(gamefile,'r',encoding='utf-8')
try:
    rawData = dataFile.readlines()
except UnicodeDecodeError as err:
        print('Error {0}'.format(err))
        sys.exit(1)
dataFile.close()

spanishWords = []
englishWords = []
sp2EnScoreList = []
en2SpScoreList = []

fileLineIndex=1
for lines in rawData:
	try:
		splitLine = lines.split(',')
		splitLine[3] = splitLine[3].strip('\n')
		splitLine[2] = int(splitLine[2])
		splitLine[3] = int(splitLine[3])
		spanishWords.append(splitLine[0])
		englishWords.append(splitLine[1])
		sp2EnScoreList.append(splitLine[2])
		en2SpScoreList.append(splitLine[3])
		fileLineIndex += 1
	except IndexError:
		print('Impropery Formatted input file on line %i'%fileLineIndex)
		sys.exit(1)
	except ValueError:
		print('Impropery Formatted input file on line %i'%fileLineIndex)
		sys.exit(1)

indexList = list(range(0,len(spanishWords)))
random.shuffle(indexList)

dispInfo = pygame.display.Info()
disp_x = int(dispInfo.current_w * 0.8) #1600
disp_y = int(dispInfo.current_h * 0.8) #1200
display = pygame.display.set_mode((disp_x,disp_y))


buttonList = [ pygame.Rect(disp_x*0.5-100, disp_y*0.5-100,200,50),
               pygame.Rect(disp_x*0.5-200,disp_y*0.5+1, 200,50),
               pygame.Rect(disp_x*0.5+1,  disp_y*0.5+1, 200,50),
               pygame.Rect(disp_x*0.5-200,disp_y*0.5+101,200,50),
               pygame.Rect(disp_x*0.5+1,  disp_y*0.5+101,200,50) ]
btnMap = { tuple(buttonList[0]) : button.Button(display, buttonList[0],'Reset Scores',resetData) ,
           tuple(buttonList[1]) : button.Button(display, buttonList[1],'Simple S->E',simpleAnswerMode),
           tuple(buttonList[2]) : button.Button(display, buttonList[2],'Simple E->S',simpleAnswerMode),
           tuple(buttonList[3]) : button.Button(display, buttonList[3],'Multiple S->E',multipleChoice),
           tuple(buttonList[4]) : button.Button(display, buttonList[4],'Multiple E->S',multipleChoice) }
modeMap = { tuple(buttonList[0]) : 0,
            tuple(buttonList[1]) : 0,
            tuple(buttonList[2]) : 1,
            tuple(buttonList[3]) : 0,
            tuple(buttonList[4]) : 1 }


loop = True
display.fill(Colors.white)
for key in btnMap:
        btnMap[key].buttonUp()
while loop:
    
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            for r in buttonList:
                if r.collidepoint(event.pos):
                    btnMap[tuple(r)].buttonDown()
                    pygame.display.update()
        if event.type == pygame.MOUSEBUTTONUP:
            for key in btnMap:
                btnMap[key].buttonUp()
            for r in buttonList:
                if r.collidepoint(event.pos):
                   btnMap[tuple(r)].click(indexList,spanishWords,englishWords,sp2EnScoreList,en2SpScoreList,modeMap[tuple(r)])
                   random.shuffle(indexList)
                   display.fill(Colors.white)
                   for key in btnMap:
                       btnMap[key].buttonUp()

print('Sp->Eng Score :' + str(getTotalScore(sp2EnScoreList)))
print('Eng->Sp Score :' + str(getTotalScore(en2SpScoreList)))


#save state of Game

    
saveGame(sp2EnScoreList,en2SpScoreList)
pygame.quit()
