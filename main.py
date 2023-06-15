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
#testing purposes
#screenWidth = 1280
#screenHeight = 1024
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

#Treasure
#treasure = pygame.image.load("")
treasures = []

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

#Bosses
boss_img = pygame.image.load("Sprites/Boss.png")
boss_img = pygame.transform.scale(boss_img, (125, 196))
boss_w = boss_img.get_width()
boss_h = boss_img.get_height()
bosses = []

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
        #initializes the time variables at the start of creation
        self.oldtime1 = gettime(99)
        self.oldtime2 = gettime(99)

    #the following gets the time elapsed since last call
    #oldtime1 is oldtime for cooldowns, oldtime2 is oldtime for time windows
    #global oldtime1
    #global oldtime2
    #oldtime2 = 0
    #oldtime1 = 0
    def timeelapsed(self):
        #global oldtime1
        self.newtime = gettime(99)
        self.elapsed = self.newtime - self.oldtime1
        return self.elapsed
    
    def cooldown(self, amount, reset = True):
        #print(self.oldtime1)
        timepassed = self.timeelapsed()
        if timepassed >= amount:
            #Modified this part, because I don't always want to reset the cooldown even if it's passed already - Tony
            if (reset):
                self.oldtime1 = gettime(99)
            return True
        else:
            return False

    def timewindow(self, amount):
        self.oldtime2
        
        timepassed = gettime(99) - self.oldtime2
        if timepassed >= amount:
            self.oldtime2 = gettime(99)
            return False
        else:
            self.oldtime2 = gettime(99)
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

def spawn_boss(pos, room):
    x = pos[0]
    y = pos[1]
    b = Bosses(x, y, boss_w, boss_h, room)
    return b 

#temporary timer to automatically create stockpiles after a delay
def check_timeouts():
    global bosses
    sec = gettime(3)
    #looks through all the spawners to find timeouts. Timeouts delay the spawning of stockpiles or enemies
    for spawner in spawners:
        for timeout in spawner.get_timeouts():
            if sec > timeout[0] + timeout[1]:
                spawner.spawn(timeout)
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
        if spawner.type == "boss":
            bosses = spawner.get_items()
            for boss in bosses:
                for timeout in boss.timeouts:
                    if boss.inRoom == currentRoom:
                        initial_sec = timeout[1]
                        cooldown = timeout[2]
                        if sec > initial_sec + cooldown:
                            boss.start_move(timeout)
    for boss in bosses:
        for timeout in boss.timeouts:
            if boss.inRoom == currentRoom:
                initial_sec = timeout[1]
                cooldown = timeout[2]
                if sec > initial_sec + cooldown:
                    boss.start_move(timeout)
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

class Treasure:
    def __init__(self, x, y, room):
        self.x = x
        self.y = y
        self.room = room

#class for apple bullets
class AppleBullets:
    def __init__(self, x, y, w, h, change_x, change_y, owner = "player"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.change_x = change_x
        self.change_y = change_y
        self.owner = owner
    
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
        self.timeouts = []

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

    def look(self):
        # 0 means left and up resp, 1 means right and down resp; -1 is null
        result = [-1,-1]
        if self.x >= playerX:
            result[0] = 0
        elif self.x < playerX:
            result[0] = 1
        if self.y >= playerY:
            result[1] = 0
        elif self.y < playerY:
            result[1] = 1
        
        return result

    def queue_move(self, sec):
        #this is temporary to test the targetting system (either all enemies target or none do at the moment)
        target_player = True
        if (not self.moving and not self.move_queued):
            if target_player:
                self.move_queued = True
                scan = self.look()
                print(str(scan))
                random_poslist = [-1, -1]
                if scan[0] == 0:
                    random_poslist[0] = random.randint(0, self.x)
                elif scan[0] == 1:
                    random_poslist[0] = random.randint(self.x, screenWidth - self.w)
                if scan[1] == 0:
                    random_poslist[1] = random.randint(0, self.y)
                elif scan[1] == 1:
                    random_poslist[1] = random.randint(self.y, screenHeight - self.h)
                random_pos = tuple(random_poslist)
                self.timeouts.append(((random_pos), sec, 3))
                print("move queued; target")
            else:
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

#Boss class
class Bosses(Enemies):
    #some values needed for the boss
    def set_boss_values(self):
        self.speed = 700
        self.health = 10
        self.vulnerable = False
        self.timeout_v = 0
        self.cooldown = random.randint(5, 7)
        self.attack_target_pos = (0, 0)
        self.attack_cooldown = 0

    #switches the vulnerability of the boss after a cooldown
    def toggle_vulnerability(self):
        #Ensures that the cooldown only starts once the room has been entered
        if (self.timeout_v == 0):
            self.timeout_v = TimeConcept()
        if (self.timeout_v.cooldown(self.cooldown)):
            print("cooldown")
            print(self.cooldown)
            self.vulnerable = not self.vulnerable
            self.cooldown = random.randint(5, 7)
            #When vulnerable, the cooldown is always 3 to toggle the shield on again
            if self.vulnerable:
                self.cooldown = 3

    #handles a bullet hitting the boss.
    def hit(self):
        if self.vulnerable == True:
            self.health -= 1
        if (self.health == 0):
            return "killed"
        else:
            return self.health
    
    def reset(self):
        self.reset_pos()
        self.timeout_v = 0
        self.cooldown = random.randint(5, 8)
        self.attack_cooldown = 0
    
    #Sets the target pos at the player's center
    def set_attack_target_pos(self):
        self.attack_target_pos = (playerX + playerW / 2, playerY + playerH / 2)
    
    #Fires an apple in the player's direction
    def attack(self):
        #Math you don't need to worry about (just creates an apple and centers it on the boss
        self.set_attack_target_pos();
        pos = self.attack_target_pos
        center_x = self.x + (boss_w - appleW) / 2
        center_y = self.y + (boss_h - appleH) / 2
        a = find_angle((center_x, center_y), pos)
        angle = a[0]
        dir_x = a[1]
        dir_y = a[2]
        bullets.append(AppleBullets(center_x, center_y, appleW, appleH, 1000 * math.cos(angle) * dir_x, 1000 * math.sin(angle) * dir_y, "boss"))
    
    #Will attempt an attack. Attack is successful 3 seconds after the initial attack. Creates a new timeconcept if there is none
    def attempt_attack(self):
        if (self.attack_cooldown == 0):
            self.attack_cooldown = TimeConcept()
            print("attack cooldown started")
        elif (self.attack_cooldown.cooldown(3)):
            print("attacking")
            self.attack()

#Will spawn stockpiles and enemies automatically
class Spawners:
    def __init__(self, type, room, max = 1, cooldown = 3, initial_pos = (0,0)):
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
            #self.timeouts.append((TimeConcept(), self.cooldown, type))


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

class AppleSpawners(Spawners):
    def spawn(self, timeout):
        pile = spawn_apple_pile(self.room)
        self.add_item(pile)
        self.remove_timeout(timeout)

class EnemySpawners(Spawners):
    def spawn(self, timeout):
        enemy = spawn_enemy(self.initial_pos, self.room)
        self.add_item(enemy)
        self.remove_timeout(timeout)


class BossSpawners(Spawners):
    def spawn(self, timeout):
        boss = spawn_boss(self.initial_pos, self.room)
        self.add_item(boss)
        self.remove_timeout(timeout)

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
        self.entrances = []
        self.long = 200
        self.short = 100
        for entrance in entrances:
            match entrance.__len__():
                case 2:
                    self.entrances.append(Entrances(entrance[0], entrance[1]))
                case 3:
                    self.entrances.append(Entrances(entrance[0], entrance[1], entrance[2]))
    #If there is a collision, the entrance tuple will be returned (so that the game loop knows the entrance #)
    def checkCollisions(self, pX, pY, pW, pH):
        target2P = [pX, pY, pW, pH]
        for entrance in self.entrances:
            if (not entrance.open):
                continue
            vals = entrance.get_vals()
            #0 = North, 1 = East, 2 = South, 3 = West
            if (vals[1] == 0):
                if (check_collisions([(screenWidth - self.long) / 2, 0, self.long, self.short], target2P)):
                    return entrance
            if (vals[1] == 1):
                if (check_collisions([screenWidth - self.short, (screenHeight - self.long) / 2, self.short, self.long], target2P)):
                    return entrance
            if (vals[1] == 2):
                if (check_collisions([(screenWidth - self.long) / 2, screenHeight - self.short, self.long, self.short], target2P)):
                    return entrance
            if (vals[1] == 3):
                if (check_collisions([0, (screenHeight - self.long) / 2, self.short, self.long], target2P)):
                    return entrance
        return False  

#Class for entrances
class Entrances:
    def __init__(self, room, door, open = True):
        self.room = room
        self.door = door
        self.open = open

    def get_vals(self):
        return (self.room, self.door, self.open)

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
rooms.append(Rooms(16, [(15, 1), (17, 3)]))
rooms.append(Rooms(17, [(16, 1), (18, 3, False)]))
rooms.append(Rooms(18, [(17, 1)]))

#adds a bunch of spawners
spawners.append(AppleSpawners("apple", 1))
spawners.append(AppleSpawners("apple", 2))
spawners.append(AppleSpawners("apple", 3, 2))
spawners.append(AppleSpawners("apple", 4))
spawners.append(AppleSpawners("apple", 5, 2))
spawners.append(AppleSpawners("apple", 6))
spawners.append(AppleSpawners("apple", 7, 1))
spawners.append(AppleSpawners("apple", 8, 1))
spawners.append(AppleSpawners("apple", 9, 2))
spawners.append(AppleSpawners("apple", 10, 3))
spawners.append(AppleSpawners("apple", 11))
spawners.append(AppleSpawners("apple", 12))
spawners.append(AppleSpawners("apple", 13, 1))
spawners.append(AppleSpawners("apple", 14))
spawners.append(AppleSpawners("apple", 15))
spawners.append(AppleSpawners("apple", 16, 3))
spawners.append(EnemySpawners("enemy", 5, 1, 5, (700, 400)))
spawners.append(EnemySpawners("enemy", 3, 1, 5, (50, 50)))
spawners.append(EnemySpawners("enemy", 10, 3, 5, (50, 50)))
spawners.append(EnemySpawners("enemy", 16, 1, 5, (50, 50)))
spawners.append(EnemySpawners("enemy", 16, 1, 5, (700, 450)))

#adds bosses
bosses.append(Bosses(100, 200, boss_w, boss_h, 17))

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

#Keeps track of dash time
dash = TimeConcept()

#Controls speed when both opposite buttons pressed
stuckspeed = 0.0 * playerSpeed

#sets healthbar
health_bar.hp = 100
HP_DMG = TimeConcept()

#Loops through the bosses to set some values specific to the bosses
for boss in bosses:
    boss.set_boss_values()

running = True

#Debug code
currentRoom = 1

#Game Loop. When the x button is clicked, running is set to false and the window closes.
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
            screen.fill((200, 255, 0))
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
            screen.fill((30, 30, 30))
        case 17:
            screen.fill((25, 25, 25))
        case 18:
            screen.fill((255, 255, 0))
            text = ammofont.render("Treasure :)", True, (255, 0, 0))
            screen.blit(text, (340, 275))

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
            if dash.timewindow(0.5) and lastkey == event.key:
                tempspeed = playerSpeed

            else:
                pass

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
            pass
        if bullet.owner == "boss" and check_collisions((bullet.x, bullet.y, bullet.w, bullet.h), (playerX, playerY, playerW, playerH)):
            bullets.remove(bullet)
            if HP_DMG.cooldown(2):
                print("player hit by boss's bullet")
                health_bar.hp = health_bar.hp - 10
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
                        appleBulletCount += 1
        #checks collision for enemies    
        elif spawner.type == "enemy":
            enemies = spawner.get_items()
            for enemy in enemies:
                enemy.move(delta)
                if enemy.inRoom == currentRoom:
                    draw(enemyImg, enemy.x, enemy.y)
                    enemy.queue_move(currentTime)
                    #Checks the collision with the player and the enemy. Removes health if collided
                    if (enemy.checkCollision(playerX, playerY, playerW, playerH)): 
                        if HP_DMG.cooldown(2):
                            print("hit by enemy")
                            health_bar.hp = health_bar.hp - 10
                    #checks the bullets for any collisions. Removes the enemy and bullet when collided
                    for bullet in bullets:
                        if (check_collisions([bullet.x, bullet.y, bullet.w, bullet.h], [enemy.x, enemy.y, enemy.w, enemy.h])):
                            print("bullet hit enemy")
                            enemies.remove(enemy)
                            bullets.remove(bullet)
                            enemies_killed += 1
                            break
                else:
                    #Resets the enemy to its original position when not in the room
                    enemy.reset_pos()

    #moves boss and detect collision
    for boss in bosses:
        if (boss.inRoom == currentRoom):
            #Makes the boss move and attempt an attack
            boss.move(delta)
            boss.attempt_attack()

            #draws the boss and its shield if not vulnerable
            if (not boss.vulnerable):
                pygame.draw.rect(screen, (100, 100, 255), (boss.x - 5, boss.y - 5, boss.w + 10, boss.h + 10))
            draw(boss_img, boss.x, boss.y)
            boss.toggle_vulnerability()

            #Queues a movement opportunity
            boss.queue_move(currentTime)   

            #Checks collision with boss and player. Removes health on collide
            if (boss.checkCollision(playerX, playerY, playerW, playerH)): 
                if HP_DMG.cooldown(2):
                    print("hit by enemy")
                    health_bar.hp = health_bar.hp - 10
            #Checks collision with boss and bullets
            for bullet in bullets:
                if (bullet.owner == "player" and check_collisions([bullet.x, bullet.y, bullet.w, bullet.h], [boss.x, boss.y, boss.w, boss.h])):
                    print("bullet hit boss")
                    #Calls the hit method in the boss. Lowers the health if vulnerable
                    m = boss.hit()
                    if (m == "killed"):
                        bosses.remove(boss)
                        enemies_killed += 1
                        rooms[16].entrances[1].open = True
                    bullets.remove(bullet)
                    break
        else:
            #resets the boss position when not in the same room
            boss.reset()

    #checks for collisions in entrances.
    for room in rooms:
        if room.num == currentRoom:
            entrance = room.checkCollisions(playerX, playerY, playerW, playerH)
            if entrance != False:
                #if r is pressed, the player will enter the room
                inEntrance = entrance.get_vals()
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
    
    #Code that makes the player's sprite different when damaged. It currently turns the player into an apple
    """
    if (HP_DMG.cooldown(2, False)):
        player(playerX, playerY)
    else:
        draw(appleImg, playerX, playerY)
    """

    #checks the spawners to see if a stockpile should be created
    check_timeouts()

    lastTime = currentTime

    pygame.display.update()