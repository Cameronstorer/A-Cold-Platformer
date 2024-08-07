################### IMPORTS ##########################

import pygame
# from os import path
# import sys
# from random import randint, choice
# import enemies, math, music, menu
# from constants import running, width, height, time, lives, distance, last_press, cooldown
from abc import ABC, abstractmethod

# window defaults
width, height = 500, 500

# game defaults
running = True
score = 0
lives = 6
time = 256
start_time = 0
distance = 5
temp_distance = distance
platforms = []
last_press = 0
cooldown = 400
DEBUG = True
paused = False

################ INITIALIZE PYGAME ###################

# initialize pygame
pygame.init()
# create a pygame clock
clock = pygame.time.Clock()
# import basic key variables
from pygame.locals import (K_LEFT, K_RIGHT, KEYDOWN, 
                           K_SPACE, K_ESCAPE, K_LSHIFT, K_LCTRL, K_a, K_d, K_w, K_UP)
# set the starting window width and height
window = pygame.display.set_mode((width, height))
# set the starting window title
pygame.display.set_caption("A Cold Platformer")
pygame.mouse.set_visible(False)

################### CLASSES #########################

# let's create a player class
class Player():
    def __init__(self):
        # initialize abstract parent class
        self.x = width//2 - (50//2)
        # self.y = height//2 - (50//2)
        self.y = 350
        self.width = 50
        self.height = 50
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))

    # draw this player on the screen
    def draw(self, surface):
        #255, 204, 153
        pygame.draw.rect(surface, ("Black"), self.rect)

# let's create level class
class Platform():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))
    
    # draw the platform on the screen
    def draw(self, surface):
        pygame.draw.rect(surface, ("Green"), self.rect)

class createObjects():
    def __init__(self):
        # create a player object
        self.player = Player()

        # create platforms
        self.x_coordinates = [0, 0, 0]
        self.y_coordinates = [400, 310, 330]
        self.platform_widths = [500, 10, 250]
        self.platform_heights = [10, 70, 10]

        for i in range(len(self.x_coordinates)):
            a = Platform(self.x_coordinates[i], self.y_coordinates[i], self.platform_widths[i], self.platform_heights[i])
            platforms.append(a)

    ############## SOME FUNCTIONS ####################################

    def draw(self):

        # draw the player
        self.player.draw(window)

        # draw the levels
        for platform in platforms:
            platform.draw(window)

objects = createObjects()

def collisions():
        
        # for i in enemyrects:
        #     if pygame.Rect.colliderect(player.rect, i):
        #         global last_hit_time
        #         cooldown = 500
        #         # cooldown so the player has a safety time
        #         now = pygame.time.get_ticks()
        #         if now - last_hit_time >= cooldown:
        #             global lives
        #             lives -= 1
        #             if lives <= 0:
        #                 player.alive = 0
        #                 global running
        #                 running = False
        #             last_hit_time = now

    if objects.player.rect.collidelist(platforms):
        objects.player.rect.y += 2

def handle_keys():
    global temp_distance
    key = pygame.key.get_pressed()
    # move the player:
    a = 0
    b = 0
    for platform in platforms:
        if objects.player.rect.collidepoint(platform.rect.left, platform.rect.y):
            a = 1
        if objects.player.rect.collidepoint(platform.rect.right, platform.rect.y):
            a = 2
        if objects.player.rect.collidepoint(platform.rect.x, platform.rect.bottom):
            b = 1
        if a == 0 or a == 2:
            # left
            if key[K_LEFT] or key[K_a]:
                platform.rect.x += temp_distance
        if a == 0 or a == 1:
            # right
            if key[K_RIGHT] or key[K_d]:
                platform.rect.x -= temp_distance
            # jump
        if b == 0:
            if key[K_SPACE] or key[K_w] or key[K_UP]:

                # cooldown so the player can't spam jump
                jump_height = 40
                now = pygame.time.get_ticks()
                global last_press
                if now - last_press >= cooldown:
                    objects.player.rect.move_ip(0, -distance*jump_height)
                    for platform in platforms:
                        if pygame.Rect.colliderect(objects.player.rect, platform.rect):
                            objects.player.rect.move_ip(0, distance*jump_height)
                    last_press = now

        # run
        if key[K_LSHIFT] or key[K_LCTRL]:
            temp_distance = distance * 3
        else:
            temp_distance = distance

    a = 0
    b = 0
        

        # # add some boundaries
        # # right wall
        # if level.rect.right > width:
        #     level.rect.x = width - level.rect.width
        # # left wall
        # if level.rect.left < 0:
        #     level.rect.x = 0
        # # bottom wall
        # if level.rect.bottom > height:
        #     level.rect.y = height - level.rect.height
        # # top wall
        # if level.rect.top < 0:
        #     level.rect.y = 0

###############   MAIN PROGRAM LOOP   ############################

# start program
while running:

    # get the current event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if unpaused == True:
                    paused = True
                    pygame.mixer.music.pause()
                    unpaused = False
                else:
                    paused = False
                    pygame.mixer.music.unpause()
                    unpaused = True
                
                # running = False
    
    if paused == False:

        window.fill(((156, 218, 238)))

        # move things lol
        # movethings(choice)
        handle_keys()

        # collisions
        collisions()

        # update/create the on-screen text
        # createtext()

        # draw the rectangles and texts
        objects.draw()

        # update the display
        pygame.display.update()
        clock.tick(60)
        time = start_time - (pygame.time.get_ticks()//1000)

        # some debugging helpers
        if DEBUG:
            lists = [platforms]
            j = ["platforms"]
            for i in lists:
                print(f"{j[lists.index(i)]} has {len(i)}")
            print(f"x = {objects.player.rect.x}, y = {objects.player.rect.y}")
        
        # # death if time runs out
        # if time <= 0:
        #     running = False
        

# quit the game if no longer running
pygame.quit()
