class WordList:

    def __init__(self, wordList):
        self.wordList = wordList
        # self.wordList = self.intoWords()
        self.onScreen = set()
    
    def intoWords(self):
        finalList = []
        for word in self.initWordList:
            finalList.append(Word(word, False))
        return finalList
    
    def putOnScreen(self, word):
        self.onScreen.add(word)

    def offScreen(self, word):
        if word in self.onScreen:
            self.onScreen.remove(word)

    def removeWord(self, word):
        wordSet = set(self.wordList)
        if word in wordSet:
            wordSet.remove(word)
        self.wordList = list(wordSet)

class Word:

    def __init__(self, word, onScreen):
        self.word = word
        self.onScreen = onScreen

class Cow:

    healthyCow = "healthyCow.png"
    sickCow = "sickCow.png"

    def __init__(self, x, y):
        self.healthy = True
        self.image = Cow.healthyCow
        self.x = x
        self.y = y
    
    def poison(self):
        self.healthy = False
        self.image = Cow.sickCow

class FallingObject:

    poison = "poison.png"
    hay = "hay.png"
    bomb = "bomb.png"
    closeBomb = "tintBomb.jpg"
    closeHay = "tintBomb.jpg"
    closePoison = "tintBomb.jpg"

    def __init__(self, word, objType, x, y):
        self.word = word
        self.type = objType
        self.hit = 0
        self.x = x
        self.y = y
        if objType == "poison":
            self.image = FallingObject.poison
            self.speed = 3
            self.closeImage = FallingObject.closePoison
        elif objType == "hay":
            self.image = FallingObject.hay
            self.speed = 4
            self.closeImage = FallingObject.closeHay
        elif objType == "bomb":
            self.image = FallingObject.bomb
            self.speed = 5
            self.closeImage = FallingObject.closeBomb
        else:
            self.image = None

    def danger(self):
        self.image = self.closeImage

    def passed(self):
        pass

    def destroyed(self):
        pass
