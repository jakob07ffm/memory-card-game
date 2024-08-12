import pygame
import random
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (255, 165, 0), (128, 0, 128)
]

CARD_WIDTH = 100
CARD_HEIGHT = 150
MARGIN = 10

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

running = True
game_over = False
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

    if flip_animation and time.time() - flip_start_time >= flip_duration:
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
            if revealed[row][col] or matched[row][col]:
                pygame.draw.rect(screen, grid[row][col], (x, y, CARD_WIDTH, CARD_HEIGHT))
            else:
                pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
                pygame.draw.rect(screen, BLACK, (x + 5, y + 5, CARD_WIDTH - 10, CARD_HEIGHT - 10))

    text = font.render(f"Attempts: {attempts}", True, BLACK)
    screen.blit(text, (10, 10))
    text = font.render(f"Matches: {matches}/8", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH - 200, 10))

    if matches == 8 and not game_over:
        text = font.render(f"You won in {attempts} attempts!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        game_over = True

    if game_over:
        restart_text = small_font.render("Press R to Restart", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

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

    pygame.display.flip()

pygame.quit()
