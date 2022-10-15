import math
from cmu_112_graphics import *
import copy
import decimal
import random
from enemy import *
from pointer import *
from texts import *
#This main class runs everything


def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))



def appStarted(app):
    # Starts the app
    '''---Customize---'''
    app.timerDelay = 15
    app.mouseMovedDelay = 15
    app.cameraDistance = 100
    app.cameraHeight = 20
    app.pS = app.pSx = app.pSy = 3
    app.changeAngle = math.pi/100*app.pS
    '''---------------'''
    '''pX : Player Position
    pZ: Player Z Position
    pDp: Player change in position
    pDt: Player change in theta in the x z plane
    pDtY: Player change in theta in the x y plane
    pT: Player theta
    delayAngle: delay in change of theta
    dimensions: dimensions of the grid
    xscale: scale of 1 to distance between two points horizontally in the grid
    yscale: scale of 1 to distance between two points vertically in the grid
    map: the positions of each point in the grid
    board: the points after the transformations
    trail: Player trail
    Enemy, pointer, and text object
    Images
    '''
    app.pX = 0
    app.pZ = 0
    app.pDp = 1
    app.pDt = 0
    app.pDty = 0
    app.pT = 0
    app.pastX = 0
    app.pastZ = 0
    app.delayAngle = 0
    app.dimensions = 20
    app.xscale = 210
    app.yscale = 1000
    app.map = [[0] * (app.dimensions+1) for i in range(app.dimensions*2+1)]
    make(app)
    app.board = copy.deepcopy(app.map)
    app.playerT = [app.pX%(app.width/app.dimensions), app.pZ%(app.width/app.dimensions), app.pX, app.pZ, "PaleTurquoise"]
    app.trail = [app.playerT]
    app.move = True
    #Cited from cmu PIL
    app.tron = app.scaleImage(app.loadImage('tron.png'), 1/5)
    app.boost1 = app.scaleImage(app.loadImage('arrow.png'), 1/16)
    app.alive = True
    app.moves = []
    app.enemy = Enemy(30, -app.cameraHeight, 30, 3, app.width/app.dimensions, app.width, app.trail)
    app.isOn = True
    app.just = 0
    app.spawn = (app.width/2, app.height)
    app.playerWin = texts((app.width/2, app.height/8, "User Wins", ("Courier", 40), "PaleTurquoise1", "n"), 1.4)
    app.enemyWin = texts((app.width/2, app.height/8, "Program Wins", ("Courier", 40), "orange1", "n"), 1.4)
    app.ruleTexts = texts(((10, 35, "Hello User\n" + 
    "\nYour Mission: Derezz the Program\n\n"
    "Abilities:\n"+
    "t : Trail Toggle\n"+
    "b : Boost (3 Only)\n"+
    "x : Delete Move Queue\n" +
    "A : Turn Left\n"+
    "D : Turn Right\n"+
    "Mouse : Look Around\n" +
    "\n\nDerezz or Be Derezzed.\n" +
    "Process finished with exit code 1",
     ("Courier", 29), "green2", "nw")), 1)
    app.justOn = True
    app.home = app.scaleImage(app.loadImage('IMG_3294.jpeg'), 0.228)
    app.playGame = Pointer(app.width/2-80, app.height/2-20, app.width/2+80, app.height/2+20, 15, 5, "The Grid")
    app.playRules = Pointer(app.width/2-80, app.height/2+100, app.width/2+80, app.height/2+140, 15, 5, "Directions")
    app.back = Pointer(app.width-110, 30, app.width-30, 70, 10, 5, "Return")
    app.indexes = []
    app.game = False
    app.rules = False
    app.boost = 3
    app.justBoost = 0
    


def make(app):
    #Initializes the map with the coordinates
    for i in range(-app.dimensions, app.dimensions+1):
        for j in range(app.dimensions+1):
            app.map[i+app.dimensions][j] = (
                i*app.width/app.dimensions, -app.cameraHeight, j*app.width/app.dimensions+1)


def update(app):
    #Updates the board matrix with translation, rotation, and offset
    for i in range(-app.dimensions, app.dimensions+1):
        for j in range(app.dimensions+1):
            x, y, z = app.map[i+app.dimensions][j]
            app.board[i+app.dimensions][j] = moveCamera(*rotate(*translate(x, y, z, app), app), app)

def translate(x, y, z, app):
    #Translates each point
    return x-app.pX, y, z - app.pZ

def rotate(x, y, z, app):
    #Rotates a point
    x, z = (x*math.cos(app.pDt + app.delayAngle) + z*math.sin(app.pDt + app.delayAngle), z * 
                math.cos(app.pDt + app.delayAngle) - x * 
                math.sin(app.pDt + app.delayAngle))
    y, z = (y*math.cos(app.pDty) + z*math.sin(app.pDty), z * 
                math.cos(app.pDty) - y * math.sin(app.pDty))
    x, z = (x*math.cos(app.pT) + z*math.sin(app.pT), z * 
                math.cos(app.pT) - x * math.sin(app.pT))
    return x, y, z

def moveCamera(x, y, z, app):
    #Factors in teh distance between player and camera positions
    return x, y, z + app.cameraDistance

def toPlane(app, x, y, z):
    #Converts a 3c point into a 2d one
    return (x/z*app.xscale+app.width/2, -y/z*app.yscale+app.height/2)
            
def canMove(app):
    #Makes an object move only in the intersections of lines
    b = False
    scaleAmount = app.width/(app.dimensions)
    if app.pX % (scaleAmount) == app.pZ % (scaleAmount) == 0:
        b = True
        intersectsTrail(app)
        if len(app.moves) > 0:
            temppDp, temppDt, tempdelayA = app.moves.pop(0)
            app.pDp = app.pDp + temppDp
            app.pDt = app.pDt + temppDt
            app.delayAngle = app.delayAngle + tempdelayA
        if app.justOn:
            app.trail.append((app.pX, app.pZ, app.pastX, app.pastZ, "PaleTurquoise"))
            if app.justOn != app.isOn:
                app.justOn = False
        app.pastX, app.pastZ = app.pX, app.pZ
    if app.isOn:
        app.playerT[:4] = [app.pastX, app.pastZ, app.pX, app.pZ]
    else:
        app.playerT[:4] = [0, 0, 0, 0]
    return b
    


def isAlive(app):
    #Checks if the player goes off the edge
    app.alive = abs(
        app.pX) <= app.width and app.pZ >= 0 and app.pZ <= app.width



def screenPoint(x0, y0, x1, y1, app):
    #Truncates a line to the segment with limits of the window
    valid1 = validPoint(x0, y0, app.width, app.height)
    valid2 = validPoint(x1, y1, app.width, app.height)
    if True in valid1 and True in valid2:
        index1 = valid1.index(True)
        index2 = valid2.index(True)
        if valid1[index1] == valid2[index1] or valid1[index2] == valid2[index2]:
            return False
    point = [(0, (y1-y0)/(x1-x0)*(0 - x1)+y1) if x1 - x0 != 0 else (0, 0), (app.width, (y1-y0)/(x1-x0)*(app.width - x1)+y1) if x1 - x0 != 0 else (0, 0),
             ((x1-x0)/(y1-y0)*(0 - y1)+x1, 0) if y1 - y0 != 0 else (00, 0), ((x1-x0)/(y1-y0)*(app.height - y1)+x1, app.height) if y1 - y0 != 0 else (0, 0)]
    if True in valid1:
        x0, y0 = point[valid1.index(True)]

    if True in valid2:
        x1, y1 = point[valid2.index(True)]
    return x0, y0, x1, y1



def validPoint(x, y, width, height):
    #Check if a point is in the window
    return (0 > x, x > width, 0 > y, y > height)



def distance(app, x, z):
    #Cancuylates the distance squared of a point to player positions
    xcamera, zcamera = app.cameraDistance*math.sin(app.pDt+app.delayAngle+app.pT), -app.cameraDistance*math.cos(app.pDt+app.delayAngle+app.pT)
    return ((x-app.pX-xcamera)**2 + (z-app.pZ-zcamera)**2)



def sort(app):
    #Sorts each trail polygon depending on its distance to the player
    app.indexes = []
    ind = set()
    for i in range(len(app.trail)):
        temp = -1
        value = 0
        for j in range(len(app.trail)):
            x = distance(app, *app.trail[j][:2])
            if x > temp and not j in ind:
                temp = x
                value = j
        ind.add(value)
        app.indexes.append(value)
            


def intersectsTrail(app):
    #Checks if the player hits the trail
    if Enemy.isin((app.pX, app.pZ), app.trail):
        app.alive = False
    


def timerFired(app):
    #Updates everything with time
    if app.rules:
        app.ruleTexts.incrementer(1)
    elif app.game:
        if app.alive:
            isAlive(app)
            if app.justBoost > 0:
                app.justBoost = app.justBoost - 1
                app.pS = 6
            else:
                app.pS = 3
            if canMove(app):
                if app.pDp % 4 == 0:
                    app.pSx = app.pS
                    app.pSz = 0
                elif app.pDp % 4 == 1:
                    app.pSx = 0
                    app.pSz = app.pS
                elif app.pDp % 4 == 2:
                    app.pSx = -app.pS
                    app.pSz = 0
                elif app.pDp % 4 == 3:
                    app.pSx = 0
                    app.pSz = -app.pS
            app.pX = app.pX + app.pSx
            app.pZ = app.pZ + app.pSz
            if abs(app.delayAngle) > 0.1:
                app.delayAngle = app.delayAngle - (abs(app.delayAngle)//app.delayAngle) * app.changeAngle
                if(app.delayAngle > 0):
                    app.delayAngle = app.delayAngle % (2*math.pi)
                else:
                    app.delayAngle = app.delayAngle % (-2*math.pi)
            else:
                app.delayAngle = 0
            enemyFrame(app)
            if app.just > 0:
                app.just = app.just - 1
            sort(app)
        else:
            app.pX = 0
            app.pZ = app.height/2
            app.pDty = 0
            app.pT = app.pT + 0.01
            app.playerWin.incrementer(1)
            app.enemyWin.incrementer(1)
            sort(app)
            if app.playerWin.increment > 500 or app.playerWin.skip > 16:
                appStarted(app)
        
        update(app)
    

def enemyFrame(app):
    #Updates the enemy every tick of timerFired
    app.enemy.move()
    app.enemy.doesItIntersect()
    app.enemy.produceTrail()
    app.enemy.guess()
    if (app.enemy.pX, app.enemy.pZ) == (30, 210):
        app.enemy.change = True
        app.enemy.changeCardinal()
        app.enemy.changeCardinal()
        app.enemy.changeCardinal()
        app.enemy.change = False 
    elif app.enemy.pX % app.enemy.scale == 0 and app.enemy.pZ % app.enemy.scale == 0:
        if (Enemy.isin(app.enemy.simulate(), app.trail)):
            app.enemy.change = True
            app.enemy.changeCardinal()
            if (Enemy.isin(app.enemy.simulate(), app.trail)):
                app.enemy.changeCardinal()
                app.enemy.changeCardinal()
            app.enemy.change = False
        elif (app.enemy.pX, app.enemy.pZ) == (210, 210)  or (app.enemy.pX, app.enemy.pZ) == (-570, 420) or app.enemy.change:
            app.enemy.change = True
            app.enemy.changeCardinal()
            if (Enemy.isin(app.enemy.simulate(), app.trail)):
                app.enemy.changeCardinal()
                app.enemy.changeCardinal()
                if (Enemy.isin(app.enemy.simulate(), app.trail)):
                    app.enemy.changeCardinal()
            app.enemy.change = False
        elif (abs(app.enemy.pX) < 570 and 100 < app.enemy.pZ < 570):
            x = random.randint(0, 20)
            if x > 5:
                if x == 6:
                    app.enemy.change = True
                    app.enemy.changeCardinal()
                    app.enemy.changeCardinal()
                    app.enemy.changeCardinal()
                    app.enemy.change = False 
                elif x == 7:
                    app.enemy.change = True
                    app.enemy.changeCardinal()
                    app.enemy.change = False 
    if not app.enemy.alive:
        app.alive = False



def keyReleased(app, event):
    #Updates angle with turns and is where features are
    if app.game:
        #Responds to keys
        if app.alive:
            #the moves in the future are deleted with x pressed
            if event.key == "x":
                app.moves = []
            elif event.key == "t":
                app.just = 5
                app.isOn = not app.isOn
                if not app.justOn:
                    app.justOn = True
            elif event.key == "b":
                if 0 < app.boost:
                    app.boost = app.boost - 1
                    app.justBoost = 20
            if event.key == "a":
                app.moves.append((1, math.pi/2, -math.pi/2))
            elif event.key == "d":
                app.moves.append((-1, - math.pi/2, math.pi/2))
            update(app)
        if event.key == "Space":
            app.playerWin.skip = app.playerWin.skip + 3
            app.enemyWin.skip = app.enemyWin.skip + 3
    elif app.rules and event.key == "Space":
        app.ruleTexts.skip = app.ruleTexts.skip + 3



def mouseMoved(app, event):
    #Updates the viewing angle
    if app.game:
        if app.alive:
        #Can change the angle of camera
            x = app.width - event.x-app.width/2
            app.pT = math.pi*x/2/app.width % (2*math.pi)
            y = -(app.height - event.y-app.height/2)
            if y < 0:
                y = 0
            app.pDty = math.pi*y/8/app.height
            update(app)
    elif app.rules:
        #Checks if cursor is on a button
        if app.back.inPoint(event.x, event.y):
            app.back.expand = True
        else:
            app.back.expand = False
    else:
        #Checks if mouse is on a button
        if app.playGame.inPoint(event.x, event.y):
            app.playGame.expand = True
        else:
            app.playGame.expand = False
        if app.playRules.inPoint(event.x, event.y):
            app.playRules.expand = True
        else:
            app.playRules.expand = False



def mousePressed(app, event):
    #Checks clicking button
    if not app.game:
        
        if app.rules:
            if app.back.inPoint(event.x, event.y):
                appStarted(app)
        else:
            if app.playGame.inPoint(event.x, event.y):
                app.game = True
            if app.playRules.inPoint(event.x, event.y):
                app.rules = True



def redrawAll(app, canvas):
    #Redraws everything
    if app.game:
        #Draws the grid and player and enemy
        drawMap(app, canvas)
        drawTrail(app, canvas)
        if app.alive and not app.isOn:
            drawPlayer(app, canvas)
        drawMargin(app, canvas)
    elif app.rules:
        #Draws teh rules
        canvas.create_rectangle(2, 2, app.width-2, app.height-2, fill = "gray1", width = 2)
        canvas.create_rectangle(0, 20, app.width*2/3, 30, fill = "green2", outline = "green2")
        app.ruleTexts.drawText(canvas)
        app.back.drawRectangle(canvas)
    else:
        #Draws the start screen
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.home))
        app.playGame.drawRectangle(canvas)
        app.playRules.drawRectangle(canvas)

    

def drawMap(app, canvas):
    #Draws the grid
    canvas.create_rectangle(0, 0, app.width, app.height, fill="black")
    for i in range(1, len(app.map)):
        for j in range(1, len(app.map[0])):
            x0, y0, z0 = app.board[i-1][j-1]
            x1, y1, z1 = app.board[i][j-1]
            x2, y2, z2 = app.board[i-1][j]
            x3, y3, z3 = app.board[i][j]
            if z0 > 0 and z1 > 0 and z2 > 0 and z3 > 0:
                x0, y0, x1, y1, x2, y2, x3, y3 = toPlane(app, x0, y0, z0) + toPlane(app, x1, y1, z1) + toPlane(app, x2, y2, z2) + toPlane(app, x3, y3, z3)
                canvas.create_polygon(
                    x0, y0, x1, y1, x3, y3, x2, y2, fill="grey4", outline="cornflower blue")



def drawTrail(app, canvas):
    #Draws the trails
    for trails in app.indexes:
        makeTrail(app, canvas, app.trail[trails])



def makeTrail(app, canvas, a):
    #Draws a polygon
    x = False
    y = False
    for j in range(0, 6, 5):
        j = j - app.cameraHeight
        y0 = y1 = j
        x0, z0, x1, z1, rgb = a
        x0, y0, z0, x1, y1, z1 = moveCamera(*rotate(*translate(x0, y0, z0, app), app), app) + moveCamera(*rotate(*translate(x1, y1, z1, app), app), app)
        if z0 > 0 and z1 > 0:
                x0, y0, x1, y1 = toPlane(app, x0, y0, z0) + toPlane(app, x1, y1, z1)
                b = screenPoint(x0, y0, x1, y1, app)
                if(b):
                    if x:
                        y = b[2:4] + b[0:2]
                    else:
                        x = b
    if x and y:
                canvas.create_polygon(x+y, fill = rgb + "1", outline = rgb + "4", width = 3)



def drawMargin(app, canvas):
    #Draws a margin and boosts
    canvas.create_rectangle(0, app.height, app.width, app.height-70, fill = "black", outline = "black")
    #Got this from cmu PIL
    canvas.create_image(app.width/2, app.height-35, image = ImageTk.PhotoImage(app.tron))
    if app.boost > 0:
        canvas.create_image(app.width-40, app.height-30, image = ImageTk.PhotoImage(app.boost1))
        if app.boost > 1:
            canvas.create_image(app.width-110, app.height-30, image = ImageTk.PhotoImage(app.boost1))
            if app.boost > 2:
                canvas.create_image(app.width-180, app.height-30, image = ImageTk.PhotoImage(app.boost1))
    if not app.alive:
        if not app.enemy.alive:
            app.playerWin.drawText(canvas)
        else:
            app.enemyWin.drawText(canvas)



def drawPlayer(app, canvas):
    #Draws the player position
    canvas.create_oval(app.width/2-10, app.height/2+app.cameraHeight/app.cameraDistance*app.yscale+10,
                            app.width/2+10, app.height/2 + app.cameraHeight/app.cameraDistance*app.yscale-10, fill="PaleTurquoise1", outline = "PaleTurquoise4", width = 2)



def main():
    #Runs the program
    runApp(width=600, height=600)

main()
