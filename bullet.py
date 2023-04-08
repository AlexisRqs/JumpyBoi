import pygame
from constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):  # Fixed method name and added x, y arguments
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x  # Set the bullet's initial position
        self.rect.y = y  # Set the bullet's initial position
        self.speed = 10
        self.direction = direction

    def update(self, enemies, score):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed

        # Check for collisions with enemies
        enemy_hit_list = pygame.sprite.spritecollide(self, enemies, True)
        for enemy in enemy_hit_list:
            # Remove the bullet when it hits an enemy
            self.kill()
            score.add_points(10)

        # Remove the bullet when it goes off-screen
        if self.rect.right < 0 or self.rect.left > 700 or self.rect.top > 500 or self.rect.bottom < 0:
            self.kill()
