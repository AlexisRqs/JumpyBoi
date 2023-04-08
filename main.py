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
pygame.display.set_caption("Jumpy v.0.3.1")


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

    def update(self):
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
        screen.blit(score_text, (size[0] - 200, 10))

    def add_points(self, points):
        self.enemy_score += points

    def reset(self):
        self.time_score = 0
        self.enemy_score = 0
        self.last_update = pygame.time.get_ticks()


# Create the player character, platform, and enemy sprites + bullets
score = Score()
player = Player()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

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

# Create a custom event for spawning enemies
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 10000)  # 10000 milliseconds = 10 seconds


def main_menu(screen, clock):
    font = pygame.font.Font(None, 36)
    title = font.render("Jumpy v.0.3.1", True, WHITE)
    start_text = font.render("Press 'S' to Start", True, WHITE)
    quit_text = font.render("Press 'Q' to Quit", True, WHITE)

    high_scores = load_high_scores()

    while True:
        screen.fill(BLACK)
        screen.blit(title, (size[0] // 2 - title.get_width() // 2, size[1] // 3))
        screen.blit(start_text, (size[0] // 2 - start_text.get_width() // 2, size[1] // 2))
        screen.blit(quit_text, (size[0] // 2 - quit_text.get_width() // 2, size[1] // 2 + 50))

        display_high_scores(screen, high_scores)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False
        clock.tick(60)


def pause_menu(screen, clock):
    font = pygame.font.Font(None, 36)
    pause_text = font.render("Paused", True, WHITE)
    resume_text = font.render("Press 'P' to resume", True, WHITE)
    restart_text = font.render("Press 'R' to restart", True, WHITE)
    start_menu_text = font.render("Press 'M' to return to start menu", True, WHITE)
    quit_text = font.render("Press 'Q' to quit", True, WHITE)

    while True:
        screen.fill(BLACK)
        screen.blit(pause_text, (size[0] // 2 - pause_text.get_width() // 2, size[1] // 3))
        screen.blit(resume_text, (size[0] // 2 - resume_text.get_width() // 2, size[1] // 2))
        screen.blit(restart_text, (size[0] // 2 - restart_text.get_width() // 2, size[1] // 2 + 50))
        screen.blit(start_menu_text, (size[0] // 2 - start_menu_text.get_width() // 2, size[1] // 2 + 100))
        screen.blit(quit_text, (size[0] // 2 - quit_text.get_width() // 2, size[1] // 2 + 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"
                elif event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_m:
                    return "main_menu"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return "quit"
        clock.tick(60)



# Function to display the "Game Over" message and handle restarting the game
def game_over(screen, clock):
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Press 'F' to play again.", True, WHITE)
    text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    return True
        clock.tick(60)


def save_high_score(score):
    with open("high_scores.txt", "a") as file:
        file.write(str(score) + "\n")


def load_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            high_scores = [int(line.strip()) for line in file.readlines()]
            high_scores.sort(reverse=True)
            return high_scores
    except FileNotFoundError:
        return []


def display_high_scores(screen, high_scores):
    font = pygame.font.Font(None, 36)
    title = font.render("High Scores:", True, WHITE)
    screen.blit(title, (size[0] // 2 - title.get_width() // 2, 100))  # Changed Y-coordinate

    for index, score in enumerate(high_scores[:5]):  # Show only the top 5 scores
        score_text = font.render(f"{index + 1}. {score}", True, WHITE)
        screen.blit(score_text, (size[0] // 2 - score_text.get_width() // 2, 150 + 30 * index))  # Changed Y-coordinate


# Call the main menu before the game loop
if not main_menu(screen, clock):
    done = True

while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == SPAWN_ENEMY_EVENT:  # Spawn enemy every 15 seconds
            enemy = Enemy()
            enemies.add(enemy)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_result = pause_menu(screen, clock)
                if pause_result == "quit":
                    done = True
                    break
                elif pause_result == "restart":
                    player = Player()
                    bullets.empty()
                    enemies.empty()
                    score.reset()
                    for i in range(5):
                        enemy = Enemy()
                        enemies.add(enemy)
                    break
                elif pause_result == "main_menu":
                    player = Player()
                    bullets.empty()
                    enemies.empty()
                    score.reset()
                    main_menu_result = main_menu(screen, clock)
                    if main_menu_result == "main":
                        for i in range(5):
                            enemy = Enemy()
                            enemies.add(enemy)
                    elif main_menu_result == "quit":
                        done = True
                        break
            elif event.key == pygame.K_LEFT:
                player.change_x = -5
            elif event.key == pygame.K_RIGHT:
                player.change_x = 5
            elif event.key == pygame.K_UP:
                player.jump()
            elif event.key == pygame.K_SPACE:  # Separate bullet firing events
                if player.change_x > 0:
                    direction = "right"
                elif player.change_x < 0:
                    direction = "left"
                else:  # If the player is not moving, use the default direction
                    direction = "right"
                bullet = Bullet(player.rect.centerx, player.rect.centery, direction)
                bullets.add(bullet)

    # Check for collisions with enemies
    enemy_hit_list = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_hit_list:
        total_score = score.time_score + score.enemy_score
        save_high_score(total_score)
        # The player character dies when it collides with an enemy
        if game_over(screen, clock):
            # Reset the game state (player, enemies, platforms, bullets, etc.)
            player = Player()
            bullets.empty()
            enemies.empty()
            score.reset()
            for i in range(5):
                enemy = Enemy()
                enemies.add(enemy)
        else:
            done = True

    # Update the player character, platforms, enemies, and bullets
    player.update()
    platforms.update()
    enemies.update()
    bullets.update()

    # Draw the screen
    screen.fill(BLACK)
    score.update(screen)
    platforms.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Quit the game
pygame.quit()
