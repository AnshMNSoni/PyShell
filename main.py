import os
import time
import platform
import psutil
import json
import pyperclip
import random
import string
import threading
import time
import subprocess
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

# dependencies
from weather import Weather
from task import Task
from linux_commands import Commands
from git_commands import Git
from terminals import Terminal
from song import Song
import config

console = Console()
USER_FILE = "users.json"
lock = threading.Lock()

scheduled_jobs = {}
commands = {} 
stop_scheduler = False
prompt_flag = True

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

# Synchronization
def list_processes(*args):
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

def generate_password(*args):
    length = Prompt.ask("Enter password length (default 12)", default="12")
    try:
        length = int(length)
    except ValueError:
        console.print("Invalid input. Using default length (12)", style="bold red")
        length = 12
        display_prompt(username)
        return
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    console.print(f"Generated Password: {password}", style="bold green")
    clipboard_copy(password)


# changing and displaying terminal 
terminal = Terminal()

def display_prompt(username):
    if terminal.get_prompt_flag(): 
        hostname = platform.node()
        cwd = os.getcwd().split(os.sep)
        time_str = datetime.now().strftime("%H:%M")

        mem = psutil.virtual_memory()
        mem_percent = mem.percent
        mem_total_gb = round(mem.total / (1024 ** 3))
        mem_used_gb = round(mem.used / (1024 ** 3))

        left_prompt = Text()
        left_prompt.append("\n # ", style="black on white")
        left_prompt.append(" shell ", style="white on blue")
        left_prompt.append("", style="blue on black")
        left_prompt.append("", style="black on blue")
        left_prompt.append(f" MEM: {mem_percent}% ↑ {mem_used_gb}/{mem_total_gb}GB ", style="white on blue")
        left_prompt.append("", style="blue on grey15")
        left_prompt.append(" code ", style="white on grey15")
        left_prompt.append("", style="grey15 on black")
        left_prompt.append(f" {time_str} ", style="white on black")
        left_prompt.append("", style="black")

        for part in cwd:
            if part:
                left_prompt.append(" // ", style="white")
                left_prompt.append("📁", style="white")
                left_prompt.append(f" {part} ", style="white")

        right_prompt = Text()
        right_prompt.append("", style="black on medium_sea_green")
        right_prompt.append("   ", style="black on medium_sea_green")

        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        right_prompt.append(f" {branch} ≡ ⎔ ~1 ", style="black on medium_sea_green")

        console.print(left_prompt + Text(" " * (console.width - len(left_prompt.plain) - len(right_prompt.plain))) + right_prompt)
    else:
        if config.current_terminal_layout == 3:  # use a global or config flag for current layout
            Terminal().terminal_3()
        console.print(terminal.get_prompt())  # Use prompt returned from Terminal
       
    
# clear console 
def clear(*args):
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    console.clear()
    console.print("="*70, style="bold blue")
    console.print("Welcome to PyShell", style="bold yellow", end=" ")
    console.print("{Python CLI by @ansh.mn.soni}", style="white")
    console.print(f"System: {platform.system()} {platform.release()} ", style="bold cyan")
    console.print("="*70, style="bold blue")

    global username
    username, role = register_user() if Prompt.ask("New user?", choices=["y", "n"]) == "y" else login_user()

    commands = {
        "rename": Commands().rename_item,
        "move": Commands().move_file,
        "copy": Commands().copy_file,
        "processes": list_processes,
        "kill": kill_process,
        "network": Commands().network_info,
        "copytext": clipboard_copy,
        "paste": clipboard_paste,
        "password": generate_password,
        "calc": Commands().calculator,
        "math-help": Commands().math_help,
        "weather": Weather().get_weather,
        "schedule": Task().schedule_task,  
        "tasks": Task().list_scheduled_tasks,  
        "unschedule": Task().remove_scheduled_task,
        "stop": Task().stop_running_tasks,
        "cls": clear,
        "terminal": Terminal().change_terminal,
        "exit": lambda _: exit(),
        
        # Git Commands (Using Git Class)
        "git-status": Git().git_status,
        "git-branches": Git().git_branches,
        "git-create": Git().git_create_branch,
        "git-switch": Git().git_switch_branch,
        "git-push": Git().git_push,
        "git-pull": Git().git_pull,
        "git-merge": Git().git_merge,
        "git-delete": Git().git_delete_branch,
        "git-clone": Git().git_clone,
        "git-add": Git().git_add,
        "git-commit": Git().git_commit,
        
        # Unique Git Features
        "play": lambda args: Song.play_song(" ".join(args)),
        "git-smart": Git().git_smart_commit,
        "git-help": Git().git_help,
        "git-history": Git().git_history,
        "git-undo": Git().git_undo,
        "git-stash": Git().git_stash,
        "git-recover": Git().git_recover,
        "git-dashboard": Git().git_dashboard,
        "git-auto_merge": Git().git_auto_merge,
        "git-voice": Git().git_voice_command,
        "git-reminder": Git().git_reminder,
        "git-offline_sync": Git().git_offline_sync
    }
    
    scheduler_thread = threading.Thread(target=Task().run_scheduler, daemon=True)
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
                Commands().list_files()
            elif cmd == "touch" and args:
                Commands().create_file(args[0])
            elif cmd == "rm" and args:
                Commands().delete_file(args[0])
            elif cmd == "mkdir" and args:
                Commands().create_folder(args[0])
            elif cmd == "rmdir" and args:
                Commands().delete_folder(args[0])
            elif cmd == "cd" and args:
                Commands().change_directory(args[0])
            elif cmd == "edit" and args:
                Commands().text_editor(args[0])
            elif cmd == "sysinfo":
                Commands().system_info()
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
