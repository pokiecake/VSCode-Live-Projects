import pygame
from pygame import mixer
import random
import time
import asyncio
import math


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
bullet_state = "ready"
rapid_fire = False
bullets = []
appleBulletCount = 0

#Apple Stockpiles
#stockpiles = []
#stockpilesTimeouts = []

#Enemies
enemyImg = pygame.image.load("Sprites/fob.png")
enemyImg = pygame.transform.scale(enemyImg, (125,196))
enemyW = enemyImg.get_width()
enemyH = enemyImg.get_height()
enemies = []
enemies_killed = 0

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
enterPopupY = 100
roomX = 650
roomY = 0
ekX = 0
ekY = 500
def showammo(x,y):
    ammocount = ammofont.render("Ammo: " + str(appleBulletCount), True, (255,0,0))
    screen.blit(ammocount, (x,y))

def showEnterPopup(x, y):
    popup = ammofont.render("Enter Room {0}?".format(inEntrance[0]), True, (0, 0, 255))
    screen.blit(popup, (x,y))

def showRoom(x, y):
    popup = ammofont.render("Room: {0}".format(currentRoom), True, (255, 0, 0))
    screen.blit(popup, (x,y))

def show_enemies_killed(x, y):
    popup = ammofont.render("Enemies killed: {0}".format(enemies_killed), True, (255, 0, 0))
    screen.blit(popup, (x, y))

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
    #oldtime1 is oldtime for cooldowns, oldtime2 is oldtime for time windows
    global oldtime1
    global oldtime2
    oldtime2 = 0
    oldtime1 = 0
    def timeelapsed(self):
        global oldtime1
        newtime = gettime(99)
        elapsed = newtime - oldtime1
        return elapsed
    
    def cooldown(self, amount):
        global oldtime1
        
        timepassed = self.timeelapsed()
        if timepassed >= amount:
            oldtime1 = gettime(99)
            return True
        else:
            return False

    def timewindow(self, amount):
        global oldtime2
        
        timepassed = gettime(99) - oldtime2
        if timepassed >= amount:
            oldtime2 = gettime(99)
            return False
        else:
            oldtime2 = gettime(99)
            return True

#temporary speed function; makes the temporary speed decay over time
tempspeed = 0
collectivetime = 0
def calcspeed(change):
    global tempspeed
    global delta
    global collectivetime
    collectivetime = collectivetime + delta
    if tempspeed > 0 and change != 0 and collectivetime != 0:
        if tempspeed < 1:
            tempspeed = 0
        retvalue = tempspeed
        tempspeed = (tempspeed * (0.5/collectivetime))
        if tempspeed > playerSpeed * 2:
            tempspeed = playerSpeed * 2
        if change > 0:
            return retvalue
        elif change < 0:
            return -retvalue
        
    elif tempspeed == 0:
        collectivetime = 0
        return 0
    else:
        return 0

#calculates whether the current value is positive or negative and returns 1 or -1 respectively
def calcsign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0


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



def player(x, y):
    screen.blit(playerImg, (x, y))

def apple(x, y):
    screen.blit(appleImg, (x, y))

#doesn't actually fire apples, only creates them and their positions
def fire_apple(x, y, mousePos = False):
    global apple_state
    apple_changeX = 0
    apple_changeY = 0
    global bullets
    bulletSpeed = 2000
    apple_state = "fire"
    xPos = x
    yPos = y
    if mousePos == False:
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
    else:
        #Finds the angle between the mouse and the center of the player
        #then it fires the apple in the direction found by the angle
        centerX = playerX + playerW / 2
        centerY = playerY + playerH / 2
        xPos = centerX - appleW / 2
        yPos = centerY - appleH / 2
        deltaX = mousePos[0] - centerX
        deltaY = mousePos[1] - centerY
        dirX = 1 if deltaX > 0 else -1
        dirY = 1 if deltaY > 0 else -1
        angle = abs(math.atan((deltaY) / (deltaX)))
        apple_changeX = math.cos(angle) * bulletSpeed * dirX
        apple_changeY = math.sin(angle) * bulletSpeed * dirY
    #sets the apple bullet's position based on the direction
    bullet = AppleBullets(xPos, yPos, appleW, appleH, apple_changeX, apple_changeY)
    bullets.append(bullet)

#draws anything apple related
def draw_apple(x, y):
    screen.blit(appleImg, (x, y))

#draws anything
def draw(img, x, y):
    screen.blit(img, (x, y))

#spawns stockpile
def spawn_apple_pile(room = currentRoom):
    x = random.randint(50, 750)
    y = random.randint(50, 550)
    s = AppleStockpiles(x, y, appleW, appleH, room)
    #stockpiles.append(s)
    return s

#spawns enemies
def spawn_enemy(pos, room):
    x = pos[0]
    y = pos[1]
    e = Enemies(x, y, enemyW, enemyH, room)
    return e

#temporary timer to automatically create stockpiles after a delay
def check_timeouts():
    sec = gettime(3)
    #looks through all the spawners to find timeouts. Timeouts delay the spawning of stockpiles or enemies
    for spawner in spawners:
        for timeout in spawner.get_timeouts():
            if sec > timeout[0] + timeout[1]:
                type = spawner.type
                if type == "apple":
                    pile = spawn_apple_pile(spawner.room)
                    spawner.add_item(pile)
                    spawner.remove_timeout(timeout)
                elif type == "enemy":
                    enemy = spawn_enemy(spawner.initial_pos, spawner.room)
                    spawner.add_item(enemy)
                    spawner.remove_timeout(timeout)
                else:
                    print("type not recognized")
        if spawner.type == "enemy":
            enemies = spawner.get_items()
            for enemy in enemies:
                for timeout in enemy.timeouts:
                    if enemy.inRoom != currentRoom:
                        enemy.timeouts.remove(timeout)
                    else:
                        initialSec = timeout[1]
                        cooldown = timeout[2]
                        if sec > initialSec + cooldown:
                            enemy.start_move(timeout)
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

def find_angle(pos1, pos2):
    deltaX = pos2[0] - pos1[0]
    deltaY = pos2[1] - pos1[1]
    dirX = 1 if deltaX > 0 else -1
    dirY = 1 if deltaY > 0 else -1
    angle = abs(math.atan((deltaY) / (deltaX)))
    return (angle, dirX, dirY)





#class for apple bullets
class AppleBullets:
    def __init__(self, x, y, w, h, change_x, change_y):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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

#Class for enemies
class Enemies:
    def __init__(self, x, y, w, h, inRoom):
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.targetPos = (0, 0)
        self.dir = (0, 0)
        self.inRoom = inRoom
        self.change_x = 0
        self.change_y = 0
        self.timeouts = []
        self.move_queued = False
        self.moving = False
        self.speed = 400
    
    def reset_pos(self):
        self.x = self.initialX
        self.y = self.initialY
        self.targetPos = (0, 0)
        self.move_queued = False
        self.moving = False
        self.change_x = 0
        self.change_y = 0
        self.dir = (0, 0)

    def move(self, delta):
        if (self.moving == True):
            self.x += self.change_x  * delta
            self.y += self.change_y * delta
            if (self.x * self.dir[0] >= self.targetPos[0] * self.dir[0]):
                self.change_x = False
                self.x = self.targetPos[0]
            if (self.y * self.dir[1] >= self.targetPos[1] * self.dir[1]):
                self.change_y = False
                self.y = self.targetPos[1]
            if (not self.change_x and not self.change_y):
                self.moving = False
        #print((self.x, self.y))
       # print((self.change_x, self.change_y))

    def queue_move(self, sec):
        if (not self.moving and not self.move_queued):
            self.move_queued = True
            random_pos = (random.randint(0, screenWidth - self.w), random.randint(0, screenHeight - self.h))
            self.timeouts.append(((random_pos), sec, 3))
            print("move queued")
    
    def start_move(self, timeout):
        self.move_queued = False
        self.moving = True
        self.targetPos = timeout[0]
        angle_and_dir = find_angle((self.x, self.y), self.targetPos)
        angle = angle_and_dir[0]
        dirX = angle_and_dir[1]
        dirY = angle_and_dir[2]
        self.dir = (dirX, dirY)
        self.change_x = math.cos(angle) * self.speed * dirX
        self.change_y = math.sin(angle) * self.speed * dirY
        self.timeouts.remove(timeout)

    def checkCollision(self, pX, pY, pW, pH):
        return check_collisions([self.x, self.y, self.w, self.h], [pX, pY, pW, pH])

#Will spawn stockpiles and enemies automatically
class Spawners:
    def __init__(self, type, room, max = 1, cooldown = 1, initial_pos = (0,0)):
        self.type = type
        self.room = room
        self.items = []
        self.timeouts = []
        self.cooldown = cooldown
        self.max = max
        self.queued = 0
        self.enabled = True
        self.initial_pos = initial_pos
            
    def check_for_items(self, sec):
        if (self.items.__len__() + self.queued < self.max):
            self.queued += 1
            self.timeouts.append((sec, self.cooldown, type))

    def remove_timeout(self, timeout):
        self.timeouts.remove(timeout)
        self.queued -= 1

    def add_item(self, pile):
        self.items.append(pile)
    
    def remove_item(self, pile):
        self.items.remove(pile)
    
    def get_timeouts(self):
        return self.timeouts
    
    def get_items(self):
        return self.items

class EnemySpawners(Spawners):
    pass
    
#class of healthbar

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
    #calculate health ratio  
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))

health_bar = HealthBar(250, 50, 400, 40, 100)

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
rooms.append(Rooms(1, [(6, 1), (4, 2), (2, 3)]))
rooms.append(Rooms(2, [(1, 1), (3, 0), (11, 3)]))
rooms.append(Rooms(3, [(2, 2)]))
rooms.append(Rooms(4, [(1, 0), (5, 1)]))
rooms.append(Rooms(5, [(6, 0), (4, 3)]))
rooms.append(Rooms(6, [(1, 3), (5, 2), (7,1)]))
rooms.append(Rooms(7, [(8, 1), (6, 3)]))
rooms.append(Rooms(8, [(9, 2), (7, 3)]))
rooms.append(Rooms(9, [(8, 0), (10, 3)]))
rooms.append(Rooms(10, [(9, 1)]))
rooms.append(Rooms(11, [(2, 1), (12, 2), (14, 3)]))
rooms.append(Rooms(12, [(11, 0), (13, 3)]))
rooms.append(Rooms(13, [(12, 1), (14, 0)]))
rooms.append(Rooms(14, [(15, 0), (11, 1), (13, 2)]))
rooms.append(Rooms(15, [(14, 2), (16, 3)]))
rooms.append(Rooms(16, [(15, 1)]))

#adds a bunch of spawners
spawners.append(Spawners("apple", 1))
spawners.append(Spawners("apple", 2, 2))
spawners.append(Spawners("apple", 3, 3))
spawners.append(Spawners("apple", 4, 2))
spawners.append(Spawners("apple", 5, 3))
spawners.append(Spawners("apple", 6, 2))
spawners.append(Spawners("apple", 7, 1))
spawners.append(Spawners("apple", 8, 1))
spawners.append(Spawners("apple", 9, 1))
spawners.append(Spawners("apple", 10, 5))
spawners.append(Spawners("apple", 11, 1))
spawners.append(Spawners("apple", 12, 1))
spawners.append(Spawners("apple", 13, 2))
spawners.append(Spawners("apple", 14, 1))
spawners.append(Spawners("apple", 15, 1))
spawners.append(Spawners("apple", 16, 5))
spawners.append(EnemySpawners("enemy", 5, 1, 5, (700, 400)))
spawners.append(EnemySpawners("enemy", 3, 1, 5, (50, 50)))
spawners.append(EnemySpawners("enemy", 10, 3, 5, (50, 50)))
spawners.append(EnemySpawners("enemy", 16, 1, 5, (50, 50)))
spawners.append(EnemySpawners("enemy", 16, 1, 5, (700, 450)))

#adds enemies
enemies.append(Enemies(0, 200, enemyW, enemyH, 3))

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
lastkey = ""
#Controls speed when both opposite buttons pressed
stuckspeed = 0.0 * playerSpeed

#sets healthbar
health_bar.hp = 100

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
        case 7:
            screen.fill((230, 200, 200))
        case 8:
            screen.fill((230, 200, 230))
        case 9:
            screen.fill((230, 230, 230))
        case 10:
            screen.fill((255, 255, 255))
        case 11:
            screen.fill((125, 150, 125))
        case 12:
            screen.fill((125, 125, 150))
        case 13:
            screen.fill((150, 125, 125))
        case 14:
            screen.fill((100, 100, 100))
        case 15:
            screen.fill((50, 50, 50))
        case 16:
            screen.fill((20, 20, 20))

    #event listener
    for event in pygame.event.get():
        #stops the game when the x button is pressed
        if event.type == pygame.QUIT:
            running = False
        #shoots an apple in the direction of the cursor
        if pygame.mouse.get_pressed()[0] and appleBulletCount > 0 and (bullet_state == "ready" or rapid_fire):
                fire_apple(playerX, playerY, pygame.mouse.get_pos())
                appleBulletCount -= 1
                #ensures that the apple won't be released when the mouse is held down
                #if you want to shoot while holding the mouse down, set the rapid_fire variable to true
                bullet_state = "fired"
        #Reloads the gun when the left mouse button is released
        elif not pygame.mouse.get_pressed()[0]:
            bullet_state = "ready"
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
            
            #testing key presses here
            dash = TimeConcept()
            if dash.timewindow(0.5) and lastkey == event.key:
                tempspeed = playerSpeed

            else:
                1==1

            lastkey = event.key

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

    #drawing hp bar
    
    health_bar.draw(screen)

    #x and y change accounting for temporary speed
    playerX_change = playerSpeed * calcsign(playerX_change) + calcspeed(playerX_change)
    playerY_change = playerSpeed * calcsign(playerY_change) + calcspeed(playerY_change)
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
    #checks for collision for all spawners
    for spawner in spawners:
        spawner.check_for_items(currentTime)
        #Checks collisions for all stockpiles
        if spawner.type == "apple":
            stockpiles = spawner.get_items()
            for pile in stockpiles:
                pos = pile.getPos()
                if currentRoom == pile.inRoom:
                    draw_apple(pos[0], pos[1])
                    #removes a pile if collided and adds to the apple bullet count
                    if pile.checkCollision(playerX, playerY, playerW, playerH):
                        spawner.remove_item(pile)
                        del pile
                        appleBulletCount += 1
        #checks collision for enemies
        elif spawner.type == "enemy":
            enemies = spawner.get_items()
            for enemy in enemies:
                enemy.move(delta)
                if enemy.inRoom == currentRoom:
                    draw(enemyImg, enemy.x, enemy.y)
                    enemy.queue_move(currentTime)
                    if (enemy.checkCollision(playerX, playerY, playerW, playerH)):
                        print("collided with enemy")
                        health_bar.hp = health_bar.hp - 10
                        
                    for bullet in bullets:
                        if (check_collisions([bullet.x, bullet.y, bullet.w, bullet.h], [enemy.x, enemy.y, enemy.w, enemy.h])):
                            print("bullet hit enemy")
                            enemies.remove(enemy)
                            del enemy
                            enemies_killed += 1
                            break
                else:
                    enemy.reset_pos()


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
    show_enemies_killed(ekX, ekY)
    if (inEntrance != -1):
        showEnterPopup(enterPopupX, enterPopupY)
    #test canvas (put temporary code here to run)
    
    

    #checks any kind of cooldowns to spawn things like stockpiles or enemies
    check_timeouts()

    lastTime = currentTime

    pygame.display.update()