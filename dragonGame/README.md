Dragon Game

This is a Python-based game created using the pygame library. In the game, you control a dragon that moves around a grid to collect food, and your score increases with each food item collected. The game ends if the dragon hits the wall or its own body.

Features:

Dragon Movement: The dragon moves in the four cardinal directions.
Food: The dragon collects food, which increases the score.
Zigzag Border: A decorative zigzag red border surrounds the grid.
Game Over: The game stops if the dragon hits the wall or itself.
Background Music: Background music plays during gameplay.
Checkered Grid: The game uses a checkered grid with alternating dark gray and black cells.
Game Over Screen: A fade effect occurs when the game ends, and a prompt to restart or quit is displayed.

Requirements:

Python 3.x
pygame library
To install pygame, run the following command:

    pip install pygame

How to Play:

The game starts with the dragon moving to the right.

Use the arrow keys to control the dragon's movement:

Up Arrow: Move up
Down Arrow: Move down
Left Arrow: Move left
Right Arrow: Move right

Collect the red food that appears on the grid to increase your score.
The game ends if the dragon collides with the wall or its own body.
Press Enter to restart the game after a game over or Esc to quit.

Game Logic:

Dragon Movement: The dragon moves on a 20x20 grid, and its position is updated every game loop. The dragon grows in size as it collects food.
Food Spawning: Food is generated at random grid positions, avoiding the edges of the screen.
Game Over: The game ends if the dragon moves out of bounds or collides with itself.

Code Breakdown:

pygame Initialization: Initializes the game window, sound system, and other necessary components.
Game Loop: Runs continuously, checking for user input, updating the game state (movement, food collection), and drawing the game elements.

Sound: Background music is played using pygame.mixer.music. If the music fails to load, an error message is printed.

Graphics:

The game screen is divided into a checkered grid with alternating dark and light colors.
The dragon is drawn as a series of connected rectangles with additional graphical details (e.g., a golden eye and horns).
A zigzag red border is drawn around the screen for extra visual effect.
A fading background effect is displayed on game over.

To Run the Game:

Download or clone the repository.
Ensure you have pygame installed.
Place a sound file DragonBack.wav in the same directory as the script.

Run the game with the following command:

        python dragon_game.py

License:
This game is open-source and free to use. Enjoy and feel free to modify it to suit your needs!