import pygame
from constants import *

class Score:
    def __init__(self):
        self.time_score = 0
        self.enemy_score = 0
        self.font = pygame.font.Font(None, 36)
        self.last_update = pygame.time.get_ticks()

    def update(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= 1000:  # Increment score every 1 second
            self.time_score += 1
            self.last_update = current_time

        total_score = self.time_score + self.enemy_score
        score_text = self.font.render(f"Score: {total_score}", True, WHITE)
        screen.blit(score_text, (SCREEN_SIZE[0] - 200, 10))

    def add_points(self, points):
        self.enemy_score += points

    def reset(self):
        self.time_score = 0
        self.enemy_score = 0
        self.last_update = pygame.time.get_ticks()

