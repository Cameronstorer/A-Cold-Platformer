################### IMPORTS ##########################

import pygame
from os import path
from random import randint, choice
# import enemies, math, music, menu, constants
from abc import ABC
################ INITIALIZE PYGAME ###################

# game defaults
screen_width, screen_height = 520, 520
running = True
last_jump = 100
jump_cooldown = 200
color_choices = ["Red", "Blue", "Green", "Pink", "Brown", "Green", "Black", "White", "Turquoise"]
round1 = True

# initialize pygame
pygame.init()
# create a pygame clock
clock = pygame.time.Clock()
# import basic key variables
from pygame.locals import (K_LEFT, K_RIGHT, KEYDOWN, 
                           K_SPACE, K_ESCAPE, K_LSHIFT, K_LCTRL, K_a, K_d, K_w, K_UP, K_DOWN, K_s)
# set the starting window properties
window = pygame.display.set_mode((screen_width, screen_height))

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
        pygame.draw.rect(window, choice(color_choices), self.rect) # the 2 is border thickness (helpful for collision detection)

# player class
class Player(BasicRect):
    def __init__(self, size):
        # self.x = screen_width//2 - (size[0]//2)
        # self.y = screen_height//2 - (size[1]//2)
        self.x = 77
        self.y = 0
        coordinates = (self.x, self.y)
        BasicRect.__init__(self, coordinates, size)
        self.y_velocity = self.x_velocity = 0
        self.surface.fill("Red")

# create the objects listed above
class CreateObjects():
    def __init__(self):

        # create a player object
        self.playersize = 20
        self.player = Player((self.playersize, self.playersize))

    
    def blit(self):
        self.player.blit()


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
                running = False

    window.fill(((156, 218, 238)))

    objects.player.surface.fill(choice(color_choices))

    if round1 == True:
        if objects.player.rect.x <= 423:
            print(f"x={objects.player.rect.x}")
            a = -.005
            b = -250
            c = 400
            objects.player.rect.y = a * ((objects.player.rect.x + b)**2) + c
            print(f"y=  {objects.player.rect.y}")
            objects.player.rect.x += 3
        else:
            round1 = False
    elif round1 == False:
        if objects.player.rect.x >= 77:
            print(f"x={objects.player.rect.x}")
            a = .005
            b = -250
            c = 100
            objects.player.rect.y = a * ((objects.player.rect.x + b)**2) + c
            print(f"y=  {objects.player.rect.y}")
            objects.player.rect.x -= 3
        else:
            round1 = True

    # blit things
    objects.blit()

    # update the display
    pygame.display.update(objects.player.rect)
    clock.tick(60)

    print(f"x{objects.player.rect.x}, y{objects.player.rect.y}")

# quit the game if no longer running
pygame.quit()
