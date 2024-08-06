######################################################
## NAME: Cameron Storer
## DESCRIPTION: A Cold Platformer. A platformer game with "icey" sprites
## DATE OF CREATION: 8/6/24
######################################################

################### IMPORTS ##########################

import pygame
from os import path
import sys
from random import randint, choice
import enemies, math, music, menu
from constants import running, width, height, time, lives, distance
from abc import ABC, abstractmethod

################ INITIALIZE PYGAME ###################

# initialize pygame
pygame.init()
# create a pygame clock
clock = pygame.time.Clock()
# import basic key variables
from pygame.locals import (K_LEFT, K_RIGHT, KEYDOWN, 
                           K_SPACE, K_ESCAPE, K_UP, K_DOWN, K_LSHIFT, K_w, K_a, K_s, K_d)
# set the starting window width and height
window = pygame.display.set_mode((width, height))
# set the starting window title
pygame.display.set_caption("A Cold Platformer")

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
        BasicRect.__init__(self, 80, 80)
    
    # add key binds to control player
    def handle_keys(self):
        key = pygame.key.get_pressed()
        # move the player:
        # left
        if key[K_LEFT] or key[K_a]:
            self.rect.move_ip(-distance, 0)
        # right
        if key[K_RIGHT] or key[K_d]:
            self.rect.move_ip(distance, 0)
        # up
        if key[K_UP] or key[K_w]:
            self.rect.move_ip(0, -distance)
        # down
        if key[K_DOWN] or key[K_s]:
            self.rect.move_ip(0, distance)
        # jump
        if key[K_SPACE]:
            self.rect.move_ip(1, 1)
        # run
        if key[K_LSHIFT]:
            self.rect.move_ip(-1, -1)
        
        # add some boundaries
        # right wall
        if self.rect.right > width:
            self.rect.x = width - self.rect.width
        # left wall
        if self.rect.left < 0:
            self.rect.x = 0
        # bottom wall
        if self.rect.bottom > height:
            self.rect.y = height - self.rect.height
        # top wall
        if self.rect.top < 0:
            self.rect.y = 0

    # draw this player on the screen
    def draw(self, surface):
        pygame.draw.rect(surface, ("Blue"), self.rect)

# let's create an enemy class
class Enemy(BasicRect):
    def __init__(self):
        BasicRect.__init__(self)
        self.size = randint(16, 40)
        self.rect = pygame.rect.Rect((randint(20, width-20), randint(20, height-20), self.size, self.size))
        self.alive = 1

    def draw(self, surface):
        pygame.draw.rect(surface, ("Red"), self.rect)

################## MAIN LOOP ########################

# create a player object
player = Player()

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
    window.fill(((255, 255, 255)))

    # some rules:
    # kill the player if the time reaches zero, or all lives are lost
    if time <= 0 or lives <= 0:
        running = False
    
############### DRAW OBJECTS ######################

    player.draw(window)
    player.handle_keys()
    
    # update the screen every frame
    pygame.display.update()
    clock.tick(time)

# quit the game
pygame.quit()

    