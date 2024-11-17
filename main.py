import pygame
import random

# Initialize Pygame
pygame.init()

# Load sounds
pygame.mixer.init()
place_sound = pygame.mixer.Sound("place.wav")
clear_sound = pygame.mixer.Sound("clear.wav")
game_over_sound = pygame.mixer.Sound("gameover.wav")

# Screen dimensions and grid
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20  # Grid is 10x20
BLOCK_SIZE = 30  # Each block is 30x30 pixels

score = 0
lines_cleared = 0
level = 1
paused = False

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (128, 0, 128),  # Purple
    (255, 165, 0),  # Orange
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Game clock
clock = pygame.time.Clock()

# Grid to hold the game state
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Current piece
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def draw(self):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (
                            (self.x + col_index) * BLOCK_SIZE,
                            (self.y + row_index) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        # Rotate the tetromino 90 degrees clockwise
        new_shape = list(zip(*self.shape[::-1]))
        original_shape = self.shape
        self.shape = new_shape

        # Check for collisions after rotation
        if check_collision(self):
            self.shape = original_shape  # Revert to original if invalid

# Function to draw the grid
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Check for collisions
def check_collision(tetromino):
    for row_index, row in enumerate(tetromino.shape):
        for col_index, cell in enumerate(row):
            if cell:
                x = tetromino.x + col_index
                y = tetromino.y + row_index
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid[y][x]:
                    return True
    return False


def merge_tetromino(tetromino):
    for row_index, row in enumerate(tetromino.shape):
        for col_index, cell in enumerate(row):
            if cell:
                grid[tetromino.y + row_index][tetromino.x + col_index] = tetromino.color
    place_sound.play()  # Play placement sound

def clear_rows():
    global grid, score, lines_cleared, level
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = GRID_HEIGHT - len(new_grid)
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(cleared_rows)] + new_grid
    if cleared_rows > 0:
        clear_sound.play()  # Play clear sound
        lines_cleared += cleared_rows
        score += [0, 40, 100, 300, 1200][cleared_rows] * level
        if lines_cleared // 10 > level - 1:
            level += 1
    return cleared_rows


# Draw score and level on the screen
def draw_status():
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

next_piece = Tetromino()  # Create the first next piece

# Draw next piece
def draw_next_piece():
    font = pygame.font.SysFont("Arial", 24)
    next_text = font.render("Next:", True, WHITE)
    screen.blit(next_text, (SCREEN_WIDTH - 100, 10))

    for row_index, row in enumerate(next_piece.shape):
        for col_index, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    next_piece.color,
                    (
                        SCREEN_WIDTH - 100 + col_index * BLOCK_SIZE // 2,
                        40 + row_index * BLOCK_SIZE // 2,
                        BLOCK_SIZE // 2,
                        BLOCK_SIZE // 2,
                    ),
                )

def main():
    global grid, paused, next_piece
    running = True
    current_piece = Tetromino()
    fall_time = 0

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_status()
        draw_next_piece()

        # Draw grid
        for row_index, row in enumerate(grid):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        cell,
                        (
                            col_index * BLOCK_SIZE,
                            row_index * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused  # Toggle pause

                if not paused:
                    if event.key == pygame.K_LEFT:
                        current_piece.move(-1, 0)
                        if check_collision(current_piece):
                            current_piece.move(1, 0)
                    if event.key == pygame.K_RIGHT:
                        current_piece.move(1, 0)
                        if check_collision(current_piece):
                            current_piece.move(-1, 0)
                    if event.key == pygame.K_DOWN:
                        current_piece.move(0, 1)
                        if check_collision(current_piece):
                            current_piece.move(0, -1)
                    if event.key == pygame.K_UP:
                        current_piece.rotate()

        if paused:
            font = pygame.font.SysFont("Arial", 36)
            pause_text = font.render("Paused", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            continue

        # Gravity
        fall_time += clock.get_rawtime()
        clock.tick(30)
        if fall_time > 500 - (level - 1) * 50:  # Speed up with level
            current_piece.move(0, 1)
            if check_collision(current_piece):
                current_piece.move(0, -1)
                merge_tetromino(current_piece)
                clear_rows()
                current_piece = next_piece
                next_piece = Tetromino()  # Generate the next piece
                if check_collision(current_piece):
                    game_over_sound.play()  # Play game-over sound
                    pygame.time.wait(2000)  # Wait 2 seconds to allow the sound to finish
                    running = False
            fall_time = 0

        # Draw current piece
        current_piece.draw()

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
