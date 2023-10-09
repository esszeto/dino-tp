from cmu_112_graphics import *
import math
from math import pi
import decimal
import random
from random import randint


#################################
# STARTSCREEN MODE
#################################
def startScreenMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height*0.2, text="dino dash!",
                       font='"press start 2p" 16 bold', fill='black')
                        # font citation: https://fonts.google.com/specimen/Press+Start+2P
    canvas.create_image(app.width/1.45, app.height/2,image=ImageTk.PhotoImage(app.image1))
    canvas.create_text(app.width*0.29, app.height/2, text = "instructions:\n\n"+
                       "1. select a location\non the globe" +
                       "\n\n2. press 'space' or\n'up' to start game " +
                       "and\nmake the dino jump\n\n3. press 'down' to make\nthe dino duck" +
                       "\n\n4. press 'q' to quit the\ngame at any time" +
                       "\n\n5. for each 250 points,\na powerup gets added to\nyour score!",
                       fill = 'black', font = '"press start 2p" 9')
    
    # drawing buttons on map
    canvas.create_oval(app.godesert.cx - app.godesert.r, app.godesert.cy - app.godesert.r, app.godesert.cx + app.godesert.r, app.godesert.cy + app.godesert.r, fill = "goldenrod")
    canvas.create_oval(app.goMountain.cx - app.goMountain.r, app.goMountain.cy - app.goMountain.r, app.goMountain.cx + app.goMountain.r, app.goMountain.cy + app.goMountain.r, fill = "lightblue")

def startScreenMode_mousePressed(app, event):
    dx = app.godesert.cx
    dy = app.godesert.cy
    dr = app.godesert.r
    if app.godesert.button_mousePressed(dx, dy, dr, event):
        app.terr_track = "desert"
        app.terr = Desert(app)
        app.mode = 'terrIntroMode'

    mx = app.goMountain.cx
    my = app.goMountain.cy
    mr = app.goMountain.r
    if app.goMountain.button_mousePressed(mx, my, mr, event):
        app.terr_track = "mountain"
        app.terr = Mountain(app)
        app.mode = 'terrIntroMode'

#################################
# TERRAIN INTRO SCREEN
#################################
def terrIntroMode_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text = (app.terr_track) +
                       " mode!\n\n\npress 'space' to begin " +
                       "\nor 'r' to return to the map",
                       font='"press start 2p" 10 bold', fill='black', justify = "center")

def terrIntroMode_keyPressed(app, event):
    if (event.key == "Up" or event.key == "Space"):
        app.mode = 'gameMode'
    
    if (event.key == "r"):
        app.mode = 'startScreenMode'

#################################
# DEFAULT GAME MODE
#################################
def gameMode_redrawAll(app, canvas):
    app.terr.drawTerrain(app, canvas)
    
    # score counter
    canvas.create_text(app.width*0.72, app.height*0.1, text="HI",
                       font='"press start 2p" 9 bold', fill='black')
    canvas.create_text(app.width*0.81, app.height*0.1, text=int(app.high_score),
                       font='"press start 2p" 9 bold', fill='black')
    canvas.create_text(app.width*0.89, app.height*0.1, text=int(app.curr_score),
                       font='"press start 2p" 9 bold', fill='black')    
    
    # dino drawing
    if not app.dino.isDucking:
        sprite = app.sprites[app.run_spriteCounter]
        canvas.create_image(30, app.dino.y, image=ImageTk.PhotoImage(sprite))
    else:
        sprite_duck = app.duck_sprites[app.duck_spriteCounter]
        canvas.create_image(30, app.dino.y, image=ImageTk.PhotoImage(sprite_duck))


def gameMode_keyPressed(app, event):
    if (event.key == "Up" or event.key == "Space"):
        #app.dy = 15
        app.dino.isJumping = True
    
    if (event.key == "Down"):
        app.dino.isDucking = True
    
    # to quit mid-game
    if (event.key == "q"):
        app.mode = 'gameOverMode'


def gameMode_keyReleased(app, event):
    if app.dino.isDucking:
        app.dino.isDucking = False
    

def gameMode_timerFired(app):    
    if app.terrlen_counter == 37:
        app.terr.heights.pop(0)
        app.terr.heights.pop(0)
        resetdinoCounter(app)
    
    if app.terr_track == "mountain":
        if len(app.terr.heights) == 64:
            app.terr.heights.extend(app.terr.genTerrain([(app.width*4, app.terr.randH), (app.width*8, app.terr.randH)], app.terr.startR))
    elif app.terr_track == "desert":
        if len(app.terr.heights) % 60 == 0:
            app.terr.heights.extend(app.terr.genTerrain([(app.width*2, app.terr.randH), (app.width*4, app.terr.randH)], app.terr.startR))
    
    app.terrlen_counter += 1
    
    # dino jump
    if app.dino.isJumping:
        app.dino.dinoJump(app)
    else:
        app.dino.updatePos(app)

    # to generate new terrain (visually, moving it over)
    newPoints = []
    for x, y in app.terr.heights:
        newPoints.append((x-2, y))
    app.terr.heights = newPoints

    # dino duck
    if app.dino.isDucking == False:
        app.run_spriteCounter = (1 + app.run_spriteCounter) % len(app.sprites) # running

    # for dino sprite to keep running
    if app.dino.isDucking == False:
        app.run_spriteCounter = (1 + app.run_spriteCounter) % len(app.sprites) # running
    elif app.dino.isDucking:
        app.duck_spriteCounter = (1 + app.duck_spriteCounter) % len(app.duck_sprites) # ducking
        
    # bird sprite flying
    app.bird_spriteCounter = (1 + app.bird_spriteCounter) % len(app.bird_sprites) # flying
    
    # cactus spawning
    if app.terr_track == "desert":
        for pos in app.cactusXPos:
            pos.timerFired(app)
            if (pos.x < app.dino.x) and cactus_collision(app, pos):
                app.mode = 'gameOverMode'

        app.counter_ca += 1
        if app.counter_ca == app.rand_cactus: 
            newHeight = app.terr.heights[16][1] - app.img2.height/4
            newCactus = Cactus(app, xPos = app.width - 1, yPos = newHeight)
            app.cactusXPos.append(newCactus)
            resetcactiCounter(app)
    
    # shrub spawning
    if app.terr_track == "mountain":
        for pos in app.shrubXPos:
            pos.timerFired(app)

        app.counter_ca += 1
        if app.counter_ca == app.rand_shrub: 
            newHeight = app.terr.heights[16][1] + app.rock_img2.height/3
            newShrub = Shrub(app, xPos = app.width - 1, yPos = newHeight)
            app.shrubXPos.append(newShrub)
            resetcactiCounter(app)
            
        # goat spawning
        for pos in app.goatXPos:
            pos.timerFired(app)
            if (pos.x - 5 < app.dino.x) and goat_collision(app, pos): # needs to be fixed
                app.mode = 'gameOverMode'
            
        app.counter_goat += 1
        if app.counter_goat == app.rand_goat: 
            newHeight = app.terr.heights[16][1] + app.goat_img.height/3
            newGoat = Goat(app, xPos = app.width - 1, yPos = newHeight)
            app.goatXPos.append(newGoat)
            resetgoatCounter(app)

    # cloud spawning
    for cloud in app.cloudXPos:
        cloud.timerFired(app)
    app.counter_cl += 1
    if app.counter_cl == app.rand_cloud:
        newHeight = random.randint(app.height*0.2, app.height*0.35)
        newCloud = Cloud(app, xPos = app.width * 0.9, yPos = newHeight)
        app.cloudXPos.append(newCloud)
        resetCounter(app)
    
    # bird spawning
    for bird in app.birdXPos:
        bird.timerFired(app)
        if (bird.x < app.dino.x) and bird_collision(app, bird):
            app.mode = 'gameOverMode'

    app.counter_bird += 1
    if app.counter_bird == app.rand_bird:
        newHeight1 = random.randint(app.height*0.1, app.height*0.18)
        newHeight2 = random.randint(app.height*0.35, int(app.height/2.1))
        newBird = Bird(app, xPos = app.width * 0.9, yPos = random.choice([newHeight1, newHeight2]))
        app.birdXPos.append(newBird)
        resetCounter(app)

    # checks for powerup every 300 points
    app.curr_score += 0.3
    checkBonus(app)
    
#################################
# resetting counters
def resetcactiCounter(app):
    app.counter_ca = 0
    app.rand_cactus = random.randint(100, 300)
    app.rand_shrub = random.randint(150, 300)

def resetgoatCounter(app):
    app.counter_goat = 0
    app.rand_goat = random.randint(150, 800)

def resetCounter(app):
    app.counter_cl = 0
    app.rand_cloud = random.randint(20, 250)
    app.counter_bird = 0
    app.rand_bird = random.randint(60, 500)

def resetdinoCounter(app):
    app.terrlen_counter = 0

def checkBonus(app):
    if int(app.curr_score) % 300 == 0 and app.curr_score > 10:
        bonus = app.jumpCounter*5
        app.curr_score += bonus
        app.jumpCounter = 0

#################################
# GAMEOVERSCREEN MODE
#################################

def gameOverMode_redrawAll(app,canvas):
    canvas.create_text(app.width/2, app.height/3.9, text="G A M E  O V E R !",
                    fill='black', font = '"press start 2p" 13 bold')
    canvas.create_text(app.width/2, app.height/3.2, text="SCORE = " + str(int(app.curr_score)),
                    fill='black', font = '"press start 2p" 9 bold')
    canvas.create_text(app.width/2, app.height/2.7, text="PREVIOUS HIGH SCORE = " + str(int(app.high_score)),
                    fill='black', font = '"press start 2p" 9 bold')
    canvas.create_text(app.width/2, app.height/2.3, text="press 'c' to run again "
                       + "in this terrain", fill='black', font = '"press start 2p" 8')
    canvas.create_text(app.width/2, app.height/2.1, text="OR... press 'r' to return to the starting screen\nand choose another location!",
                    fill='black', font = '"press start 2p" 8', justify = "center")
    canvas.create_image(app.width/2, app.height*0.7, image = ImageTk.PhotoImage(app.sprites[2]))

def gameOverMode_keyPressed(app, event):        
    if (event.key == "c"):
        if app.high_score < app.curr_score:
            app.high_score = app.curr_score
        app.curr_score = 0
        baby_appStarted(app)
        app.mode = 'gameMode'

    if (event.key == "r"):
        app.mode = 'startScreenMode'
        app.curr_score = 0
        app.high_score = 0

#################################
# CLASSES
#################################

class Dino():
    def __init__(self, app):
        self.x = 37
        self.y = app.terr.heights[2][1] # - some amount for the dino
        self.dy = 15
        self.ddy = -0.8 # changes how high dino go
        self.isJumping = False
        self.isDucking = False
    
    def updatePos(self, app):
        self.y = app.terr.heights[2][1] # - some amount for the dino

    def dinoJump(self, app):
        og_ypos = self.y
        self.dy += self.ddy
        self.y -= self.dy

        if abs(self.y - og_ypos) > 100:
            self.y -= self.dy
        
        if app.dino.y > app.terr.heights[1][1]:
            self.dy = 15
            app.dino.y = app.terr.heights[1][1]
            app.dino.isJumping = False

    def dinoDuck(self, app):
        self.isDucking = True
    
class Cactus():
    def __init__(self, app, xPos, yPos):
        self.x = xPos
        self.y = app.terr.heights[16][1] - app.img2.height/4
        self.img2 = app.scaleImage((app.loadImage('cactus_single.png')), 1/4)
    
    def timerFired(self, app):
        self.x -= 5            
        if self.x < app.width*0.01:
            app.cactusXPos.remove(self)   
            app.jumpCounter += 1 # for powerup
    
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(app.img2))

class Shrub():
    def __init__(self, app, xPos, yPos):
        self.x = xPos
        self.y = app.terr.heights[16][1] # app.rock_img2.height/4
        self.rock_img2 = app.scaleImage((app.loadImage('rock_img2.png')), 1/35)
    
    def timerFired(self, app):
        self.x -= 2
        if self.x < app.width*0.01:
            app.shrubXPos.remove(self)   
    
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(app.rock_img2))

class Goat():
    def __init__(self, app, xPos, yPos):
        self.x = xPos
        self.y = app.terr.heights[16][1]
        self.goat_img = app.scaleImage((app.loadImage('goat_img.png')), 1/27)
    
    def timerFired(self, app):
        self.x -= 2
        if self.x < app.width*0.01:
            app.goatXPos.remove(self)
            app.jumpCounter += 1 # for powerup
    
    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(app.goat_img))

class Cloud():
    def __init__(self, app, xPos, yPos):
        self.x = xPos
        self.y = yPos
        self.img3 = app.scaleImage((app.loadImage('cloud_screenshot.png')), 1/6)

    def drawCharacter(app, canvas):
        for x in app.cloudXPos:
            canvas.create_image(x - app.scrollX, app.height/5, image = ImageTk.PhotoImage(app.img3))
            
    def timerFired(self, app):
        self.x -= 2.5
        if self.x < app.width*0.1:
            app.cloudXPos.remove(self)

    def redraw(self, app, canvas):
        canvas.create_image(self.x, self.y, image = ImageTk.PhotoImage(self.img3))

class Bird():
    def __init__(self, app, xPos, yPos):
        self.x = xPos
        self.y = yPos
        self.img_bird = app.scaleImage((app.loadImage('bird_img.png')), 1/30)
    
    def timerFired(self, app):
        self.x -= 4
        if self.x < app.width*0.01:
            app.birdXPos.remove(self)   

    # image source: https://img.itch.zone/aW1hZ2UvNTA5MzIwLzI2NDIzNTcucG5n/347x500/%2FqbQKf.png
    def redraw(self, app, canvas):
        sprite_bird = app.bird_sprites[app.bird_spriteCounter]
        canvas.create_image(self.x, self.y, image=ImageTk.PhotoImage(sprite_bird))


##################################
# TERRAIN GENERATION
##################################

class Terrain():
    def __init__(self, app):
        self.r = 0
        self.heights = self.genTerrain([(0, app.height), (app.width - 1, app.height)], 0)

    def genTerrain(self, m, r):
        return [(0, 0), (0, 0), (0, 0), (0, 0)]

class Desert(Terrain):
    def __init__(self, app):
        super().__init__(app)
        self.startR = 0
        self.randH = random.randint(int(app.height/1.9), int(app.height/1.9 + 1))
        self.heights = self.genTerrain([(0, self.randH), (app.width*2, self.randH)], self.startR)
    
    def genTerrain(self, m, r):
        if (m[1][0] - m[0][0]) < 40:
            return [(m[0][0], m[0][1]), (m[1][0], m[1][1])]
        else:
            cx = (m[0][0] + m[1][0]) // 2
            cy = m[0][1]
            
            L = self.genTerrain([(m[0][0], m[0][1]), (cx, cy)], 0)
            R = self.genTerrain([(cx, cy), (m[1][0], m[1][1])], 0)
            
            return L + R
        
    def drawTerrain(self, app, canvas):        
        for i in range(len(self.heights) - 1):
            canvas.create_line(self.heights[i][0], int(self.heights[i][1]), self.heights[i+1][0], int(self.heights[i+1][1]), fill = "black")

        # cactus drawing
        # image credit: https://www.programmersought.com/article/93434919643/
        for pos in app.cactusXPos:
            pos.redraw(app, canvas)
        
        # cloud drawing
        # image credit: https://miro.medium.com/freeze/max/600/1*82D2cg8Gpe9CVISaph6RPg.gif
        for cloud in app.cloudXPos:
            cloud.redraw(app, canvas)
        
        # bird drawing
        for bird in app.birdXPos:
            bird.redraw(app, canvas)

# midpoint displacement algorithm source:
# https://learn.64bitdragon.com/articles/computer-science/procedural-generation/midpoint-displacement-in-one-dimension
class Mountain(Terrain):
    def __init__(self, app):
        super().__init__(app)
        self.randH = random.randint(app.height/2 - 50, app.height/2 + 100)
        self.startR = 100
        self.heights = self.genTerrain([(0, self.randH), (app.width * 4, self.randH)], self.startR)
    
    def genTerrain(self, m, r):
        # m is the list of the two starting tuples
        if (m[1][0] - m[0][0]) < 40:
            return [(m[0][0], m[0][1])]

        else:
            cx = (m[0][0] + m[1][0]) // 2
            low = min(m[0][1], m[1][1])
            high = max(m[0][1], m[1][1])
            cy = random.randint(low, high)
            cy += random.randint(-r, r)
            
            L = self.genTerrain([(m[0][0], m[0][1]), (cx, cy)], r//2)
            R = self.genTerrain([(cx, cy), (m[1][0], m[1][1])], r//2)
            
            return L + R
        
    def drawTerrain(self, app, canvas):
        for i in range(len(self.heights) - 1):
            canvas.create_line(self.heights[i][0], int(self.heights[i][1]), self.heights[i+1][0], int(self.heights[i+1][1]), fill = "black")

        # shrub drawing
        for pos in app.shrubXPos:
            pos.redraw(app, canvas)
        
        # goat drawing
        for pos in app.goatXPos:
            pos.redraw(app, canvas)
        
        # cloud drawing
        for cloud in app.cloudXPos:
            cloud.redraw(app, canvas)
        
        # bird drawing
        for bird in app.birdXPos:
            bird.redraw(app, canvas)

    
#################################
# COLLISION FUNCTIONS
##################################

def cactus_collision(app, pos):
    if (((app.dino.x + app.sprites[0].width/2) > (pos.x - app.img2.width//2)) and
        (abs(app.dino.y + app.sprites[0].height/2) > abs(pos.y - app.img2.height//2))):

        app.gameOver = True
        app.mode = 'gameOverMode'
        return True

def goat_collision(app, pos):
    if (((app.dino.x + app.sprites[0].width/2) > (pos.x - app.goat_img.width//2)) and
        (abs(app.dino.y + app.sprites[0].height/2) > abs(pos.y - app.goat_img.height//2))):

        app.gameOver = True
        app.mode = 'gameOverMode'
        return True

def bird_collision(app, pos):
    if not app.dino.isDucking: # running
        if (((app.dino.x + app.sprites[0].width/2) > (pos.x - app.bird_img.width//2)) and
        (abs(app.dino.y - app.sprites[0].height/2) < abs(pos.y + app.bird_img.height//2))):
            # print(f'dino x = {app.dino.x + app.sprites[0].width/2}')
            # print(f'bird x = {pos.x - app.bird_img.width//2}')
            # print(f'dino y = {app.dino.y - app.sprites[0].height/2}')
            # print(f'bird y = {pos.y + app.bird_img.height//2}')
        
            app.gameOver = True
            app.mode = 'gameOverMode'
            return True

    else: # ducking
        if (((app.dino.x + app.duck_img.width/2) > (pos.x - app.bird_img.width//2)) and
        ((app.dino.y - app.duck_img.height ) < (pos.y + app.bird_img.height//2))):
            app.gameOver = True
            app.mode = 'gameOverMode'
            return True

#################################
# BUTTONS FOR START SCREEN
#################################

class Button():
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
            
    def button_mousePressed(app, cx, cy, r, event):
        disX = cx - event.x
        disY = cy - event.y
        if (math.sqrt(disX**2 + disY**2) <= r):
            return True

# includes image sources
def appStarted(app):
    # game opens with startScreenMode
    app.mode = "startScreenMode"
    app.terr_track = ""

    # map image source: https://www.freeiconspng.com/thumbs/world-map-png/world-map-png-17.png
    app.image1 = app.loadImage('Picsart_22-11-18_19-07-11-561.png')
    app.img2 = app.scaleImage((app.loadImage('cactus_single.png')), 1/4)
    # rock image source: https://w7.pngwing.com/pngs/759/478/png-transparent-brown-rock-illustration-pixel-art-sprite-rocks-brown-painting-8bit-color.png
    app.rock_img2 = app.scaleImage((app.loadImage('rock_img2.png')), 1/35)
    # arch image source: https://www.upr.org/science/2019-02-25/science-utah-upr-announces-new-podcast
    app.goat_img = app.scaleImage((app.loadImage('goat_img.png')), 1/27)
    
    app.img_cloud = app.scaleImage((app.loadImage('cloud_screenshot.png')), 1/6)
    
    # establishing the terrain instance
    app.terr = Terrain(app)
    
    # sprite gen code derived from 112 lecture notes
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
    # running spritestrip
    # image credit: not ducking -- https://24glo.com/img/game/dino/2x-trex.png
    spritestrip = app.scaleImage((app.loadImage('trex_sprite.png')), 1/2.4)
    app.sprites = []
    for i in range(3):
        sprite = spritestrip.crop((37*i, 0, 37+37*i, 50))
        app.sprites.append(sprite)
    app.run_spriteCounter = 0
    
    # ducking spritestrip
    # https://trex-runner.fandom.com/wiki/Lonely_T-Rex?file=Trexsprite.jpg
    app.duck_img = app.scaleImage((app.loadImage('dinoducksprite.png')), 1/2.4)
    spritestrip = app.scaleImage((app.loadImage('dinoducksprite.png')), 1/2.4)
    app.duck_sprites = []
    for i in range(2):
        sprite = spritestrip.crop((52*i, 0, 52+52*i, 18))
        app.duck_sprites.append(sprite)
    app.duck_spriteCounter = 0
    
    # bird flying spritestrip
    app.bird_img = app.scaleImage((app.loadImage('bird_sprite4.png')), 1/2.4)
    spritestrip = app.scaleImage((app.loadImage('bird_sprite4.png')), 1/2.4)
    app.bird_sprites = []
    for i in range(4):
        sprite = spritestrip.crop((38*i, 0, 38+38*i, 84))
        app.bird_sprites.append(sprite)
    app.bird_spriteCounter = 0
    
    app.high_score = 0
    app.curr_score = 0 # how to print this as '00000' initially rather than 0
    
    app.timerDelay = 5
    
    app.gameOver = False
    
    app.isRunning = False
    
    app.gravity = -5.2
    app.counter_ca = 0
    app.counter_cl = 0
    app.counter_bird = 0
    app.counter_goat = 0
    app.terrlen_counter = 0
    
    app.counter_pu = 0 # powerup score timer
    app.showScore = False
        
    app.dino = Dino(app)
    app.cactusX = 0
    app.cactusXPos = [] # keeps track of cactus x positions for mvmt
    app.cloudXPos = [] # keeps track of clouds
    app.birdXPos = [] # keeps track of birds
    app.shrubXPos = [] # keeps track of rocks
    app.goatXPos = [] # keeps track of goats
    app.letterXPos = [] # keeps track of powerup letters
    
    mountain_appStarted(app) # calls mountain_appStarted for mountain instance
    
    # for spawning instances of these objects
    app.rand_cactus = random.randint(60, 300)
    app.rand_cloud = random.randint(20, 400)
    app.rand_bird = random.randint(60, 400)
    app.rand_shrub = random.randint(75, 400)
    app.rand_goat = random.randint(150, 800)
    
    app.jumpCounter = 0 # for the powerup
    
    app.m = []
    app.r = 100
        
    # app.buttons = []
    app.godesert = Button(app.width*0.7, app.height/2, 5) # goes to desert mode
    app.goMountain = Button(app.width*0.55, app.height/2.23, 5) # goes to mountain mode


# mountain terrain gen app started
def mountain_appStarted(app):
    # app.heights = Mountain(app).genTerrain(app)
    app.randH = random.randint(app.height/2, app.height/2 + 200)
    app.r = 100

def baby_appStarted(app):
    app.mode = "gameMode"
    app.cactusXPos = []
    app.shrubXPos = []
    app.goatXPos = []
    app.cloudXPos = []
    app.birdXPos = []
    app.jumpCounter = 0
    
    if app.terr_track == "mountain":
        if len(app.terr.heights) == 16:
            app.terr.heights.extend(app.terr.genTerrain([(app.width*2, app.terr.randH), (app.width*4, app.terr.randH)], app.terr.startR))
    elif app.terr_track == "desert":
        if len(app.terr.heights) % 60 == 0:
            app.terr.heights.extend(app.terr.genTerrain([(app.width*2, app.terr.randH), (app.width*4, app.terr.randH)], app.terr.startR))
    

runApp(width=600, height=400)