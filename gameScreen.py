from cmu_graphics import *
from objects import *
import random
from PIL import Image

def makeCMUImage(app, name):
    image = Image.open(f"images/{name}")
    return CMUImage(image)

def onAppStart(app):
    app.width = 600
    app.height = 800
    app.stepsPerSecond = 30
    app.newObjWait = 90
    app.textX = app.width // 2
    app.textY = app.height * 3 // 4
    app.dangerous = 100
    app.threshold = app.height * 3 // 4
    app.bg = makeCMUImage(app, "cowbg.png")

    app.cows = [Cow(generateRandX(), generateRandY(650, 750)), Cow(generateRandX(), generateRandY(650, 750))]
    app.objects = []
    app.wordToObject = dict()

    app.input = ""
    lst = ["hello", "test", "words", "april", "gong"]
    app.wordList = WordList(lst)
    app.counter = 0
    app.score = 0
    app.losses = 0
    app.wins = 0

    app.inGame = True
    # level increases every 20 seconds
    app.level = 1
    app.gameOver = False

def redrawAll(app):
    # draw background
    drawImage(app.bg, 0, 0)
    # display user input text
    drawLabel(app.input, app.textX, app.textY, size=16)
    # draw cows
    drawCows(app)
    if app.inGame:
        # draw falling objects
        drawFalling(app)
    else:
        drawLabel(f'Level: {app.level}', app.width//2, app.height//2, size=24)

def drawFalling(app):
    for i in range(len(app.objects)):
        object = app.objects[i]
        objImage = makeCMUImage(app, object.image)
        drawImage(objImage, object.x, object.y, width=50, height=50)
        # draw the word on the object
        drawLabel(object.word, object.x+25, object.y+60, align="center", size=16)

def drawCows(app):
    for i in range(len(app.cows)):
        cow = app.cows[i]
        cowImage = makeCMUImage(app, cow.image)
        drawImage(cowImage, cow.x, cow.y, width=170, height=85)

def onKeyPress(app, key):
    if key == "backspace":
        if app.input != "":
            app.input = app.input[:-1]
    elif key == "enter":
        if app.input in app.wordList.onScreen:
            hitObj = app.wordToObject[app.input]
            # matches an object, destroy it
            destroyObject(app, hitObj)
        # sees if it hits any of the right letters
        app.input = ""
    elif key.isalpha() and key != "space":
        app.input += key

def onStep(app):
    if app.inGame:
        # generate a new falling object every set amount of time
        if app.counter == 0 or app.counter % app.newObjWait == 0:
            newObj = generateRandObj(app)
            app.objects.append(newObj)
            app.counter = 0
        app.counter += 1
        print(app.counter)
        # update positions of falling objects
        for obj in app.objects:
            obj.y += obj.speed
            # indicate position is approaching threshold
            if app.threshold - obj.y <= app.dangerous:
                obj.danger()
            # destroy if position is beyond threshold
            if obj.y >= app.threshold:
                destroyObject(app, obj)
    elif not app.gameOver:
        # level display counter
        if app.counter >= app.stepsPerSecond * 3:
            app.inGame = True
        app.counter += 1

def generateRandObj(app):
    # generate a random word from wordlist
    randInt = random.randint(0, len(app.wordList.wordList)-1)
    randWord = app.wordList.wordList[randInt]
    # add word to list of words on screen
    app.wordList.putOnScreen(randWord)
    # remove word so it doesn't appear again for now
    app.wordList.removeWord(randWord)

    # generate random object with random word
    options = ["poison", "poison", "poison", "bomb", "hay"]
    randInt = random.randint(0, len(options)-1)
    randObj = FallingObject(randWord, options[randInt], generateRandX(), 0)
    # add word: object to dictionary
    app.wordToObject[randWord] = randObj
    return randObj

def generateRandX(leftLim = 0, rightLim = app.width):
    return random.randint(leftLim, rightLim)

def generateRandY(topLim = 0, botLim = app.height):
    return random.randint(topLim, botLim)

# take object off screen
def destroyObject(app, hitObject):
    # remove from objects list
    app.objects = removeObject(app, hitObject)
    hitWord = hitObject.word
    # add word back to the list
    app.wordList.wordList.append(hitWord)
    # remove its word from onscreen list
    if hitWord in app.wordList.onScreen:
        app.wordList.onScreen.remove(hitWord)

def removeObject(app, obj):
    objSet = set(app.objects)
    objSet.remove(obj)
    return list(objSet)

# fire projectile towards target object

def main():
    runApp()

if __name__ == '__main__':
    main()  
