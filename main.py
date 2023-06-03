import pygame
from pygame import mixer
import random

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
playerImg = pygame.image.load("Assets/player.png")
playerW = playerImg.get_width()
playerH = playerImg.get_height()
playerX = 370
playerY = 350
playerX_change = 0
playerY_change = 0
playerSpeed = 2
playerDirection = 0

#Apple
appleImg = pygame.image.load("Assets/Apple.png")
appleX = random.randint(50, 750)
appleY = random.randint(50, 350)
apple_state = "ready"
appleBulletX = 0
appleBulletY = 0
apple_changeX = 0
apple_changeY = 0

#Background
background = pygame.image.load("Assets/spongebob.png")

def player(x, y):
    screen.blit(playerImg, (x, y))

def apple(x, y):
    screen.blit(appleImg, (x, y))

def fire_apple(x, y):
    global apple_state
    global appleBulletX
    global appleBulletY
    global apple_changeX
    global apple_changeY
    apple_state = "fire"
    xPos = x
    yPos = y
    match(playerDirection):
        case 0:
            yPos -= 25
            xPos += 25
            apple_changeX = 0
            apple_changeY = -7
            pass
        case 1:
            yPos += 50
            xPos += 30
            apple_changeX = 7
            apple_changeY = 0
            pass
        case 2:
            yPos += 150
            xPos += 25
            apple_changeX = 0
            apple_changeY = 7
            pass
        case 3:
            yPos += 50
            xPos -= 10
            apple_changeX = -7
            apple_changeY = 0
            pass
    appleBulletX = xPos
    appleBulletY = yPos

def draw_apple(x, y):
    screen.blit(appleImg, (x, y))

#background sound
mixer.music.load('Assets/Clouds.wav')
mixer.music.play(-1)

#Game Loop. When the x button is clicked, running is set to false and the window closes.
running = True
while running:

    #Draws Purplish background. Unneeded due to spongebob background
    screen.fill((150,0,150))

    #draws spongebob background
    screen.blit(background, (75,100))
    #event listener
    for event in pygame.event.get():
        #stops the game when the x button is pressed
        if event.type == pygame.QUIT:
            running = False
        #handles key presses
        if event.type == pygame.KEYDOWN:
            #sets the x and y changes based on what is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -playerSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change = playerSpeed
            if event.key == pygame.K_UP:
                playerY_change = -playerSpeed
            if event.key == pygame.K_DOWN:
                playerY_change = playerSpeed
            #changes the direction of the player
            if event.key == pygame.K_w:
                playerDirection = 0
            if event.key == pygame.K_d:
                playerDirection = 1
            if event.key == pygame.K_s:
                playerDirection = 2
            if event.key == pygame.K_a:
                playerDirection = 3
            if event.key == pygame.K_SPACE:
                fire_apple(playerX, playerY)
        #handles key lifts
        if event.type == pygame.KEYUP:
            #stops changes after corresponding keys are lifted
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
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
    if apple_state is "fire":
        appleBulletX += apple_changeX
        appleBulletY += apple_changeY
        draw_apple(appleBulletX, appleBulletY)

    #draws the players and apples
    player(playerX, playerY)
    apple(appleX, appleY)
    pygame.display.update()