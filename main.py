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

#Apple Bullet
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
    #0 is up, 1 is right, 2 is down, 3 is left
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
    #sets the apple bullet's position based on the direction
    appleBulletX = xPos
    appleBulletY = yPos

def draw_apple(x, y):
    screen.blit(appleImg, (x, y))

#background sound
mixer.music.load('Assets/Clouds.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#Global Variable Setup
#Key Press Status (held down or not)
lefthold = False
righthold = False
uphold = False
downhold = False

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
            #if both opposite directions are held, player stops
            if event.key == pygame.K_LEFT and righthold == False:
                playerX_change = -playerSpeed
                lefthold = True
            elif event.key == pygame.K_LEFT and righthold == True:
                playerX_change = 0
                lefthold = True
            if event.key == pygame.K_RIGHT and lefthold == False:
                playerX_change = playerSpeed
                righthold = True
            elif event.key == pygame.K_RIGHT and lefthold == True:
                playerX_change = 0
                righthold = True

            if event.key == pygame.K_UP and downhold == False:
                playerY_change = -playerSpeed
                uphold = True
            elif event.key == pygame.K_UP and downhold == True:
                playerY_change = 0
                uphold = True
            if event.key == pygame.K_DOWN and uphold == False:
                playerY_change = playerSpeed
                downhold = True
            elif event.key == pygame.K_DOWN and uphold == True:
                playerY_change = 0
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
                fire_apple(playerX, playerY)

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
    if apple_state == "fire":
        appleBulletX += apple_changeX
        appleBulletY += apple_changeY
        draw_apple(appleBulletX, appleBulletY)

    #draws the players and apples
    player(playerX, playerY)
    apple(appleX, appleY)
    pygame.display.update()