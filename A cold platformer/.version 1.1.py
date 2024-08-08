######################################################
## NAME: Cameron Storer
## DESCRIPTION: A Cold Platformer. A platformer game with "icey" sprites
## DATE OF CREATION: 8/6/24
##
################### IMPORTS ##########################

import pygame
from os import path
# from random import randint, choice
# import enemies, math, music, menu, constants
from abc import ABC

################### DEFAULTS #########################

# game defaults
screen_width, screen_height = 500, 500
running = True
score = 0
lives = 6
time = 256
start_time = 0
distance = 5
temp_distance = distance
platforms = []
last_press = 400
cooldown = 500
DEBUG = False
paused = False
jumpheight = 100
jumpstart = 0
jumping = False
runspeed = 2
fallspeed = 4
jumpspeed = 12

################ INITIALIZE PYGAME ###################

# initialize pygame
pygame.init()
# create a pygame clock
clock = pygame.time.Clock()
# import basic key variables
from pygame.locals import (K_LEFT, K_RIGHT, KEYDOWN, 
                           K_SPACE, K_ESCAPE, K_LSHIFT, K_LCTRL, K_a, K_d, K_w, K_UP)
# set the starting window properties
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A Cold Platformer")

################### CLASSES #########################

# type abstract class
class BasicRect(ABC):
    def __init__(self, coordinates, size):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = size[0]
        self.height = size[1]
        self.rect = pygame.rect.Rect(coordinates, size)
        self.surface = pygame.Surface(size)

    # blit the player on the screen
    def blit(self):
        window.blit(self.surface, self.rect)
        # lets look at our collision detection
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2) # the 2 is border thickness (helpful for collision detection)

# player class
class Player(BasicRect):
    def __init__(self, size):
        self.x = screen_width//2 - (size[0]//2)
        # self.y = screen_height//2 - (size[1]//2)
        self.y = 422
        coordinates = (self.x, self.y)
        # initialize abstract parent class
        BasicRect.__init__(self, coordinates, size)
        self.surface.fill("Red")

# platform class
class Platform(BasicRect):
    def __init__(self, coordinates, size):
        BasicRect.__init__(self, coordinates, size)
        self.surface.fill("Green")

# tracker class
class Tracker(Platform):
    def __init__(self):
        Platform.__init__(self, (250, 250), (2, 2))
        self.surface.fill("Black")

# create the objects listed above
class CreateObjects():
    def __init__(self):

        # create a player object
        self.playersize = 20
        self.player = Player((self.playersize, self.playersize))

        # create tracker object
        self.tracker = Tracker()

        # create platform objects
        self.coordinates =  [(0,460),  (0,0),   (500, 0),   (0, 350)]
        self.size =         [(500,40), (40,500),  (40,500), (500, 40)]

        for i in range(len(self.coordinates)):
            platform = Platform((self.coordinates[i][0], self.coordinates[i][1]),
                        (self.size[i][0], self.size[i][1]))
            platforms.append(platform)

        platforms.append(self.tracker)
    
    def blit(self):
        self.player.blit()
        global platforms
        [platform.blit() for platform  in platforms]

############## SOME FUNCTIONS #######################

def handle_keys():
    global temp_distance
    key = pygame.key.get_pressed()
    # move the player:
    
    for platform in platforms:
        # left
        if key[K_LEFT] or key[K_a]:
            platform.rect.x += temp_distance

        # right
        if key[K_RIGHT] or key[K_d]:
            platform.rect.x -= temp_distance

    # jump
    if key[K_SPACE] or key[K_w] or key[K_UP]:
        # only allow the player to jump from the ground
        if objects.player.rect.collidelist(platforms) != -1:
            # how high the player can jump
            global jump_height, jumpstart, jumping, last_press
            # cooldown so the player can't spam jump
            now = pygame.time.get_ticks()
            if now - last_press >= cooldown:
                jumpstart = objects.player.rect.y
                jumping = True
                # make player jump
                # objects.player.rect.move_ip(0, -distance*jump_height)
                last_press = now
            
    # run
    if key[K_LSHIFT] or key[K_LCTRL]:
        global runspeed
        temp_distance = distance * runspeed
    else:
        temp_distance = distance

def collisions():




    if objects.player.rect.collidelist(platforms) != -1:
        for platform in platforms:

            if objects.player.rect.left == platform.rect.right:
                platform.rect.x += 2


            elif objects.player.rect.right == platform.rect.left:
                platform.rect.x -= 3
            
def gravity():
    if objects.player.rect.collidelist(platforms) == -1:
        objects.player.rect.y += fallspeed

def initJump():
    global jumpstart, jumping
    if objects.player.rect.y > jumpstart - jumpheight:
        objects.player.rect.y -= jumpspeed
    else:
        jumping = False

###############   MAIN PROGRAM LOOP   ###############

# create all objects
objects = CreateObjects()

# start program
while running:

    # get the current event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if paused == False:
                    paused = True
                    pygame.mixer.music.pause()
                    unpaused = False
                else:
                    paused = False
                    pygame.mixer.music.unpause()
                
                # running = False
    
    if paused == False:

        window.fill(((156, 218, 238)))

        # handle keystrokes
        handle_keys()

        # handle collisions
        collisions()

        # make the player fall
        gravity()

        # make the player jump
        if jumping:
            initJump()

        # blit things
        objects.blit()

        # update the display
        pygame.display.update()
        clock.tick(60)
        time = start_time - (pygame.time.get_ticks()//1000)

        # some debugging helpers
        if DEBUG:
            print(f"player x:  {objects.tracker.rect.x},  y:  {objects.player.rect.y}")
        
# quit the game if no longer running
pygame.quit()
