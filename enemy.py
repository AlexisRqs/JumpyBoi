import pygame
import random
from constants import *

# Define the enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 670)
        self.rect.y = random.randint(0, 470)
        self.change_x = random.choice([-2, -1, 1, 2])
        self.change_y = random.choice([-2, -1, 1, 2])

    def update(self):
        # Move the enemy
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Reverse direction if the enemy hits a wall
        if self.rect.right > 700 or self.rect.left < 0:
            self.change_x *= -1
        if self.rect.bottom > 500 or self.rect.top < 0:
            self.change_y *= -1

