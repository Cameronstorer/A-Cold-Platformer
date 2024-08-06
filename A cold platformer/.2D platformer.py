################### IMPORTS ##########################

import pygame
# from os import path
# import sys
# from random import randint, choice
# import enemies, math, music, menu
from constants import running, width, height, time, lives, distance, last_press, cooldown
from abc import ABC, abstractmethod

################ INITIALIZE PYGAME ###################

# initialize pygame
pygame.init()
# create a pygame clock
clock = pygame.time.Clock()
# import basic key variables
from pygame.locals import (K_LEFT, K_RIGHT, KEYDOWN, 
                           K_SPACE, K_ESCAPE, K_LSHIFT, K_a, K_d, K_w)
# set the starting window width and height
window = pygame.display.set_mode((width, height))
# set the starting window title
pygame.display.set_caption("2D")

################### CLASSES #########################

# let's create an abstract rect class
class BasicRect(ABC):
    def __init__(self, givenWidth, givenHeight):
        self.x = width//2 - (givenWidth//2)
        self.y = height//2 - (givenHeight//2)
        self.width = givenWidth
        self.height = givenHeight
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))

    @abstractmethod
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 128), self.rect)

# let's create a player class
class Player(BasicRect):
    def __init__(self):
        # initialize abstract parent class
        BasicRect.__init__(self, 50, 50)
    
    # draw this player on the screen
    def draw(self, surface):
        #255, 204, 153
        pygame.draw.rect(surface, ("Black"), self.rect)

# let's create level class
class Level():
    def __init__(self, x, y, width, height):
        # initialize the abstract super class
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.rect.Rect((self.x, self.y, self.width, self.height))
    
    # draw the level on the screen
    def draw(self, surface):
        pygame.draw.rect(surface, ("Green"), self.rect)


# create a player object
player = Player()

levels = []
piece_a = Level(0, 275, 500, 10)
levels.append(piece_a)

########## THE KEY PRESSES ########################

def handle_keys():
    for level in levels:
        key = pygame.key.get_pressed()
        # move the player:
        # left
        if key[K_LEFT] or key[K_a]:
            level.rect.move_ip(-distance, 0)
        # right
        if key[K_RIGHT] or key[K_d]:
            level.rect.move_ip(distance, 0)
        # jump
        if key[K_SPACE] or key[K_w]:

            # cooldown so the player can't spam jump
            now = pygame.time.get_ticks()
            global last_press
            if now - last_press >= cooldown:
                player.rect.move_ip(0, -distance*10)
                last_press = now
            start_time = pygame.time.get_ticks()

        # # run
        # if key[K_LSHIFT]:
        #     temp_distance = distance * 3
        # else:
        #     temp_distance = distance
        
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
        

################## MAIN LOOP ########################


# main program loop:
while running:
    #add some methods for the user to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    # the window background color
    window.fill(((156, 218, 238)))

    # some rules:
    # kill the player if the time reaches zero, or all lives are lost
    if time <= 0 or lives <= 0:
        running = False
    
    if pygame.time.get_ticks() > 400:
        for level in levels:
            print(f"{player.rect.bottom} {level.rect.top}")
            if player.rect.bottom < level.rect.top:
                if pygame.time.get_ticks() % 2 == 0:
                    player.rect.y += 2

    # if pygame.time.get_ticks() - last_press < cooldown:
    #     if pygame.time.get_ticks() % 3 == 0:
    #         for level in levels:
    #             level.rect.y += 1

    handle_keys()
    
########## DO SOME MATH ###########################

    # if player.rect.bottom 

############### DRAW OBJECTS ######################

    player.draw(window)
    for level in levels:
        level.draw(window)

    # update the screen every frame
    pygame.display.update()
    clock.tick(time)

# quit the game
pygame.quit()

    