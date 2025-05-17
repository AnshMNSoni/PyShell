import os
import subprocess
from InquirerPy import inquirer

class Game:
    def play_game(args=None):
        games_dir = "game"
        games = [f for f in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, f))]
    
        if not games:
            print("No games found.")
            return
    
        selected_game = inquirer.select(
            message="🎮 Select a game to play:",
            choices=games,
            default=games[0],
        ).execute()
    
        game_path = os.path.join(games_dir, selected_game, "main.py")
    
        if os.path.isfile(game_path):
            print(f"\n🚀 Launching {selected_game}...\n")
            subprocess.run(["python", game_path])
        else:
            print(f"❌ No main.py found for {selected_game}.")
