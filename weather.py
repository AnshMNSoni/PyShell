# Weather Information

import requests, os, time, msvcrt
from rich.console import Console
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import RadioList, Box, Frame
from prompt_toolkit.layout.containers import HSplit
from menu_base import MojiSwitchMenu

console = Console()

class Weather:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            console.print("Warning: OPENWEATHER_API_KEY not set", style="bold yellow")
    
    def get_weather(self, city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather_data = {
                    'temp': data['main']['temp'],
                    'wind': data['wind']['speed'],
                    'humidity': data['main']['humidity']
                }
                animate_weather_loading()
                animate_weather_display(weather_data)
            else:
                console.print(f"Error: {data['message']}", style="bold red")
        except Exception as e:
            console.print(f"Failed to fetch weather data: {e}", style="bold red")

def show_weather_menu():
    # Define options for weather operations
    options = [
        ("🌤️ Current Weather", "current"),
        ("📅 5-Day Forecast", "forecast"),
        ("🌡️ Temperature History", "history"),
        ("🌪️ Weather Alerts", "alerts"),
        ("📍 Change Location", "location"),
        ("📊 Weather Stats", "stats")
    ]
    
    def on_execute(state):
        # Get list of enabled operations
        enabled_ops = [name for name, value in options if state[value]]
        if not enabled_ops:
            console.print("[bold red]No operations selected![/bold red]")
            return
            
        # Animate weather loading
        animate_weather_loading()
        
        # Process each enabled operation
        results = {}
        for op in enabled_ops:
            # Simulate weather data fetch
            time.sleep(0.5)
            results[op] = f"Weather data for {op}"
            
        # Display results
        animate_weather_display(results)
    
    # Create and run menu
    menu = MojiSwitchMenu(
        title="🌤️ Weather Operations",
        options=options,
        on_execute=on_execute
    )
    menu.run()

def animate_weather_loading():
    """Animate weather data loading with a spinning effect"""
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    console.print("\n")
    for _ in range(20):  # 2 seconds of animation
        for char in spinner:
            console.print(f"\033[A\033[K[bold blue]{char} Fetching weather data...[/bold blue]")
            time.sleep(0.1)
    console.print("\n")

def animate_weather_display(weather_data):
    """Animate weather data display with a fade-in effect"""
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            for key, value in weather_data.items():
                console.print(f"[grey50]{key}: {value}[/grey50]")
        elif i == 1:
            for key, value in weather_data.items():
                console.print(f"[bold blue]{key}: {value}[/bold blue]")
        else:
            for key, value in weather_data.items():
                console.print(f"[bold green]{key}: {value}[/bold green]")
        time.sleep(0.2)
    console.print("\n")

def animate_forecast_loading():
    """Animate forecast loading with a progress bar effect"""
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Loading forecast: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n")

def animate_location_change():
    """Animate location change with a spinning effect"""
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    console.print("\n")
    for _ in range(10):  # 1 second of animation
        for char in spinner:
            console.print(f"\033[A\033[K[bold blue]{char} Updating location...[/bold blue]")
            time.sleep(0.1)
    console.print("\n")

def animate_forecast_display(forecast_data):
    """Animate forecast data display with a slide-in effect"""
    console.print("\n")
    for day in forecast_data:
        for i in range(3):
            console.print("\033[A\033[K", end="")
            if i == 0:
                console.print(f"[grey50]📅 {day['date']}[/grey50]")
                console.print(f"[grey50]🌡️ {day['temp']}°C[/grey50]")
                console.print(f"[grey50]🌤️ {day['condition']}[/grey50]")
            elif i == 1:
                console.print(f"[bold blue]📅 {day['date']}[/bold blue]")
                console.print(f"[bold blue]🌡️ {day['temp']}°C[/bold blue]")
                console.print(f"[bold blue]🌤️ {day['condition']}[/bold blue]")
            else:
                console.print(f"[bold green]📅 {day['date']}[/bold green]")
                console.print(f"[bold green]🌡️ {day['temp']}°C[/bold green]")
                console.print(f"[bold green]🌤️ {day['condition']}[/bold green]")
            time.sleep(0.2)
        console.print("\n")