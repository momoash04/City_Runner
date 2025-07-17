
City Runner is a vibrant, fast-paced 2D endless runner game built with Python and Pygame. The objective is to run as far as you can, dodge obstacles, and collect coins across beautifully rendered cities around the world. Unlock a diverse cast of characters, each with unique abilities, and compete against your own high score!

The game features persistent data, meaning your high score, coin balance, and purchased characters are saved automatically between sessions.

Core Features

Five Unique Arenas: Run through themed levels representing iconic cities:

Giza: Dodge obstacles amidst the pyramids and the Sphinx under a desert sun.

London: Dash past Tower Bridge and the Shard on an overcast day.

Paris: A scenic run along the Seine with Notre Dame and the Eiffel Tower in view.

Rome: Evade ancient columns and see the Colosseum at a golden sunset.

New York: Navigate a busy street with the Statue of Liberty and skyscrapers in the background.

10+ Unlockable Characters: Use coins collected during gameplay to purchase a variety of characters in the shop. Play as a stealthy Ninja, a high-jumping Superhero, a swashbuckling Pirate, a shambling Zombie, and more!

Character-Specific Abilities: Certain characters have unique gameplay traits, such as the Superhero's double jump or the Ninja's chance to gain a protective shield.

Persistent Data Saving: Your high score, total coins, and all unlocked characters are automatically saved to a gamedata.txt file, so your progress is never lost.

Dynamic Difficulty: The game's speed gradually increases the longer you survive, ensuring a constant challenge.

Intuitive UI: A clean main menu, a city selection screen with visual previews, and a character shop that shows you what you're buying.

Gameplay

The goal is to survive as long as possible by jumping over randomly spawning obstacles. Each obstacle you successfully pass increases your score by one point. Collecting coins adds to your total balance, which can be spent in the Character Shop.

Controls

SPACEBAR: Jump / Confirm Selection in Menus

P: Pause the game during a run

UP / DOWN ARROWS: Navigate lists in the menus (City Select, Character Shop)

ENTER: Select / Confirm in Menus

B: Go Back to the Main Menu from the Shop or City Select screen

Game Screens

Main Menu: The central hub where you can choose to start a game, go to the shop, select a city, or quit.

City Select: Browse the available cities. The background dynamically changes to give you a preview of the arena you are about to play in.

Character Shop: A two-column interface where you can browse characters on the left and see a live preview on the right. The shop displays the character's description and cost, or whether you already own it.

Game Over Screen: Appears when you hit an obstacle. It displays your final score for the run, your all-time high score, and your updated coin balance.

Technical Requirements

To run this game, you will need:

Python 3.x

Pygame library

How to Run the Game

Ensure Python is installed. You can download it from python.org.

Install the Pygame library. Open your terminal or command prompt and run the following command:

Generated sh
pip install pygame


Save the Code. Save the game's source code as a Python file (e.g., city_runner.py).

Sound Files (Optional). The code is set up to safely handle missing sound files and will run without them (silently). For the full experience, add the following .wav files to the same directory as your script:

jump.wav

coin.wav

lose.wav

high_score.wav

background.wav (for looping music)

Run the Game. Open a terminal or command prompt, navigate to the directory where you saved the file, and run:

Generated sh
python city_runner.py
```    The game window should now appear, and a `gamedata.txt` file will be created automatically to store your progress.
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Sh
IGNORE_WHEN_COPYING_END
Code Structure Overview

The code is organized into several logical sections:

Initialization: Imports necessary libraries, sets up the display, and defines global constants (colors, speed, gravity, etc.).

Data Management: Contains the load_data() and save_data() functions that handle reading from and writing to the gamedata.txt file.

Classes:

CartoonCharacter: The blueprint for the player, handling physics, jumping, and drawing logic for all character types.

Obstacle: Defines the behavior and appearance of the obstacles, with looks that adapt to the current city theme.

Coin: Defines the collectible coins.

Cloud: A simple class for decorative background clouds.

Background & Flag Drawing: A set of functions dedicated to rendering the unique visual elements of each city arena and its national flag.

Game State Functions: Each major part of the game (main_menu, shop_screen, game_over_screen, etc.) is managed by its own function, which contains a loop to handle its specific logic and UI.

Main Game Loop (main()): The central controller that directs the flow of the game by switching between different game states based on player input.
