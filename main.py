import pygame
import random

# Initialize Pygame
pygame.init()

# Load sounds
pygame.mixer.init()
place_sound = pygame.mixer.Sound("place.wav")  # Sound when a piece is placed
clear_sound = pygame.mixer.Sound("clear.wav")  # Sound when rows are cleared
game_over_sound = pygame.mixer.Sound("gameover.wav")  # Sound when the game ends

# Screen dimensions and grid
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600  # The game screen size in pixels
GRID_WIDTH, GRID_HEIGHT = 10, 20  # Number of blocks horizontally and vertically in the grid
BLOCK_SIZE = 30  # Size of each block in pixels

# Game variables
score = 0
lines_cleared = 0
level = 1
paused = False  # Variable to track if the game is paused

# Colors used in the game
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

# Tetromino shapes definition
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
    [[0, 1, 1], [1, 1, 0]],  # S shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Game clock to control game speed
clock = pygame.time.Clock()

# Grid to store the current state of the board (filled cells and empty cells)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Tetromino class representing the falling piece
class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)  # Randomly select a shape
        self.color = random.choice(COLORS)  # Randomly select a color for the shape
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2  # Starting x position at the center of the grid
        self.y = 0  # Starting y position at the top of the grid

    def draw(self):
        # Draw each block of the current tetromino on the screen
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
        # Move the tetromino by a specified number of blocks
        self.x += dx
        self.y += dy

    def rotate(self):
        # Rotate the tetromino 90 degrees clockwise
        new_shape = list(zip(*self.shape[::-1]))
        original_shape = self.shape
        self.shape = new_shape

        # If rotation leads to collision, revert back to the original shape
        if check_collision(self):
            self.shape = original_shape

# Draw the grid lines on the game screen
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Check if the current position of a tetromino results in a collision
def check_collision(tetromino):
    for row_index, row in enumerate(tetromino.shape):
        for col_index, cell in enumerate(row):
            if cell:
                x = tetromino.x + col_index
                y = tetromino.y + row_index
                # Check if the tetromino is out of bounds or overlapping with filled cells
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid[y][x]:
                    return True
    return False

# Merge the current tetromino into the grid when it reaches the bottom or hits another piece
def merge_tetromino(tetromino):
    for row_index, row in enumerate(tetromino.shape):
        for col_index, cell in enumerate(row):
            if cell:
                grid[tetromino.y + row_index][tetromino.x + col_index] = tetromino.color
    place_sound.play()  # Play placement sound

# Clear rows that are completely filled
def clear_rows():
    global grid, score, lines_cleared, level
    # Remove all full rows from the grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = GRID_HEIGHT - len(new_grid)
    # Add empty rows at the top to keep the grid size constant
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(cleared_rows)] + new_grid

    if cleared_rows > 0:
        clear_sound.play()  # Play clear sound
        lines_cleared += cleared_rows
        score += [0, 40, 100, 300, 1200][cleared_rows] * level  # Update score based on rows cleared

        # Increase level every 10 lines
        if lines_cleared // 10 > level - 1:
            level += 1

# Draw the current score and level on the screen
def draw_status():
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

# Create the next piece to be displayed
next_piece = Tetromino()

# Draw the next piece in a small preview box
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

# Main game loop
def main():
    global grid, paused, next_piece
    running = True
    current_piece = Tetromino()
    fall_time = 0

    while running:
        screen.fill(BLACK)  # Clear the screen
        draw_grid()  # Draw the grid lines
        draw_status()  # Draw the score and level
        draw_next_piece()  # Draw the next piece preview

        # Draw each block of the current grid state (occupied blocks)
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

        # Handle user input events
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

        # Pause game logic
        if paused:
            font = pygame.font.SysFont("Arial", 36)
            pause_text = font.render("Paused", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            continue

        # Control gravity - automatically drop pieces over time
        fall_time += clock.get_rawtime()
        clock.tick(30)
        if fall_time > 500 - (level - 1) * 50:  # Reduce delay as level increases
            current_piece.move(0, 1)
            if check_collision(current_piece):
                current_piece.move(0, -1)  # Move back if collision occurs
                merge_tetromino(current_piece)
                clear_rows()
                current_piece = next_piece  # Replace with the next piece
                next_piece = Tetromino()  # Generate a new next piece
                if check_collision(current_piece):
                    game_over_sound.play()  # Play game-over sound
                    pygame.time.wait(2000)  # Wait 2 seconds for the sound to finish
                    running = False
            fall_time = 0

        # Draw the current piece
        current_piece.draw()

        # Update the display
        pygame.display.flip()

    pygame.quit()  # Quit Pygame

# Run the main function
if __name__ == "__main__":
    main()
