import pygame
from pygame.math import Vector2

class ConstantFirePattern():

    def __init__(
            self, 
            spawn_x: int, 
            spawn_y: int, 
            bullet_speed: int, 
            vector: Vector2
        ):

        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.bullet_speed = bullet_speed
        self.vector = vector
        self.start_time = pygame.time.get_ticks()

    def fire(self, delta_time):
        """Fires a bullet at a consistent rate"""
        elapsed = pygame.time.get_ticks() - self.start_time

        if elapsed >= 1000:
            bullet = Bullet(
                self.spawn_x,
                self.spawn_y,
                4, 
                4, 
                self.bullet_speed, 
                self.vector,
                self.level
            )
            self.start_time = pygame.time.get_ticks()