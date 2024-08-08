################### IMPORTS ##########################

import pygame
from os import path
# from random import randint, choice
# import enemies, math, music, menu, constants
from abc import ABC
################ INITIALIZE PYGAME ###################

# game defaults
screen_width, screen_height = 1000, 1000
running = True
last_jump = 100
jump_cooldown = 200

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
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2) # the 2 is border thickness (helpful for collision detection)

# player class
class Player(BasicRect):
    def __init__(self, size):
        self.x = screen_width//2 - (size[0]//2)
        self.y = screen_height//2 - (size[1]//2)
        coordinates = (self.x, self.y)
        BasicRect.__init__(self, coordinates, size)
        self.y_velocity = self.x_velocity = 0
        self.surface.fill("Red")
        self.rect = pygame.rect.Rect(coordinates, size)
        height = self.rect.y

        @property
        def y_velocity(self):
            return self._y_velocity
        @y_velocity.setter
        def y_velocity(self, value):
            if value <= 5 and value >= 0:
                self._y_velocity = value

        @property
        def x_velocity(self):
            return self._x_velocity
        @x_velocity.setter
        def x_velocity(self, value):
            if value <= 5 and value >= -5:
                self._x_velocity = value



class Platform(BasicRect):
    def __init__(self):
        self.x = 0
        self.y = 480
        self.size = (500, 20)
        coordinates = (self.x, self.y)
        # initialize abstract parent class
        BasicRect.__init__(self, coordinates, self.size)
        self.surface.fill("Blue")


# create the objects listed above
class CreateObjects():
    def __init__(self):

        # create a player object
        self.playersize = 20
        self.player = Player((self.playersize, self.playersize))
        self.platform = Platform()

    
    def blit(self):
        self.player.blit()
        self.platform.blit()

def handle_keys():
    key = pygame.key.get_pressed()
    # move the player:
    # left
    if key[K_LEFT] or key[K_a]:
        objects.player.x_velocity -= 1
    else:
        objects.player.x_velocity += .5

    # right
    if key[K_RIGHT] or key[K_d]:
        objects.player.x_velocity += 1
    else:
        objects.player.x_velocity -= .5

    # down
    if key[K_DOWN] or key[K_s]:
        objects.player.y_velocity += 1
    else:
        objects.player.y_velocity -= .5

    # jump
    if key[K_SPACE] or key[K_UP] or key[K_w]:
        start = objects.player.rect.y
        if objects.player.rect.y < start + 5:
            a = objects.player.rect.y * (-1 * objects.player.rect.y) + 5
            objects.player.rect.y = a

        objects.player.y_velocity += 1
    else:
        objects.player.y_velocity += .5

                
    # if key[K_SPACE] or key[K_w] or key[K_UP]:
    #         # jump_cooldown so the player can't spam jump
    #         global last_jump, jump_cooldown
    #         now = pygame.time.get_ticks()
    #         if now - last_jump >= jump_cooldown:
    #             objects.player.rect.y -= 30
    #             last_jump = now

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

    # handle key presses
    handle_keys()

    # player velocity based movement
    objects.player.rect.x += objects.player.x_velocity
    objects.player.rect.y += objects.player.y_velocity

    # blit things
    objects.blit()

    # gravity
    if objects.player.rect.colliderect(objects.platform.rect) == False:
        objects.player.rect.y += 4

    # update the display
    pygame.display.update()
    clock.tick(60)

    print(f"x{objects.player.rect.x}, y{objects.player.rect.y}")

# quit the game if no longer running
pygame.quit()
