from cmu_graphics import *
from objects import *
import random
from PIL import Image
import math

def makeCMUImage(app, name):
    image = Image.open(f"images/{name}")
    return CMUImage(image)

'''
Citations:
Robyn Speer. (2022). rspeer/wordfreq: v3.0 (v3.0.2). Zenodo. https://doi.org/10.5281/zenodo.7199437


Level Settings:
score = speed * 50 + length of word * 20
every object passed, score -= int(20 * (2/speed))
Level 1: 
    waitTime 2 seconds
    poison speed = 1
    bomb speed = 2
    hay speed = 2
level up when 30 seconds passed
'''

def onAppStart(app):
    app.start = True
    app.width = 600
    app.height = 800
    app.stepsPerSecond = 30
    app.newObjWait = 70
    app.textX = app.width // 2
    app.textY = app.height * 3 // 4
    app.scoreX = app.width // 10
    app.scoreY = app.height // 15
    app.dangerous = 200
    app.threshold = app.height * 3 // 4
    app.titlepg = makeCMUImage(app, "title.png")
    app.bg = app.titlepg

    app.cows = [Cow(generateRandX(), generateRandY(650, 700)), Cow(generateRandX(), 
                                                                   generateRandY(650, 700))]
    app.objects = []
    app.projectiles = []
    app.wordToObject = dict()
    app.objToSpeed = {"poison": 1,
                      "hay": 2,
                      "bomb": 2}

    app.input = ""
    app.correctTyped = False

    # cow related words
    lst = ["pasture", "shepherd", "bonanza",
           "moooooo", "milk", "udders", "bovine", "cattle", "heifer", "dairy",
           "grazing", "hooves", "calves", "holstein", "angus", "jersey", "hereford",
           "brahman", "charolais", "limousin", "simmental", "highland", "shorthorn",
           "ayrshire", "longhorn", "dexter", "beef", "manure", "barn", "silage", 
           "grazing", "livestock", "muzzle", "bullpen", "meadow", "field",
           "pastoral", "ranch", "agriculture", "milkmaid", "lactation", "ruminant",
           "herefordshire", "stockyard", "bovinophile", "bovinophobia", "milkshake",
           "cheesemaking", "clover", "meadowlark", "mootivation", "moosic", "cowcatcher",
           "cowpox", "cowabunga", "cowpoke"]

    # generate 100 more random words
    app.wordList = WordList(lst, 100)
    app.missedWords = set()

    app.projR = 5
    app.projSteps = 15
    app.projX = app.textX
    app.projY = app.textY

    app.counter = 0
    app.score = 0
    app.losses = 0
    app.wins = 0

    app.inGame = False
    # level increases every 30 seconds
    app.level = 1
    app.totalLevels = 10
    app.gameOver = False
    app.paused = False
    app.instructions = False

def restart(app):
    app.cows = [Cow(generateRandX(), generateRandY(650, 700)), Cow(generateRandX(), 
                                                                   generateRandY(650, 700))]
    app.objects = []
    app.projectiles = []
    app.wordToObject = dict()
    app.objToSpeed = {"poison": 1,
                      "hay": 2,
                      "bomb": 2}

    app.input = ""
    app.correctTyped = False

    # cow related words
    lst = ["pasture", "shepherd", "bonanza",
           "moooooo", "milk", "udders", "bovine", "cattle", "heifer", "dairy",
           "grazing", "hooves", "calves", "holstein", "angus", "jersey", "hereford",
           "brahman", "charolais", "limousin", "simmental", "highland", "shorthorn",
           "ayrshire", "longhorn", "dexter", "beef", "manure", "barn", "silage", 
           "grazing", "livestock", "muzzle", "bullpen", "meadow", "field",
           "pastoral", "ranch", "agriculture", "milkmaid", "lactation", "ruminant",
           "herefordshire", "stockyard", "bovinophile", "bovinophobia", "milkshake",
           "cheesemaking", "clover", "meadowlark", "mootivation", "moosic", "cowcatcher",
           "cowpox", "cowabunga", "cowpoke"]

    # generate 100 more random words
    app.wordList = WordList(lst, 100)
    app.missedWords = set()

    app.projR = 5
    app.projSteps = 15
    app.projX = app.textX
    app.projY = app.textY

    app.counter = 0
    app.score = 0
    app.losses = 0
    app.wins = 0

    app.inGame = False
    # level increases every 30 seconds
    app.level = 1
    app.totalLevels = 10
    app.gameOver = False
    app.paused = False
    app.instructions = False

def redrawAll(app):
    # draw background
    drawImage(app.bg, 0, 0)
    if app.start:
        drawLabel("Press space to continue", app.width//4, app.height*7//8, 
        font='monospace', size=16, fill='white')
    if not app.start and not app.instructions:
        # draw score
        drawLabel(f'Score: {int(app.score)}', app.scoreX, app.scoreY, font='monospace',
                  bold=True)
        # draw cows
        drawCows(app)
        if app.inGame and not app.paused:
            # display user input text
            drawLabel(app.input, app.textX, app.textY, font='monospace', bold=True, size=16)
            # draw falling objects and projectiles
            drawFalling(app)
            drawProjectiles(app)
        elif not app.gameOver and not app.start:
            drawLabel(f'Level: {app.level}', app.width//2, app.height//2, font='monospace', 
                      bold=True, size=24)
        elif app.gameOver:
            drawLabel("GAME OVER", app.width//2, app.height//2, font='monospace', 
                      bold=True, size=24)
            drawLabel("Press space to restart", app.width//2, app.height//2+100,
                      font='monospace', bold=True, size=16)

def drawFalling(app):
    for i in range(len(app.objects)):
        obj = app.objects[i]
        drawImage(obj.image, obj.x, obj.y, width=50, height=50)
        # draw the word on the object
        # draw hit words in red
        hitInd = obj.word.hit
        # drawLabel(obj.word.word, obj.x+25, obj.y+60, align='center', size=16)
        drawLabel(obj.word.word[:hitInd] + " " * (len(obj.word.word)-hitInd), obj.x+25, obj.y+60, 
                    align="center", size=16, fill="red", font='monospace', bold=True)
        drawLabel(" " * (hitInd+1) + obj.word.word[hitInd:], obj.x+25, obj.y+60, align="center", 
                  font='monospace', bold=True, size=16)

def drawProjectiles(app):
    for proj in app.projectiles:
        drawCircle(proj.x, proj.y-10, app.projR)

def drawCows(app):
    for i in range(len(app.cows)):
        cow = app.cows[i]
        drawImage(cow.image, cow.x, cow.y, width=170, height=85)

def onKeyPress(app, key):
    if key == '0':
        app.paused = not app.paused
    if key == "space":
        if app.start:
            app.bg = makeCMUImage(app, "instructions.png")
            app.start = False
            app.instructions = True
        elif app.instructions:
            app.bg = makeCMUImage(app, "cowbg.png")
            app.instructions = False
        elif app.gameOver:
            app.gameOver = False
            restart(app)
    if key == "backspace":
        if app.input != "":
            app.input = app.input[:-1]
    elif key == "enter":
        if Word(app.input, True) in app.wordList.onScreen:
            hitObj = app.wordToObject[app.input]
            objectHit(app, hitObj)
        app.input = ""
    elif len(key) == 1 and key != '0' and app.inGame:
        app.input += key
    # sees if it hits any of the right letters
    for screenWord in app.wordList.onScreen:
        if app.input == screenWord.word[:len(app.input)]:
            screenWord.hit = len(app.input)
        else:
            screenWord.hit = 0

def onStep(app):
    # game over when no cows
    if len(app.cows) == 0:
        app.inGame = False
        app.gameOver = True
    if not app.start and app.inGame and not app.paused and not app.instructions:
        # every 30 seconds, level increases
        if app.counter != 0 and app.counter % (app.stepsPerSecond * 30) == 0:
            levelIncrease(app)
        # generate a new falling object every set amount of time
        elif app.counter == 0 or app.counter % app.newObjWait == 0:
            newObj = generateRandObj(app)
            app.objects.append(newObj)
        app.counter += 1
        # update positions of falling objects
        for obj in app.objects:
            # make move depending on object move type
            if obj.movement == "straight":
                moveStraight(obj)
            elif obj.movement == 'zigzag':
                moveZigzag(obj)
            # indicate position is approaching threshold
            if app.threshold - obj.y <= app.dangerous:
                obj.danger()
            # destroy if position is beyond threshold
            if obj.y >= app.threshold:
                objectPassed(app, obj)
                destroyObject(app, obj)
            # destroy in projSteps when obj hit
            if obj.destroy:
                if obj.destroyCount >= app.projSteps:
                    destroyObject(app, obj)
                else:
                    obj.destroyCount += 1

        # update positions of projectiles
        for i in range(len(app.projectiles)):
            app.projectiles[i].getNextPos()
            if app.projectiles[i].reachedTarget:
                app.projectiles.pop(i)
        # keep dead cows for 2 seconds
        for cow in app.cows:
            if cow.dead:
                cow.deadTimer += 1
                if cow.deadTimer >= app.stepsPerSecond * 2:
                    # remove cow from list
                    app.cows = app.cows[1:]
            else:
                cow.randCowMove(app.stepsPerSecond, max(0, cow.x-100), 
                                min(app.width, cow.x+100), max(650, cow.y-100), 
                                min(750, cow.y+100))
    elif not app.start and not app.gameOver:
        # level display counter
        if app.counter >= app.stepsPerSecond * 3:
            app.inGame = True
        app.counter += 1

def levelIncrease(app):
    # add object words back to list
    for obj in app.objects:
        app.wordList.addWord(obj.word)
    app.level += 1
    # even level, increase frequency at same speed
    if app.level % 2 == 0 and app.newObjWait >= 10:
        app.newObjWait -= 5
    # odd level, increase speed of each object
    elif app.level % 2 == 1:
        for obj in app.objToSpeed:
            app.objToSpeed[obj] += 1
    app.counter = 0
    # reset things
    app.objects = []
    app.projectiles = []
    app.wordToObject = dict()
    app.input = ""
    app.inGame = False

def generateRandObj(app):
    # generate a random word from level's wordlist
    leveledList = app.wordList.getLevelList(app.level, app.totalLevels, 
                                            list(app.missedWords))
    randInt = random.randint(0, len(leveledList)-1)
    randWord = leveledList[randInt]
    while randWord in app.wordList.onScreen:
        randInt = random.randint(0, len(leveledList)-1)
        randWord = leveledList[randInt]
    # add word to list of words on screen
    app.wordList.putOnScreen(randWord)
    # remove word so it doesn't appear again for now
    app.wordList.removeWord(randWord.word)

    # generate random object with random word, random movetype
    options = ["poison", "poison", "poison", "bomb", "bomb", "hay"]
    randInt = random.randint(0, len(options)-1)
    randType = options[randInt]
    movements = ["straight", "zigzag"]
    randInt = random.randint(0, len(movements)-1)
    randMoveType = movements[randInt]
    randObj = FallingObject(randWord, randType, generateRandX(100, app.width-100), 
                            0, app.objToSpeed[options[randInt]], movement=randMoveType,
                            rightLim=app.width-100, leftLim=100)
    # add word: object to dictionary
    app.wordToObject[randWord.word] = randObj
    return randObj

def generateRandX(leftLim = 0, rightLim = app.width):
    return random.randint(leftLim, rightLim)

def generateRandY(topLim = 0, botLim = app.height):
    return random.randint(topLim, botLim)

def objectPassed(app, obj):
    firstCow = app.cows[0]
    if obj.type == "poison":
        # make the first healthy cow sick, or kill if already sick
        if firstCow.healthy:
            firstCow.poison()
        else:
            firstCow.kill()
    elif obj.type == "bomb":
        # kill the cow 
        firstCow.kill()
    updateScore(app, False, obj)
    # add to missed words
    app.missedWords.add(obj.word)

def objectHit(app, obj):
    updateScore(app, True, obj)
    if obj.type == "hay":
        app.cows.append(Cow(generateRandX(), generateRandY(650, 700)))
    # start setting timer to destroy object in set steps
    obj.destroy = True
    # add projectile towards object
    addProjectile(app, obj)
    # score = 50
    # remove from missed words
    if obj.word in app.missedWords:
        app.missedWords.remove(obj.word)

def updateScore(app, wasHit, obj):
    distFromCows = app.threshold - obj.y
    scaledDistFromCows = int(distFromCows * (10 / app.threshold))
    if wasHit:
        app.score += (app.level * 2) * (obj.word.difficulty * 50 +
                                        scaledDistFromCows * 10)
    else:
        app.score -= app.level * 10 * obj.word.difficulty * 10

# take object off screen
def destroyObject(app, obj):
    # remove from objects list
    app.objects = removeObject(app, obj)
    hitWord = obj.word
    # add word back to the list
    app.wordList.addWord(hitWord)
    # remove its word from onscreen list
    app.wordList.offScreen(hitWord)

def removeObject(app, obj):
    objSet = set(app.objects)
    if obj in objSet:
        objSet.remove(obj)
    return list(objSet)

def moveStraight(obj):
    obj.y += obj.speed

def moveZigzag(obj):
    obj.y += obj.speed
    # object moves left
    if obj.xMove < 0:
        # keep moving to left if space left
        if obj.x > obj.leftLimit:
            obj.x -= obj.xSpeed
        # change movement to right when limit surpassed
        else:
            obj.xMove *= -1
    # object moves right
    elif obj.xMove > 0:
        if obj.x < obj.rightLimit:
            obj.x += obj.xSpeed
        else:
            obj.xMove *= -1

def moveSin(app, obj):
    obj.y += obj.speed
    randInRange = random.randint(20, obj.x)
    obj.x += math.sin()

# predict where an object will be in steps
def predictObjPos(obj, steps):
    x = obj.x
    y = obj.y + obj.speed * steps
    if obj.xMove == 0:
        return x, y
    stepsAcrossMove = obj.xMove // obj.xSpeed
    # moving left
    if obj.xMove < 0:
        stepsToLimit = (obj.x - obj.leftLimit) // obj.xSpeed
    # moving right
    elif obj.xMove > 0:
        stepsToLimit = (obj.rightLimit - obj.x) // obj.xSpeed
    stepsAfterLimit = steps - stepsToLimit 
    # print(f'current x: {obj.x}, rightLimit: {obj.rightLimit}, leftLimit: {obj.leftLimit}, xMove: {obj.xMove}, xSpeed: {obj.xSpeed}, stepsAcrossMove: {stepsAcrossMove}, stepsToLimit: {stepsToLimit}, stepsAfterLimit: {stepsAfterLimit}')
    # doesn't change directions
    if stepsAfterLimit <= 0:
        if obj.xMove < 0:
            x = obj.x - obj.xSpeed * steps
        else:
            x = obj.x + obj.xSpeed * steps
    else:
        runs = steps // stepsAfterLimit
        stepsFromLimit = stepsAfterLimit % stepsAcrossMove
        # equivalent to turning around once and going back, same dir
        if (runs % 2 == 1 and obj.xMove < 0) or (runs % 2 == 0 and obj.xMove > 0):
            x = obj.rightLimit - stepsFromLimit
        else:
            x = obj.leftLimit + stepsFromLimit
    return x, y

def addProjectile(app, hitObj):
    tx, ty = predictObjPos(hitObj, app.projSteps)
    tx += 25
    ty += 60
    app.projectiles.append(Projectile(app.projX, app.projY, tx, ty, app.projSteps))

def main():
    runApp()

if __name__ == '__main__':
    main()  
