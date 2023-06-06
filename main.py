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
playerSpeed = 500
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
#stockpiles = []
#stockpilesTimeouts = []

#Apple spawners
spawners = []

#rooms
rooms = []
entranceW = 100
entranceH = 200
inEntrance = -1

#Text
ammofont = pygame.font.Font('freesansbold.ttf',32)
ammox = 0
ammoy = 0
enterPopupX = 0
enterPopupY = 50
roomX = 650
roomY = 0
def showammo(x,y):
    ammocount = ammofont.render("Ammo: " + str(appleBulletCount), True, (255,0,0))
    screen.blit(ammocount, (x,y))

def showEnterPopup(x, y):
    popup = ammofont.render("Enter Room {0}?".format(inEntrance[0]), True, (0, 0, 255))
    screen.blit(popup, (x,y))

def showRoom(x, y):
    popup = ammofont.render("Room: {0}".format(currentRoom), True, (255, 0, 0))
    screen.blit(popup, (x,y))

#gets the time when the program started
timestart = time.time()

#Note: time.time() gets the time from the time their code was made; must get relative time

#returns the relative time when the program started to that point in time
#rounded to the int placed in the parameter
def gettime(roundnum):
    currenttime = round((time.time() - timestart),roundnum)
    return currenttime


#time class will now be used to add more functions related to time
class TimeConcept:
    def __init__(self):
        1 == 1
    


    #the following gets the time elapsed since last call
    global oldtime
    oldtime = 0
    def timeelapsed(self):
        global oldtime
        newtime = gettime(99)
        elapsed = newtime - oldtime
        oldtime = newtime
        return elapsed

#displays text for the time
timefont = pygame.font.Font('freesansbold.ttf',32)
timex = 0
timey = 550
lastTime = 0
currentTime = 0
def showtime(x,y):
    timecount = timefont.render("Time elapsed: " + str(gettime(3)), True, (0,0,255))
    screen.blit(timecount, (x,y))

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
    bulletSpeed = 2000
    apple_state = "fire"
    xPos = x
    yPos = y
    #0 is up, 1 is right, 2 is down, 3 is left
    match(playerDirection):
        case 0:
            yPos -= appleH
            xPos += (playerW - appleW) / 2
            apple_changeX = 0
            apple_changeY = -bulletSpeed
        case 1:
            yPos += (playerH - appleH) / 2
            xPos += playerW + appleW
            apple_changeX = bulletSpeed
            apple_changeY = 0
        case 2:
            yPos += playerH + appleH
            xPos += (playerW - appleW) / 2
            apple_changeX = 0
            apple_changeY = bulletSpeed
        case 3:
            yPos += (playerH - appleH) / 2
            xPos -= appleW
            apple_changeX = -bulletSpeed
            apple_changeY = 0
    #sets the apple bullet's position based on the direction
    appleBulletX = xPos
    appleBulletY = yPos
    bullet = AppleBullets(xPos, yPos, apple_changeX, apple_changeY)
    bullets.append(bullet)

#draws anything apple related
def draw_apple(x, y):
    screen.blit(appleImg, (x, y))

#spawns stockpile on cooldown
def spawn_apple_pile(roomNum = currentRoom):
    x = random.randint(50, 750)
    y = random.randint(50, 550)
    s = AppleStockpiles(x, y, appleW, appleH, roomNum)
    #stockpiles.append(s)
    return s

#temporary timer to automatically create stockpiles after a delay
def check_timeouts():
    sec = gettime(3)
    #looks through all the spanwers to find timeouts. Timeouts delay the spawning of stockpiles
    for spawner in spawners:
        for timeout in spawner.get_timeouts():
            if sec > timeout[0] + 1:
                pile = spawn_apple_pile(timeout[1])
                spawner.add_stockpile(pile)
                spawner.remove_timeout(timeout)
    #for sTime in stockpilesTimeouts:
        #if sec > sTime[0] + 1:
            #spawn_apple_pile(sTime[1])
            #stockpilesTimeouts.remove(sTime)

#checks collision between target 1 and 2. Trust me on the math
def check_collisions(target1P, target2P):
    x1 = target1P[0]
    y1 = target1P[1]
    w1 = target1P[2]
    h1 = target1P[3]
    x2 = target2P[0]
    y2 = target2P[1]
    w2 = target2P[2]
    h2 = target2P[3]

    return (y2 < y1 + h1 and y2 + h2 > y1) and ((x2 < x1 + w1 and x2 + w2 > x1) or (x2 + w2 > x1 and x2 < x1 + w1))

#class for apple bullets
class AppleBullets:
    def __init__(self, x, y, change_x, change_y):
        self.x = x
        self.y = y
        self.change_x = change_x
        self.change_y = change_y
    
    def change(self, delta):
        self.x += self.change_x * delta
        self.y += self.change_y * delta
    
    def getPos(self):
        return (self.x, self.y)

#class for apple stockpiles
class AppleStockpiles:
    def __init__(self, x, y, w, h, inRoom):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.inRoom = inRoom
    
    #checks for collision in the horizontal and vertical direction
    def checkCollision(self, pX, pY, pW, pH):
        return check_collisions([self.x, self.y, self.w, self.h], [pX, pY, pW, pH])
        #I'll keep this in case we need it later
        #if (pY < self.y + self.h and pY + pH > self.y):
            #if (pX < self.x + self.w and pX + pW > self.x) or (pX + pW > self.x and pX < self.x + self.w):
                #return True
    
    def getPos(self):
        return (self.x, self.y)

#Will spawn stockpiles automatically
class Spawners:
    def __init__(self, type, room, max = 1):
        self.type = type
        self.room = room
        self.stockpiles = []
        self.stockpileTimeouts = []
        self.maxStockpiles = max
        self.queuedStockpiles = 0
    
    def check_for_stockpiles(self, sec):
        if (self.stockpiles.__len__() + self.queuedStockpiles < self.maxStockpiles):
            self.queuedStockpiles += 1
            self.stockpileTimeouts.append((sec, self.room))
    
    def remove_timeout(self, timeout):
        self.stockpileTimeouts.remove(timeout)
        self.queuedStockpiles -= 1

    def add_stockpile(self, pile):
        self.stockpiles.append(pile)
    
    def remove_stockpile(self, pile):
        self.stockpiles.remove(pile)
    
    def get_timeouts(self):
        return self.stockpileTimeouts
    
    def get_stockpiles(self):
        return self.stockpiles


#class for rooms
class Rooms:
    def __init__(self, num, entrances):
        #entrances will be an object that holds the room it can connect to and the direction (North, East, South, West) it connects from
        #the long side is dependent on where the entrance is. You can ask me to clarify if you need to -Tony
        self.num = num
        self.entrances = entrances
        self.long = 200
        self.short = 100
    #If there is a collision, the entrance tuple will be returned (so that the game loop knows the entrance #)
    def checkCollisions(self, pX, pY, pW, pH):
        target2P = [pX, pY, pW, pH]
        for entrance in self.entrances:
            #0 = North, 1 = East, 2 = South, 3 = West
            if (entrance[1] == 0):
                if (check_collisions([300, 0, self.long, self.short], target2P)):
                    return entrance
            if (entrance[1] == 1):
                if (check_collisions([700, 200, self.short, self.long], target2P)):
                    return entrance
            if (entrance[1] == 2):
                if (check_collisions([300, 500, self.long, self.short], target2P)):
                    return entrance
            if (entrance[1] == 3):
                if (check_collisions([0, 200, self.short, self.long], target2P)):
                    return entrance
        return False  

#spawns an apple pile in room 1 and room 2
#spawn_apple_pile(1)
#spawn_apple_pile(2)

#adds a bunch of rooms
rooms.append(Rooms(1, [(4, 1), (6, 2), (2, 3)]))
rooms.append(Rooms(2, [(1, 1), (3, 0)]))
rooms.append(Rooms(3, [(2, 2)]))
rooms.append(Rooms(4, [(1, 3), (5, 2)]))
rooms.append(Rooms(5, [(4, 0), (6, 3)]))
rooms.append(Rooms(6, [(1, 0), (5, 1)]))

#adds a bunch of spawners
spawners.append(Spawners("apple", 1))
spawners.append(Spawners("apple", 2, 2))
spawners.append(Spawners("apple", 3, 3))
spawners.append(Spawners("apple", 4, 2))
spawners.append(Spawners("apple", 5, 3))
spawners.append(Spawners("apple", 6, 2))

#background sound
mixer.music.load('Assets/Sky.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#Global Variable Setup
#Key Press Status (held down or not)
lefthold = False
righthold = False
uphold = False
downhold = False
#Controls speed when both opposite buttons pressed
stuckspeed = 0.0 * playerSpeed

#Game Loop. When the x button is clicked, running is set to false and the window closes.
running = True
while running:
    currentTime = gettime(12)
    delta = currentTime - lastTime
    #Draws Purplish background. Unneeded due to spongebob background
    #screen.fill((150,0,150))

    #draws spongebob background
    #pygame.transform.scale_by(BGImage,20)
    #screen.blit(background, (0,0))
    match(currentRoom):
        case 1:
            screen.blit(BGImage, (0,0))
        case 2:
            screen.fill((150, 0, 150))
        case 3:
            screen.fill((225, 100, 100))
        case 4:
            screen.fill((100, 225, 100))
        case 5:
            screen.fill((255, 255, 0))
        case 6:
            screen.fill((200, 200, 200))

    #event listener
    for event in pygame.event.get():
        #stops the game when the x button is pressed
        if event.type == pygame.QUIT:
            running = False
        #handles key presses
        if event.type == pygame.KEYDOWN:
            #sets the x and y changes based on what is pressed
            #sets status of hold on the key to true
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
            
            #changes the room when at an entrance. (not for testing purposes)
            if event.key == pygame.K_e and inEntrance != -1:
                currentRoom = inEntrance[0]
                dir = inEntrance[1]
                match(dir):
                    case 0:
                        playerY = screenHeight - playerH
                    case 1:
                        playerX = 0
                    case 2:
                        playerY = 0
                    case 3:
                        playerX = screenWidth - playerW
        #handles key lifts
        if event.type == pygame.KEYUP:
            #stops changes after corresponding keys are lifted given that no other key is held
            #sets status of hold on the key to false
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
    playerX += playerX_change * delta
    playerY += playerY_change * delta

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
        bullet.change(delta)
        pos = bullet.getPos()
        x = pos[0]
        y = pos[1]
        draw_apple(x, y)
        if x < 0 or x > screenWidth or y < 0 or y > screenHeight:
            bullets.remove(bullet)
            del bullet
    
    #checks for collision for all stockpiles in all spawners
    for spawner in spawners:
        spawner.check_for_stockpiles(currentTime)
        stockpiles = spawner.get_stockpiles()
        for pile in stockpiles:
            pos = pile.getPos()
            if currentRoom == pile.inRoom:
                draw_apple(pos[0], pos[1])
                #removes a pile if collided and adds to the apple bullet count
                if pile.checkCollision(playerX, playerY, playerW, playerH):
                    spawner.remove_stockpile(pile)
                    del pile
                    appleBulletCount += 1

    #checks for collisions in entrances.
    for room in rooms:
        if room.num == currentRoom:
            entrance = room.checkCollisions(playerX, playerY, playerW, playerH)
            if entrance != False:
                #if r is pressed, the player will enter the room
                inEntrance = entrance
            else:
                inEntrance = -1

    #draws the players and apples
    player(playerX, playerY)

    #draws text & other assets
    showammo(ammox,ammoy)
    showtime(timex,timey)
    showRoom(roomX, roomY)
    if (inEntrance != -1):
        showEnterPopup(enterPopupX, enterPopupY)
    #test canvas (put temporary code here to run)
    
    #checks the spawners to see if a stockpile should be created
    check_timeouts()

    lastTime = currentTime

    pygame.display.update()