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

EASY = (4, 4)
MEDIUM = (6, 4)
HARD = (6, 6)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Memory Card Game")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 72)

leaderboard = {'Easy': (float('inf'), 0), 'Medium': (float('inf'), 0), 'Hard': (float('inf'), 0)}

# Removed pygame.mixer initialization and music loading
# pygame.mixer.init()
# pygame.mixer.music.load(None)  # Background music removed

def generate_grid(level):
    rows, cols = level
    num_pairs = rows * cols // 2
    colors = COLORS[:num_pairs] * 2
    random.shuffle(colors)
    grid = []
    for row in range(rows):
        grid.append(colors[row * cols:(row + 1) * cols])
    return grid, rows, cols

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

def draw_timer_and_attempts(elapsed_time, attempts, level_name, hints_left):
    timer_text = font.render(f"Time: {int(elapsed_time)}s", True, BLACK)
    screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 10))
    attempts_text = font.render(f"Attempts: {attempts}", True, BLACK)
    screen.blit(attempts_text, (10, 10))
    level_text = font.render(f"Level: {level_name}", True, BLACK)
    screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
    hints_text = font.render(f"Hints Left: {hints_left}", True, BLACK)
    screen.blit(hints_text, (SCREEN_WIDTH // 2 - hints_text.get_width() // 2, 40))

def calculate_score(attempts, elapsed_time):
    score = max(10000 - (attempts * 100 + int(elapsed_time) * 10), 0)
    return score

def display_end_screen(score, level_name):
    text1 = large_font.render("You Win!", True, BLACK)
    text2 = font.render(f"Score: {score}", True, BLACK)
    restart_text = small_font.render("Press R to Restart", True, BLACK)

    screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 2 - text1.get_height() * 2))
    screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

    best_time, best_attempts = leaderboard[level_name]
    if score > best_time * best_attempts:  # Lower time and fewer attempts means better score
        leaderboard[level_name] = (score, score)

def handle_victory(matches, total_matches, elapsed_time, attempts, level_name):
    if matches == total_matches:
        score = calculate_score(attempts, elapsed_time)
        display_end_screen(score, level_name)
        return True
    return False

def animate_match(x, y, color):
    for i in range(10):
        draw_card(x, y, color, progress=1 - i / 10)
        pygame.display.flip()
        pygame.time.wait(50)

def choose_level():
    screen.fill(WHITE)
    title = large_font.render("Choose a Level", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    easy_text = font.render("1. Easy (4x4)", True, BLACK)
    medium_text = font.render("2. Medium (6x4)", True, BLACK)
    hard_text = font.render("3. Hard (6x6)", True, BLACK)

    screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, 250))
    screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, 300))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, 350))

    pygame.display.flip()

    level_choice = None
    while level_choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_choice = EASY
                    level_name = 'Easy'
                elif event.key == pygame.K_2:
                    level_choice = MEDIUM
                    level_name = 'Medium'
                elif event.key == pygame.K_3:
                    level_choice = HARD
                    level_name = 'Hard'
    return level_choice, level_name

def main_menu():
    screen.fill(WHITE)
    title = large_font.render("Memory Card Game", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    start_text = font.render("Press Enter to Start", True, BLACK)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 250))

    leaderboard_text = font.render("Press L to View Leaderboard", True, BLACK)
    screen.blit(leaderboard_text, (SCREEN_WIDTH // 2 - leaderboard_text.get_width() // 2, 300))

    exit_text = font.render("Press Esc to Exit", True, BLACK)
    screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 350))

    pygame.display.flip()

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_menu = False
                elif event.key == pygame.K_l:
                    show_leaderboard()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def show_leaderboard():
    screen.fill(WHITE)
    title = large_font.render("Leaderboard", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    y_pos = 200
    for level, (time, attempts) in leaderboard.items():
        text = font.render(f"{level}: Best Score - {time} (Attempts: {attempts})", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_pos))
        y_pos += 50

    back_text = small_font.render("Press B to go back", True, BLACK)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, y_pos + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return

main_menu()
running = True
while running:
    level, level_name = choose_level()
    grid, rows, cols = generate_grid(level)
    revealed = [[False] * cols for _ in range(rows)]
    matched = [[False] * cols for _ in range(rows)]
    attempts = 0
    matches = 0
    flip_animation = False
    flip_start_time = 0
    flip_duration = 0.5
    card_flip_progress = 0
    start_time = time.time()
    hints_left = 3
    game_over = False
    first_card = None
    second_card = None

    while not game_over:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not flip_animation and not game_over:
                x, y = event.pos
                col = x // (CARD_WIDTH + MARGIN)
                row = y // (CARD_HEIGHT + MARGIN)
                if row < rows and col < cols and not revealed[row][col]:
                    revealed[row][col] = True
                    if first_card is None:
                        first_card = (row, col)
                    elif second_card is None:
                        second_card = (row, col)
                        attempts += 1
                        flip_animation = True
                        flip_start_time = time.time()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h and hints_left > 0:
                    hints_left -= 1
                    for r in range(rows):
                        for c in range(cols):
                            revealed[r][c] = True
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    for r in range(rows):
                        for c in range(cols):
                            if not matched[r][c]:
                                revealed[r][c] = False

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
                    animate_match(r1 * (CARD_WIDTH + MARGIN), c1 * (CARD_HEIGHT + MARGIN), grid[r1][c1])
                    animate_match(r2 * (CARD_WIDTH + MARGIN), c2 * (CARD_HEIGHT + MARGIN), grid[r2][c2])
                else:
                    revealed[r1][c1] = False
                    revealed[r2][c2] = False
                first_card = None
                second_card = None
                flip_animation = False

        for row in range(rows):
            for col in range(cols):
                x = col * (CARD_WIDTH + MARGIN)
                y = row * (CARD_HEIGHT + MARGIN)
                if (row, col) == first_card or (row, col) == second_card:
                    draw_card(x, y, grid[row][col], revealed=True, progress=card_flip_progress)
                elif revealed[row][col] or matched[row][col]:
                    draw_card(x, y, grid[row][col])
                else:
                    draw_card(x, y, grid[row][col], revealed=False)

        elapsed_time = time.time() - start_time
        if handle_victory(matches, rows * cols // 2, elapsed_time, attempts, level_name):
            game_over = True

        if not game_over:
            draw_timer_and_attempts(elapsed_time, attempts, level_name, hints_left)

        pygame.display.flip()

pygame.quit()
