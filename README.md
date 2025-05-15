UNO Card Game with AI Opponent
Welcome to our UNO Card Game, a single-player game developed as a semester project for our Artificial Intelligence course. Built in Python using Pygame, this game features a heuristic-based AI opponent that plays strategically against the player. The code is modular, well-documented, and includes an enhanced UI with centered cards, readable text, and hover effects.
Project Overview
UNO is a classic card game where players discard cards by matching colors or numbers, with action cards (Skip, Reverse, DrawTwo) and Wild cards adding strategic depth. This project is a single-player version where the player competes against an AI opponent. Key features include:

Full implementation of UNO rules.
A smart AI opponent using heuristic-based decision-making.
Modular code structure for maintainability and reusability.
Polished UI with no card overlap, clear text, and visual effects.

Installation
To run the game locally, follow these steps:
Prerequisites

Python 3.12+ (tested with 3.12.0)
Pygame 2.6.1: For graphics and event handling
NumPy: For sound effects
A system with a graphical interface (Windows, macOS, Linux)

Steps

Clone the Repository:
git clone https://github.com/[your-username]/uno-card-game.git
cd uno-card-game


Install Dependencies:
pip install pygame numpy


Run the Game:
python main.py


Optional (Browser):

The game is compatible with Pyodide for browser-based execution. Load all files (constants.py, card.py, game_logic.py, ui.py, main.py) into a Pyodide environment and run main.py.



Usage

Start the Game: Run python main.py to launch the game.
Gameplay:
Click a card in your hand (bottom) to play it if it matches the top card’s color or value.
If no cards are playable, click the Draw button.
For Wild cards, select a color from the buttons that appear.
The AI opponent plays automatically on its turn.


Winning: The first to discard all cards wins. A message (“You win!” or “AI wins!”) appears at the end.
UI Features:
Cards are centered with dynamic spacing to prevent overlap.
Text has a black background for readability against any card color.
Hover effects highlight playable cards and buttons.
A gradient background enhances visual appeal.



Project Structure
The project is modular, divided into separate files for clarity and reusability:
uno-card-game/
├── constants.py      # Game constants (card size, colors, etc.)
├── card.py           # Card class for card logic
├── game_logic.py     # Core game mechanics (deck, AI, actions)
├── ui.py             # UI rendering and input handling
├── main.py           # Main game loop
├── README.md         # This file

Key Components

constants.py: Defines shared constants like CARD_WIDTH, COLORS, and BUTTON_COLOR.
card.py: Implements the Card class with playability logic (can_play).
game_logic.py: Manages deck creation, AI heuristics, card dealing, and action handling (e.g., Skip, DrawTwo).
ui.py: Renders the game using Pygame, with centered hands, hover effects, and readable text.
main.py: Orchestrates the game by connecting logic and UI.

AI Approach
The AI opponent uses heuristic-based decision-making:

Scores each playable card based on:
Color match with current card: +5 points
Most common color in AI’s hand: +3 points
Action cards (Skip, Reverse, DrawTwo): +10 points
Wild cards: +8 points (+2 for WildDrawFour)


Selects the highest-scoring card or draws if no cards are playable.
For Wild cards, chooses the most common color in its hand to maximize future plays.

This approach is simple, efficient, and provides a challenging opponent, aligning with AI course objectives.


