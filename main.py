import pygame
import random
import time
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

COLORS = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PURPLE]

CARD_WIDTH = 100
CARD_HEIGHT = 150
MARGIN = 10
RADIUS = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Memory Card Game")

cards = COLORS * 2
random.shuffle(cards)

grid = []
for row in range(4):
    grid.append(cards[row * 4:(row + 1) * 4])

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

first_card = None
second_card = None
revealed = [[False] * 4 for _ in range(4)]
matched = [[False] * 4 for _ in range(4)]
attempts = 0
matches = 0
flip_animation = False
flip_start_time = 0
flip_duration = 0.5
card_flip_progress = 0
start_time = time.time()
end_time = 0
game_over = False
restart_prompt_shown = False

def draw_card(x, y, color, revealed=True, progress=1):
    if progress < 1:
        width = CARD_WIDTH * abs(math.cos(math.pi * progress))
        x += (CARD_WIDTH - width) / 2
    else:
        width = CARD_WIDTH
    
    if revealed:
        pygame.draw.rect(screen, color, (x, y, width, CARD_HEIGHT), border_radius=RADIUS)
    else:
        pygame.draw.rect(screen, DARK_GRAY, (x, y, width, CARD_HEIGHT), border_radius=RADIUS)
        pygame.draw.rect(screen, GRAY, (x + 5, y + 5, width - 10, CARD_HEIGHT - 10), border_radius=RADIUS-5)

def draw_timer_and_attempts():
    elapsed_time = time.time() - start_time
    timer_text = font.render(f"Time: {int(elapsed_time)}s", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 10))
    attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
    screen.blit(attempts_text, (10, 10))

def calculate_score():
    elapsed_time = end_time - start_time
    score = max(10000 - (attempts * 100 + int(elapsed_time) * 10), 0)
    return score

def display_end_screen():
    score = calculate_score()
    text1 = font.render("Congratulations!", True, BLACK)
    text2 = font.render(f"You won in {int(end_time - start_time)} seconds", True, BLACK)
    text3 = font.render(f"Score: {score}", True, BLACK)
    restart_text = small_font.render("Press R to Restart", True, BLACK)

    screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2 - text1.get_height() * 2))
    screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, SCREEN_HEIGHT // 2 + text3.get_height() * 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not flip_animation and not game_over:
            x, y = event.pos
            col = x // (CARD_WIDTH + MARGIN)
            row = y // (CARD_HEIGHT + MARGIN)
            if row < 4 and col < 4 and not revealed[row][col]:
                revealed[row][col] = True
                if first_card is None:
                    first_card = (row, col)
                elif second_card is None:
                    second_card = (row, col)
                    attempts += 1
                    flip_animation = True
                    flip_start_time = time.time()

    if flip_animation:
        card_flip_progress = (time.time() - flip_start_time) / flip_duration
        if card_flip_progress >= 1:
            card_flip_progress = 1
            r1, c1 = first_card
            r2, c2 = second_card
            if grid[r1][c1] == grid[r2][c2]:
                matched[r1][c1] = True
                matched[r2][c2] = True
                matches += 1
            else:
                revealed[r1][c1] = False
                revealed[r2][c2] = False
            first_card = None
            second_card = None
            flip_animation = False

    for row in range(4):
        for col in range(4):
            x = col * (CARD_WIDTH + MARGIN)
            y = row * (CARD_HEIGHT + MARGIN)
            if (row, col) == first_card or (row, col) == second_card:
                draw_card(x, y, grid[row][col], revealed=True, progress=card_flip_progress)
            elif revealed[row][col] or matched[row][col]:
                draw_card(x, y, grid[row][col])
            else:
                draw_card(x, y, grid[row][col], revealed=False)

    if matches == 8 and not game_over:
        game_over = True
        end_time = time.time()

    if game_over:
        display_end_screen()
        restart_prompt_shown = True

    if restart_prompt_shown:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            random.shuffle(cards)
            grid = []
            for row in range(4):
                grid.append(cards[row * 4:(row + 1) * 4])
            revealed = [[False] * 4 for _ in range(4)]
            matched = [[False] * 4 for _ in range(4)]
            attempts = 0
            matches = 0
            first_card = None
            second_card = None
            game_over = False
            restart_prompt_shown = False
            start_time = time.time()

    if not game_over:
        draw_timer_and_attempts()

    pygame.display.flip()

pygame.quit()
