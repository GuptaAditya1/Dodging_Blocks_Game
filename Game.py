"""
DODGE THE BLOCKS — a tiny Pygame arcade

How to run:
1) pip install pygame
2) python dodge_the_blocks.py  (or run this file)

Goal:
- Move left/right to dodge falling blocks.
- Survive as long as possible to increase your score.

Controls:
- Left/Right arrows or A/D to move
- Enter/Space to start/restart
- Esc to quit
"""

import random
import sys
import pygame

# --- Config ---
WIDTH, HEIGHT = 480, 720
FPS = 60
PLAYER_SIZE = (50, 20)
PLAYER_SPEED = 6
BLOCK_MIN_SIZE = 20
BLOCK_MAX_SIZE = 60
BLOCK_MIN_SPEED = 3
BLOCK_MAX_SPEED = 8
SPAWN_EVERY_MS = 700  # spawn interval for blocks
MARGIN = 8

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 36, bold=True)

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, SPAWN_EVERY_MS)

# --- Helpers ---
def make_block():
    w = random.randint(BLOCK_MIN_SIZE, BLOCK_MAX_SIZE)
    h = random.randint(BLOCK_MIN_SIZE, BLOCK_MAX_SIZE)
    x = random.randint(0, WIDTH - w)
    speed = random.randint(BLOCK_MIN_SPEED, BLOCK_MAX_SPEED)
    color = (random.randint(120, 255), random.randint(80, 200), random.randint(80, 200))
    return pygame.Rect(x, -h, w, h), speed, color


def reset_game():
    player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE[0] // 2, HEIGHT - 80, *PLAYER_SIZE)
    blocks = []
    score = 0.0
    alive = True
    return player, blocks, score, alive


player, blocks, score, alive = reset_game()

# --- Game Loop ---
running = True
start_screen = True

while running:
    dt = clock.tick(FPS) / 1000.0  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if start_screen and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                start_screen = False
            elif not alive and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                player, blocks, score, alive = reset_game()
        elif event.type == SPAWN_EVENT and not start_screen and alive:
            blocks.append(make_block())

    keys = pygame.key.get_pressed()

    # Update only when game is active
    if not start_screen and alive:
        move = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        player.x += int(move) * PLAYER_SPEED
        player.x = max(MARGIN, min(WIDTH - player.width - MARGIN, player.x))

        # Move blocks
        to_remove = []
        for i, (rect, speed, color) in enumerate(blocks):
            rect.y += speed
            if rect.top > HEIGHT:
                to_remove.append(i)
        # cleanup off-screen blocks
        for i in reversed(to_remove):
            blocks.pop(i)

        # Collision
        for rect, speed, color in blocks:
            if rect.colliderect(player):
                alive = False
                break

        # Score increases with time
        score += dt

    # --- Draw ---
    screen.fill((18, 18, 22))

    # ground line
    pygame.draw.line(screen, (40, 40, 48), (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 2)

    # Draw player
    pygame.draw.rect(screen, (240, 240, 255), player, border_radius=6)

    # Draw blocks
    for rect, speed, color in blocks:
        pygame.draw.rect(screen, color, rect, border_radius=4)

    # UI text
    if start_screen:
        title = big_font.render("DODGE THE BLOCKS", True, (255, 255, 255))
        prompt = font.render("Press Enter/Space to start", True, (200, 200, 210))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 3 + 48))
    else:
        score_text = font.render(f"Score: {int(score * 10)}", True, (230, 230, 235))
        screen.blit(score_text, (MARGIN, MARGIN))

    if not alive:
        over = big_font.render("Game Over", True, (255, 200, 200))
        retry = font.render("Press Enter/Space to retry", True, (220, 220, 230))
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(retry, (WIDTH // 2 - retry.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
