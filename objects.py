from wordfreq import word_frequency
from wonderwords import RandomWord
from cmu_graphics import *
from PIL import Image
import random


R = RandomWord()


class WordList:

    def __init__(self, wordList, listLength):
        self.wordList = wordList
        self.wordSet = set(self.wordList)
        self.listOfWords = self.intoWords()
        self.onScreen = set()
        self.listLength = listLength
        self.genRandomList()
        self.difficultySort()
        self.removedWordToIndex = dict()
    
    def __repr__(self):
        string = 'hi'
        for word in self.listOfWords:
            string += f'{word.word}: {word.difficulty}, '
        return string
    
    def intoWords(self):
        finalList = []
        for word in self.wordList:
            finalList.append(Word(word, False))
        return finalList
    
    def putOnScreen(self, word):
        self.onScreen.add(word)

    def offScreen(self, word):
        onScreenList = list(self.onScreen)
        for screenWord in onScreenList:
            if word == screenWord.word:
                self.onScreen.remove(screenWord)

    def removeWord(self, word):
        for i in range(len(self.listOfWords)):
            if self.listOfWords[i].word == word:
                self.removedWordToIndex[word] = i
                self.listOfWords.pop(i)
                break
        if word in self.wordSet:
             self.wordSet.remove(word)
        self.wordList = list(self.wordSet)

    def addWord(self, word):
        if word not in self.wordSet:
            if word.word in self.removedWordToIndex:
                i = self.removedWordToIndex[word.word]
                self.listOfWords.insert(i, word)
            self.wordSet.add(word)
            self.wordList.append(word)

    def genRandomList(self):
        for i in range(self.listLength):
            nextWord = R.word()
            # add non-repeating words in list
            if nextWord not in self.wordSet:
                self.wordSet.add(nextWord)
                self.wordList.append(nextWord)
                self.listOfWords.append(Word(nextWord, False))

    # sort by difficulty
    def difficultySort(self):
        self.listOfWords = sorted(self.listOfWords, 
        key=lambda word:word.difficulty)

    # get sublist depending on game level
    # corresponding difficulty + player's missed words
    def getLevelList(self, currLevel, totalLevels, missedWords):
        length = len(self.listOfWords)
        listSize = length // totalLevels
        indLow = (currLevel-1) * listSize
        indHi = indLow + listSize
        if currLevel >= totalLevels:
            indLow = length - listSize
            indHi = length
        return self.listOfWords[indLow:indHi]

class Word:

    def __init__(self, word, onScreen):
        self.word = word
        self.onScreen = onScreen
        self.frequency = word_frequency(word, 'en')
        self.hit = 0
        self.difficulty = self.getDifficulty()

    def __repr__(self):
        return self.word
    
    def __eq__(self, other):
        return type(other) == Word and self.word == other.word

    def __hash__(self):
        return hash(self.word)

    def getDifficulty(self):
        length = len(self.word)
        # length + convert frequency to number between 0 and 10
        # 0 is highest frequency (lower difficulty), 10 lowest frequency
        freqScore = self.decimalPlaces()
        return length + freqScore

    # return how many decimal places frequency is
    def decimalPlaces(self):
        if self.frequency == 0.0:
            return 10
        n = self.frequency
        places = 0
        while n < 1:
            n *= 10
            places += 1
        return places

class Cow:

    healthyCow = "healthyCow.png"
    sickCow = "sickCow.png"
    deadCow = "deadCow.png"

    def __init__(self, x, y):
        self.healthy = True
        self.image = Cow.makeCMUImage(Cow.healthyCow)
        self.x = x
        self.y = y
        self.deadTimer = 0
        self.dead = False
        self.moveTimer = random.randint(7, 10)
        self.timer = 0
        self.tx = x
        self.ty = y
    
    def poison(self):
        self.healthy = False
        self.image = Cow.makeCMUImage(Cow.sickCow)
    
    def kill(self):
        self.image = Cow.makeCMUImage(Cow.deadCow)
        self.dead = True

    def randCowMove(self, stepsPerSec, xLowLim, xHiLim, yLowLim, yHiLim):
        stepsInSeconds = self.moveTimer * stepsPerSec
        if self.timer >= stepsInSeconds:
            self.timer = 0
            # generate random cow move
            self.tx = random.randint(xLowLim, xHiLim)
            self.ty = random.randint(yLowLim, yHiLim)
        elif self.timer < stepsInSeconds // 2:
            # move towards target
            stepsLeft = stepsInSeconds // 2 - self.timer
            xDist = (self.x-self.tx) / stepsLeft
            yDist = (self.y-self.ty) / stepsLeft
            self.x -= int(xDist)
            self.y -= int(yDist)
            self.timer += 1
        else:
            self.timer += 1

    def makeCMUImage(name):
        image = Image.open(f"images/{name}")
        return CMUImage(image)


class FallingObject:

    poison = "poison.png"
    hay = "hay.png"
    bomb = "bomb.png"
    closeBomb = "tintBomb.png"
    closeHay = "tintHay.png"
    closePoison = "tintPoison.png"

    def __init__(self, word, objType, x, y, speed, movement="straight", rightLim=0,
                 leftLim=0):
        self.word = word
        self.destroyCount = 0
        self.type = objType
        self.destroy = False
        self.hitLetters = 0
        self.x = x
        self.y = y
        self.xMove = 0
        self.limit = 0
        self.movement = movement
        if movement != "straight":
            distFromLeft = leftLim - x
            distFromRight = rightLim - x
            self.xMove = random.randint(distFromLeft, distFromRight)
            if self.xMove < 0:
                self.leftLimit = x + self.xMove 
                self.rightLimit = x
            else:
                self.leftLimit = x
                self.rightLimit = x + self.xMove

        self.speed = speed
        self.xSpeed = random.randint(1, 3)
        if objType == "poison":
            self.image = FallingObject.makeCMUImage(FallingObject.poison)
            self.closeImage = FallingObject.makeCMUImage(FallingObject.closePoison)
        elif objType == "hay":
            self.image = FallingObject.makeCMUImage(FallingObject.hay)
            self.closeImage = FallingObject.makeCMUImage(FallingObject.closeHay)
        elif objType == "bomb":
            self.image = FallingObject.makeCMUImage(FallingObject.bomb)
            self.closeImage = FallingObject.makeCMUImage(FallingObject.closeBomb)
        else:
            self.image = None

    def danger(self):
        self.image = self.closeImage

    def makeCMUImage(name):
        image = Image.open(f"images/{name}")
        return CMUImage(image)

class Projectile:

    def __init__(self, initX, initY, targetX, targetY, numSteps):
        self.x = initX
        self.y = initY
        self.numSteps = numSteps
        self.steps = 0
        self.tx = targetX
        self.ty = targetY
        self.reachedTarget = False

    def getNextPos(self):
        if self.steps >= self.numSteps:
            self.reachedTarget = True
        else:
            stepsLeft = self.numSteps - self.steps
            xDist = (self.x-self.tx) / stepsLeft
            yDist = (self.y-self.ty) / stepsLeft
            self.x -= xDist
            self.y -= yDist
            self.steps += 1
