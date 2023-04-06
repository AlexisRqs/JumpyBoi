import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the game window
pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jumpy v.0.2.0")

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

    def update(self):
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

# Define the platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()

# Create the player character, platform, and enemy sprites
player = Player()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
for i in range(10):
    platform = Platform(70, 20)
    platform.rect.x = random.randint(0, 630)
    platform.rect.y = random.randint(50, 450)
    platforms.add(platform)

for i in range(5):
    enemy = Enemy()
    enemies.add(enemy)

# Add a platform at the bottom of the screen
bottom_platform = Platform(700, 20)
bottom_platform.rect.x = 0
bottom_platform.rect.y = 480
platforms.add(bottom_platform)

# Set up the game loop
clock = pygame.time.Clock()
done = False

while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player.change_x = -5
            elif event.key == pygame.K_d:
                player.change_x = 5
            elif event.key == pygame.K_SPACE:
                player.jump()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_d:
                player.change_x = 0

    # Update the player character, platforms, and enemies
    player.update()
    platforms.update()
    enemies.update()

    # Draw the screen
    screen.fill(BLACK)
    platforms.draw(screen)
    enemies.draw(screen)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
