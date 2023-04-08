import pygame
import random
from bullet import *
import pygame
import random
from constants import *
from player import Player
from enemy import Enemy
from platform import Platform
from bullet import Bullet
from score import Score

# Set up the game window
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(CAPTION)

# Create the player character, platform, and enemy sprites + bullets
score = Score()
player = Player()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def create_platforms(n):
    for _ in range(n):
        platform = Platform(70, 20)
        platform.rect.x = random.randint(0, 630)
        platform.rect.y = random.randint(50, 450)
        platforms.add(platform)


def create_enemies(n):
    for _ in range(n):
        enemy = Enemy()
        enemies.add(enemy)


# Create platforms and enemies
create_platforms(10)
create_enemies(5)

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
    title = font.render(CAPTION, True, WHITE)
    start_text = font.render("[SPACEBAR] Start", True, WHITE)
    quit_text = font.render("[Q] Quit", True, WHITE)

    high_scores = load_high_scores()

    while True:
        screen.fill(BLACK)
        screen.blit(title, (SCREEN_SIZE[0] // 2 - title.get_width() // 2, SCREEN_SIZE[1] // 10))
        screen.blit(start_text, (SCREEN_SIZE[0] // 2 - start_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 70))
        screen.blit(quit_text, (SCREEN_SIZE[0] // 2 - quit_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 110))

        display_high_scores(screen, high_scores)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return False
        clock.tick(60)


def pause_menu(screen, clock):
    font = pygame.font.Font(None, 36)
    pause_text = font.render("Paused", True, WHITE)
    resume_text = font.render("[Esc] Close", True, WHITE)
    restart_text = font.render("[R] Restart", True, WHITE)
    start_menu_text = font.render("[M] Menu", True, WHITE)
    quit_text = font.render("[Q] Quit game", True, WHITE)

    while True:
        screen.blit(pause_text, (SCREEN_SIZE[0] // 2 - pause_text.get_width() // 2, SCREEN_SIZE[1] // 3))
        screen.blit(resume_text, (SCREEN_SIZE[0] // 2 - resume_text.get_width() // 2, SCREEN_SIZE[1] // 2))
        screen.blit(restart_text, (SCREEN_SIZE[0] // 2 - restart_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 50))
        screen.blit(start_menu_text, (SCREEN_SIZE[0] // 2 - start_menu_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 100))
        screen.blit(quit_text, (SCREEN_SIZE[0] // 2 - quit_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
    restart_text = font.render("[R] Restart", True, WHITE)
    start_menu_text = font.render("[M] Menu", True, WHITE)
    quit_text = font.render("[Q] Quit game", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))

    while True:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        screen.blit(restart_text, (SCREEN_SIZE[0] // 2 - restart_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 50))
        screen.blit(start_menu_text, (SCREEN_SIZE[0] // 2 - start_menu_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 100))
        screen.blit(quit_text, (SCREEN_SIZE[0] // 2 - quit_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    return True
                elif event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_m:
                    return "main_menu"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return "quit"
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
    screen.blit(title, (SCREEN_SIZE[0] // 2 - title.get_width() // 2, 100))  # Changed Y-coordinate

    for index, score in enumerate(high_scores[:5]):  # Show only the top 5 scores
        score_text = font.render(f"{index + 1}. {score}", True, WHITE)
        screen.blit(score_text,
                    (SCREEN_SIZE[0] // 2 - score_text.get_width() // 2, 150 + 30 * index))  # Changed Y-coordinate


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
            if event.key == pygame.K_ESCAPE:
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
        game_over_result = game_over(screen, clock)
        if game_over_result == "restart" or game_over_result == True:
            # Reset the game state (player, enemies, platforms, bullets, etc.)
            player = Player()
            bullets.empty()
            enemies.empty()
            score.reset()
            for i in range(5):
                enemy = Enemy()
                enemies.add(enemy)
        elif game_over_result == "main_menu":
            player = Player()
            bullets.empty()
            enemies.empty()
            score.reset()
            main_menu_result = main_menu(screen, clock)
            if main_menu_result:
                for i in range(5):
                    enemy = Enemy()
                    enemies.add(enemy)
            else:
                done = True
        elif game_over_result == "quit":
            done = True

    # Update the player character, platforms, enemies, and bullets
    player.update(platforms, enemies)
    platforms.update()
    enemies.update()
    bullets.update(enemies, score)

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
