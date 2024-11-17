# Tetris Game

A simple Tetris game built in Python using the Pygame library. This project includes basic Tetris functionalities such as moving and rotating tetrominoes, clearing lines, leveling up, and keeping track of the score. Sound effects are also included to enhance gameplay.

## Features

Classic Tetris gameplay with 7 different tetromino shapes.

Ability to move left, right, down, and rotate pieces.

Automatic dropping of pieces with increasing speed as the level advances.

Score and level tracking, with the score increasing based on the number of rows cleared.

Pause functionality.

Preview of the next tetromino.

Sound effects for piece placement, row clearing, and game over.

## Requirements

Python 3.x

Pygame library

Installation

Clone the repository:

git clone https://github.com/yourusername/tetris-game.git

Navigate to the project directory:

cd tetris-game

Install Pygame:

pip install pygame

## Running the Game

To run the Tetris game, simply execute the Python script:

python tetris.py

## Controls

Arrow Keys:

Left Arrow: Move the tetromino left.

Right Arrow: Move the tetromino right.

Down Arrow: Speed up the tetromino's fall.

Up Arrow: Rotate the tetromino.

P Key: Pause and resume the game.

## Gameplay Overview

The game screen is a grid where tetromino pieces fall from the top.

The player can move the pieces left, right, or down, and rotate them to fit into empty spaces.

When a row is completely filled, it gets cleared, and the player earns points.

The level increases every 10 rows cleared, making the pieces fall faster.

The game ends when the tetrominoes reach the top of the screen.

## Scoring System

Clearing 1 row: 40 points × level

Clearing 2 rows: 100 points × level

Clearing 3 rows: 300 points × level

Clearing 4 rows (Tetris): 1200 points × level

## Sound Effects

Piece Placement: A sound plays when a tetromino is placed.

Row Clearing: A sound plays when one or more rows are cleared.

Game Over: A sound plays when the game ends.

## Future Improvements

Add more advanced rotation mechanics for better piece fitting.

Implement saving and loading of the game state.

Add a leaderboard to track high scores.

Improve graphics with textures and animations.

## License

This project is open-source and available under the MIT License.

## Credits

Pygame Library: Used to create the game interface and handle user input.

Sounds: Created using various open-source sound libraries.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue if you find a bug or have a suggestion for a new feature.

Contact

For any inquiries, please reach out to davidnjoroge560@gmail.com
