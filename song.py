import requests
import webbrowser
import sys
from rich.console import Console

console = Console()

class Song:
    @staticmethod
    def play_song(args):
        if not args:
            console.print("Usage: play <song-name>", style="bold red")
            return

        song_name = "".join(args)

        try:
            # Search for the song using saavn.dev API
            url = f"https://saavn.dev/api/search/songs?query={song_name}"
            response = requests.get(url)
            data = response.json()

            # Get first song result
            results = data['data']['results']
            if not results:
                raise Exception("No results found.")

            song = results[0]
            song_title = song['name']
            song_url = song['url']

            console.print(f"🎵 Opening in browser: {song_title}", style="bold green")
            webbrowser.open(song_url)

        except Exception as e:
            console.print(f"❌ Failed to find or play the song: {e}", style="bold red")