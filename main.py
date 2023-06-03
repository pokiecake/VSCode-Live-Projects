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

#Apple
appleImg = pygame.image.load("Assets/Apple.png")
appleX = random.randint(50, 750)
appleY = random.randint(50, 350)

def player(x, y):
    screen.blit(playerImg, (x, y))

def apple(x, y):
    screen.blit(appleImg, (x, y))

#background sound
mixer.music.load('Assets/Clouds.wav')
mixer.music.play(-1)

#Game Loop. When the x button is clicked, running is set to false and the window closes.
running = True
while running:

    #Draws Purplish background
    screen.fill((150,0,150))

    #event listener
    for event in pygame.event.get():
        #stops the game when the x button is pressed
        if event.type == pygame.QUIT:
            running = False
        #handles key presses
        if event.type == pygame.KEYDOWN:
            #sets the x and y changes based on what is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
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
    
    #draws the players and apples
    player(playerX, playerY)
    apple(appleX, appleY)
    pygame.display.update()