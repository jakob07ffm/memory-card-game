import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Card dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 150
MARGIN = 10

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Card Game")

# Fonts
font = pygame.font.Font(None, 36)

# Create a list of pairs of numbers (1 to 8) and shuffle them
cards = list(range(1, 9)) * 2
random.shuffle(cards)

# Create a 4x4 grid of cards
grid = []
for row in range(4):
    grid.append(cards[row * 4:(row + 1) * 4])

# Game variables
first_card = None
second_card = None
revealed = [[False] * 4 for _ in range(4)]
matched = [[False] * 4 for _ in range(4)]
attempts = 0
matches = 0

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and first_card is None:
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

    # Check for matches
    if first_card and second_card:
        r1, c1 = first_card
        r2, c2 = second_card
        if grid[r1][c1] == grid[r2][c2]:
            matched[r1][c1] = True
            matched[r2][c2] = True
            matches += 1
        else:
            pygame.display.flip()
            time.sleep(1)
            revealed[r1][c1] = False
            revealed[r2][c2] = False
        first_card = None
        second_card = None

    # Draw the grid of cards
    for row in range(4):
        for col in range(4):
            x = col * (CARD_WIDTH + MARGIN)
            y = row * (CARD_HEIGHT + MARGIN)
            if revealed[row][col] or matched[row][col]:
                pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT))
                text = font.render(str(grid[row][col]), True, WHITE)
                screen.blit(text, (x + 40, y + 55))
            else:
                pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT))
                pygame.draw.rect(screen, WHITE, (x + 5, y + 5, CARD_WIDTH - 10, CARD_HEIGHT - 10))

    # Check for game over
    if matches == 8:
        text = font.render(f"You won in {attempts} attempts!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(3)
        running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
