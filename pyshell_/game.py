import os
import subprocess
from InquirerPy import inquirer


class Game:
    @staticmethod
    def play_game(args=None):
        # Always look for "game" folder inside this package
        base_dir = os.path.dirname(__file__)
        games_dir = os.path.join(base_dir, "game")

        # Check if folder exists
        if not os.path.exists(games_dir):
            print(f"❌ Games directory not found: {games_dir}")
            return

        # List available games (only subdirectories)
        games = [
            f for f in os.listdir(games_dir)
            if os.path.isdir(os.path.join(games_dir, f))
        ]

        if not games:
            print("No games found.")
            return

        # Let user select a game
        selected_game = inquirer.select(
            message="🎮 Select a game to play:",
            choices=games,
            default=games[0],
        ).execute()

        # Path to the selected game’s entrypoint
        game_path = os.path.join(games_dir, selected_game, "main.py")

        if os.path.isfile(game_path):
            print(f"\n🚀 Launching {selected_game}...\n")
            subprocess.run(["python", game_path])
        else:
            print(f"❌ No main.py found for {selected_game}.")
