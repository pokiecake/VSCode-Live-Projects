import pygame
from pygame import mixer
import random
import time
import asyncio


# Intialize the pygame
pygame.init()

# create the screen
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

#Title and Icon
pygame.display.set_caption("Buffet Wars")
icon = pygame.image.load("Assets/turkey.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("Sprites/bob.png")
playerImg = pygame.transform.scale(playerImg,(125,196))
playerW = playerImg.get_width()
playerH = playerImg.get_height()
playerX = 370
playerY = 350
playerX_change = 0
playerY_change = 0
playerSpeed = 3
playerDirection = 0
currentRoom = 1

#Apple
appleImg = pygame.image.load("Assets/Apple.png")
appleW = appleImg.get_width()
appleH = appleImg.get_height()

#Apple Bullets
apple_state = "ready"
bullets = []
appleBulletX = 0
appleBulletY = 0
apple_changeX = 0
apple_changeY = 0
appleBulletCount = 0

#Apple Stockpiles
stockpiles = []
stockpilesTimes = [-2]

#Background
background = pygame.Surface((screenWidth, screenHeight))

BGImage = pygame.image.load("Assets/spongebob.png")

BGImage = pygame.transform.scale(BGImage,(screenWidth, screenHeight))

# camera setup

def player(x, y):
    screen.blit(playerImg, (x, y))

def apple(x, y):
    screen.blit(appleImg, (x, y))

#doesn't actually fire apples, only creates them and their positions
def fire_apple(x, y):
    global apple_state
    global appleBulletX
    global appleBulletY
    global apple_changeX
    global apple_changeY
    global bullets
    apple_state = "fire"
    xPos = x
    yPos = y
    #0 is up, 1 is right, 2 is down, 3 is left
    match(playerDirection):
        case 0:
            yPos -= appleH
            xPos += (playerW - appleW) / 2
            apple_changeX = 0
            apple_changeY = -7
            pass
        case 1:
            yPos += (playerH - appleH) / 2
            xPos += playerW + appleW
            apple_changeX = 7
            apple_changeY = 0
            pass
        case 2:
            yPos += playerH + appleH
            xPos += (playerW - appleW) / 2
            apple_changeX = 0
            apple_changeY = 7
            pass
        case 3:
            yPos += (playerH - appleH) / 2
            xPos -= appleW
            apple_changeX = -7
            apple_changeY = 0
            pass
    #sets the apple bullet's position based on the direction
    appleBulletX = xPos
    appleBulletY = yPos
    bullet = AppleBullets(xPos, yPos, apple_changeX, apple_changeY)
    bullets.append(bullet)

#draws anything apple related
def draw_apple(x, y):
    screen.blit(appleImg, (x, y))

#spawns stockpile on cooldown
def spawn_apple_pile():
    x = random.randint(50, 750)
    y = random.randint(50, 550)
    s = AppleStockpiles(x, y, appleW, appleH)
    stockpiles.append(s)
    draw_apple(x, y)

def check_timeouts():
    sec = time.time()
    for sTime in stockpilesTimes:
        if sec > sTime + 1:
            spawn_apple_pile()
            stockpilesTimes.remove(sTime)

#class for apple bullets
class AppleBullets:
    def __init__(self, x, y, change_x, change_y):
        self.x = x
        self.y = y
        self.change_x = change_x
        self.change_y = change_y
    
    def change(self):
        self.x += self.change_x
        self.y += self.change_y
    
    def getPos(self):
        return (self.x, self.y)

#class for apple stockpiles
class AppleStockpiles:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    #checks for collision in the horizontal and vertical direction
    def checkCollision(self, pX, pY, pW, pH):
        if (pY < self.y + self.h and pY + pH > self.y):
            if (pX < self.x + self.w and pX + pW > self.x) or (pX + pW > self.x and pX < self.x + self.w):
                return True
    
    def getPos(self):
        return (self.x, self.y)

class Spawners:
    def __init__(self, type):
        self.type = type

#class for rooms
class Rooms:
    def __init__(self, connections):
        #connections will be an object that holds the room it can connect to and the direction (North, East, South, West) it connects from
        self.connections = connections


#background sound
mixer.music.load('Assets/Sky.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#Global Variable Setup
#Key Press Status & Contradict Speed (held down or not)
lefthold = False
righthold = False
uphold = False
downhold = False
#Controls speed when both opposite buttons pressed
stuckspeed = 0.0 * playerSpeed

#Game Loop. When the x button is clicked, running is set to false and the window closes.
running = True
while running:
    #creates a new stockpile if one hasn't been created
    check_timeouts()
    #Draws Purplish background. Unneeded due to spongebob background
    #screen.fill((150,0,150))

    #draws spongebob background
    #pygame.transform.scale_by(BGImage,20)
    #screen.blit(background, (0,0))
    screen.blit(BGImage, (0,0))

    


    #event listener
    for event in pygame.event.get():
        #stops the game when the x button is pressed
        if event.type == pygame.QUIT:
            running = False
        #handles key presses
        if event.type == pygame.KEYDOWN:
            #sets the x and y changes based on what is pressed
            #if both opposite directions are held, player moves slower at rate of stuckspeed
            if event.key == pygame.K_LEFT and righthold == False:
                playerX_change = -playerSpeed
                lefthold = True
            elif event.key == pygame.K_LEFT and righthold == True:
                playerX_change = stuckspeed
                lefthold = True
            if event.key == pygame.K_RIGHT and lefthold == False:
                playerX_change = playerSpeed
                righthold = True
            elif event.key == pygame.K_RIGHT and lefthold == True:
                playerX_change = -stuckspeed
                righthold = True

            if event.key == pygame.K_UP and downhold == False:
                playerY_change = -playerSpeed
                uphold = True
            elif event.key == pygame.K_UP and downhold == True:
                playerY_change = stuckspeed
                uphold = True
            if event.key == pygame.K_DOWN and uphold == False:
                playerY_change = playerSpeed
                downhold = True
            elif event.key == pygame.K_DOWN and uphold == True:
                playerY_change = -stuckspeed
                downhold = True
            
            #changes the direction of the player's shooting
            if event.key == pygame.K_w:
                playerDirection = 0
            if event.key == pygame.K_d:
                playerDirection = 1
            if event.key == pygame.K_s:
                playerDirection = 2
            if event.key == pygame.K_a:
                playerDirection = 3
            if event.key == pygame.K_SPACE:
                if appleBulletCount > 0:
                    fire_apple(playerX, playerY)
                    appleBulletCount -= 1
        #handles key lifts
        if event.type == pygame.KEYUP:
            #stops changes after corresponding keys are lifted given that no other key is held
            #if the other direction is held, direction immediately switches to match
            if event.key == pygame.K_LEFT and righthold == True:
                playerX_change = playerSpeed
                lefthold = False
            elif event.key == pygame.K_RIGHT and lefthold == True:
                playerX_change = -playerSpeed
                righthold = False
            elif event.key == pygame.K_RIGHT:
                righthold = False
                playerX_change = 0
            elif event.key == pygame.K_LEFT:
                lefthold = False
                playerX_change = 0

            if event.key == pygame.K_UP and downhold == True:
                playerY_change = playerSpeed
                uphold = False
            elif event.key == pygame.K_DOWN and uphold == True:
                playerY_change = -playerSpeed
                downhold = False
            elif event.key == pygame.K_DOWN:
                downhold = False
                playerY_change = 0
            elif event.key == pygame.K_UP:
                uphold = False
                playerY_change = 0

    #changes the player's position
    playerX += playerX_change
    playerY += playerY_change

    #snaps the player to a boundary
    if playerX <= 0:
        playerX = 0
    elif playerX + playerW >= screenWidth:
        playerX = screenWidth - playerW
    if playerY <= 0:
        playerY = 0
    elif playerY + playerH >= screenHeight:
        playerY = screenHeight - playerH
    
    #Bullet movement
    for bullet in bullets:
        bullet.change()
        pos = bullet.getPos()
        x = pos[0]
        y = pos[1]
        draw_apple(x, y)
        if x < 0 or x > screenWidth or y < 0 or y > screenHeight:
            bullets.remove(bullet)
            del bullet

    #checks for collision for all stockpiles
    for pile in stockpiles:
        pos = pile.getPos()
        draw_apple(pos[0], pos[1])
        #removes a pile if collided and adds to the apple bullet count
        if pile.checkCollision(playerX, playerY, playerW, playerH):
            stockpiles.remove(pile)
            del pile
            appleBulletCount += 1
            stockpilesTimes.append(time.time())

    #draws the players and apples
    player(playerX, playerY)
    pygame.display.update()