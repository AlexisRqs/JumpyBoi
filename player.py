import pygame
from constants import *

# Define the player character class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.change_x = 0
        self.change_y = 0

    def update(self, platforms, enemies):
        # Apply gravity
        self.change_y += 0.5

        # Move horizontally
        self.rect.x += self.change_x

        # Check for collisions with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.change_x > 0:
                self.rect.right = platform.rect.left
            elif self.change_x < 0:
                self.rect.left = platform.rect.right

        # Move vertically
        self.rect.y += self.change_y

        # Check for collisions with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = platform.rect.bottom
                self.change_y = 0

        # Check for collisions with enemies
        enemy_hit_list = pygame.sprite.spritecollide(self, enemies, False)
        if enemy_hit_list:
            # The player character dies when it collides with an enemy
            self.kill()

    def jump(self):
        # Make the player character jump
        self.change_y = -10

