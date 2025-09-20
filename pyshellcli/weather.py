# Weather Information

import requests, os
from rich.console import Console

class Weather:
    def get_weather(self, args):
        console = Console()
        if not args:
            console.print("Usage: weather <city>", style="bold red")
            return

        city = " ".join(args)
        api_key = os.getenv("API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] != 200:
                console.print(f"Error: {data['message']}", style="bold red")
                return

            weather_desc = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            console.print(f"\n[bold cyan]Weather in {city}:[/bold cyan]")
            console.print(f"🌤️  {weather_desc}")
            console.print(f"🌡️  Temperature: {temp}°C")
            console.print(f"💧 Humidity: {humidity} %")
            console.print(f"💨 Wind Speed: {wind_speed} m/s")

        except Exception as e:
            console.print(f"Failed to fetch weather data: {e}", style="bold red")