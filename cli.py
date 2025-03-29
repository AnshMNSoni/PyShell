import os
import time
import platform
import psutil
import json
import shutil
import socket
import subprocess
import requests
import shlex
import pyperclip
import random
import string
import threading
import schedule
import time
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style

console = Console()
USER_FILE = "users.json"
lock = threading.Lock()

scheduled_jobs = {}
commands = {} 
scheduled_jobs = {}
stop_scheduler = False 

# Load users
def load_users():
    with lock:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                return json.load(file)
    return {}

def save_users(users):
    with lock:
        with open(USER_FILE, "w") as file:
            json.dump(users, file, indent=4)

def clipboard_copy(text):
    with lock:
        pyperclip.copy(text)
        console.print("Text copied to clipboard!", style="bold green")

def clipboard_paste():
    with lock:
        console.print(f"Clipboard Content: {pyperclip.paste()}", style="bold yellow")

# User Authentication
def register_user():
    users = load_users()
    username = Prompt.ask("Enter new username")
    role = Prompt.ask("Assign role (admin/user)", choices=["admin", "user"], default="user")
    if username in users:
        console.print("User already exists!", style="bold red")
        return register_user()
    password = Prompt.ask("Enter password", password=True)
    users[username] = {"password": password, "role": role}
    save_users(users)
    console.print("User registered successfully!", style="bold green")
    return username, role

def login_user():
    users = load_users()
    username = Prompt.ask("Enter username")
    password = Prompt.ask("Enter password", password=True)
    if username in users and users[username]["password"] == password:
        console.print("Login successful!", style="bold green")
        return username, users[username]["role"]
    else:
        console.print("Invalid credentials!", style="bold red")
        return login_user()

# File Operations with Synchronization
def rename_item(args):
    if len(args) < 2:
        console.print("Usage: rename <old_name> <new_name>", style="bold red")
        return
    old_name, new_name = args
    with lock:
        try:
            os.rename(old_name, new_name)
            console.print(f"'{old_name}' renamed to '{new_name}'", style="bold green")
        except FileNotFoundError:
            console.print("Item not found.", style="bold red")

def move_file(args):
    if len(args) < 2:
        console.print("Usage: move <source> <destination>", style="bold red")
        return
    src, dest = args
    with lock:
        try:
            shutil.move(src, dest)
            console.print(f"Moved '{src}' to '{dest}'", style="bold green")
        except Exception as e:
            console.print(str(e), style="bold red")

def copy_file(args):
    if len(args) < 2:
        console.print("Usage: copy <source> <destination>", style="bold red")
        return
    src, dest = args
    with lock:
        try:
            shutil.copy(src, dest)
            console.print(f"Copied '{src}' to '{dest}'", style="bold green")
        except Exception as e:
            console.print(str(e), style="bold red")

def list_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        console.print(f"{proc.info['pid']} - {proc.info['name']}")

def kill_process(args):
    if not args:
        console.print("Usage: kill <PID>", style="bold red")
        return
    try:
        psutil.Process(int(args[0])).terminate()
        console.print(f"Process {args[0]} terminated", style="bold red")
    except Exception as e:
        console.print(str(e), style="bold red")

def network_info():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        external_ip = requests.get("https://api64.ipify.org").text
        console.print(f"Local IP: {local_ip}")
        console.print(f"External IP: {external_ip}")
    except Exception as e:
        console.print(f"Network Error: {e}", style="bold red")

def generate_password():
    length = Prompt.ask("Enter password length (default 12)", default="12")
    try:
        length = int(length)
    except ValueError:
        console.print("Invalid input. Using default length (12)", style="bold red")
        length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    console.print(f"Generated Password: {password}", style="bold green")
    clipboard_copy(password)
    
# Commands
def list_files():
    console.print("\nFiles and Directories:", style="bold cyan")
    for item in os.listdir():
        console.print(f" - {item}")

def create_file(filename):
    with open(filename, 'w') as f:
        content = Prompt.ask("Enter content")
        f.write(content)
    console.print(f"File '{filename}' created.", style="bold green")

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        console.print(f"File '{filename}' deleted.", style="bold red")
    else:
        console.print("File not found.", style="bold yellow")

def system_info():
    console.print("\n[bold blue]System Info:[/bold blue]")
    console.print(f" CPU Usage: {psutil.cpu_percent()}%")
    console.print(f" RAM Usage: {psutil.virtual_memory().percent}%")

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    console.print(f"Folder '{folder_name}' created.", style="bold green")

def delete_folder(folder_name):
    if os.path.exists(folder_name):
        os.rmdir(folder_name)
        console.print(f"Folder '{folder_name}' deleted.", style="bold red")
    else:
        console.print("Folder not found or not empty.", style="bold yellow")

def change_directory(path):
    try:
        os.chdir(path)
        console.print(f"Changed directory to {os.getcwd()}", style="bold green")
    except Exception as e:
        console.print(str(e), style="bold red")

def text_editor(filename):
    if not os.path.exists(filename):
        console.print("File not found. Creating a new file.", style="bold yellow")
    with open(filename, 'a+') as f:
        console.print("Enter text (type 'exit' to save and exit):", style="bold cyan")
        while True:
            line = input()
            if line.lower() == 'exit':
                break
            f.write(line + '\n')
    console.print(f"File '{filename}' saved.", style="bold green")

# Built-in Calculator
def calculator(args):
    if not args:
        console.print("Usage: calc <expression>", style="bold red")
        return
    try:
        expression = " ".join(args)
        result = eval(expression)
        console.print(f"Result: {result}", style="bold green")
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")

# Weather Information
def get_weather(args):
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

# Task Scheduling
def execute_command(args):
    if not args:
        console.print("[bold red]No command entered![/bold red]")
        return

    command_name = args[0]
    command_args = args[1:]

    if command_name in commands:
        try:
            commands[command_name](*command_args)  # Execute predefined command
        except TypeError as e:
            console.print(f"[bold red]Error executing command '{command_name}': {e}[/bold red]")
    else:
        try:
            subprocess.run([command_name] + command_args, check=True, text=True)
        except FileNotFoundError:
            console.print(f"[bold red]Unknown command: {command_name}. Type 'help' for a list of commands.[/bold red]")
        except Exception as e:
            console.print(f"[bold red]Error executing command: {e}[/bold red]")

def schedule_task(args):
    if len(args) < 3:
        console.print("Usage: schedule <interval> <unit> <command>", style="bold red")
        console.print("Example: schedule 10 seconds say 'Hello'", style="bold yellow")
        return

    try:
        interval = int(args[0])
    except ValueError:
        console.print("[bold red]Invalid interval! Must be an integer.[/bold red]")
        return

    unit = args[1].lower()
    command = " ".join(args[2:])

    def run_scheduled_task():
        """Executes a scheduled command."""
        global stop_scheduler
        
        if stop_scheduler:
            console.print("[bold red]Task execution stopped.[/bold red]")
            return
    
        console.print(f"[bold green]Running scheduled task:[/bold green] {command}")
        cmd_parts = shlex.split(command)  # Correctly parse arguments with quotes
        execute_command(cmd_parts)

    if unit in ["seconds", "minutes", "hours"]:
        job = getattr(schedule.every(interval), unit).do(run_scheduled_task)
        job_id = len(scheduled_jobs) + 1
        scheduled_jobs[job_id] = job
        console.print(f"Task scheduled every {interval} {unit}. Task ID: {job_id}", style="bold cyan")
    else:
        console.print("[bold red]Invalid time unit! Use: seconds, minutes, or hours.[/bold red]")

def stop_running_tasks(*args):
    """Sets the stop flag to True to prevent new tasks from running."""
    global stop_scheduler
    stop_scheduler = True
    schedule.clear()
    console.print("[bold red]Stopping all scheduled tasks...[/bold red]")

# Background scheduler loop
def run_scheduler():
    """Continuously runs pending scheduled tasks in the background."""
    while True:
        schedule.run_pending()
        time.sleep(1)  # Adjust sleep time if needed


def list_scheduled_tasks(_):
    if not scheduled_jobs:
        console.print("No scheduled tasks.", style="bold yellow")
    else:
        console.print("Scheduled Tasks:", style="bold cyan")
        for job_id, job in scheduled_jobs.items():
            console.print(f"[{job_id}] {job}", style="bold green")

def remove_scheduled_task(args):
    if not args:
        console.print("Usage: unschedule <task_id>", style="bold red")
        return

    task_id = int(args[0])
    if task_id in scheduled_jobs:
        schedule.cancel_job(scheduled_jobs[task_id])
        del scheduled_jobs[task_id]
        console.print(f"Task {task_id} unscheduled.", style="bold yellow")
    else:
        console.print(f"No task found with ID {task_id}.", style="bold red")

# display prompt 
def display_prompt(username):
    hostname = platform.node()
    cwd = os.getcwd()
    time_str = datetime.now().strftime("%H:%M:%S")
    console.print(f"\n[bold cyan]👤 {username}@{hostname}[/bold cyan] [yellow]~ {cwd}[/yellow]  [bold magenta]{time_str}[/bold magenta]", end="\n❯ ", style=Style(color="bright_green"))

# clear console 
def clear(*args):
    console.print("="*70, style="bold blue")
    display_prompt(username)
    console.clear()

def main():
    console.clear()
    console.print("="*70, style="bold blue")
    console.print("Welcome to PyCLI", style="bold yellow", end=" ")
    console.print("{Python Command Line Interface by ansh.mn.soni}", style="magenta")
    console.print(f"System: {platform.system()} {platform.release()} ", style="bold cyan")
    console.print("="*70, style="bold blue")

    global username
    username, role = register_user() if Prompt.ask("New user?", choices=["y", "n"]) == "y" else login_user()

    commands = {
        "rename": rename_item,
        "move": move_file,
        "copy": copy_file,
        "processes": list_processes,
        "kill": kill_process,
        "network": network_info,
        "copytext": clipboard_copy,
        "paste": clipboard_paste,
        "password": generate_password,
        "calc": calculator,
        "weather": get_weather,
        "schedule": schedule_task,  
        "tasks": list_scheduled_tasks,  
        "unschedule": remove_scheduled_task,
        "stop": stop_running_tasks,
        "cls": clear,
        "exit": lambda _: exit()
    }
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    while True:
        display_prompt(username)
        command = input().strip().lower().split()
        
        if not command:
            continue
        
        cmd, *args = command
        
        start_time = time.time()
        
        if not command:
            continue
        
        cmd, *args = command
        start_time = time.time()
        
        if cmd in commands:
            commands[cmd](args)
        else:
            if cmd == "ls":
                list_files()
            elif cmd == "touch" and args:
                create_file(args[0])
            elif cmd == "rm" and args:
                delete_file(args[0])
            elif cmd == "mkdir" and args:
                create_folder(args[0])
            elif cmd == "rmdir" and args:
                delete_folder(args[0])
            elif cmd == "cd" and args:
                change_directory(args[0])
            elif cmd == "edit" and args:
                text_editor(args[0])
            elif cmd == "sysinfo":
                system_info()
            elif cmd == "exit":
                console.print("Exiting PyOS...", style="bold red")
                break
            else:
                console.print("Invalid command!", style="bold red")
        
        exec_time = time.time() - start_time
        console.print(f"Execution time: {exec_time:.4f} seconds", style="bold yellow")
        time.sleep(1)

if __name__ == "__main__":
    main()
