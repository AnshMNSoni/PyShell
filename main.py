import os, time, psutil, json, pyperclip, random, string, threading, time, pyfiglet, config
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from ai_panel import show_ai_panel, is_feature_enabled
from prompt_toolkit.key_binding import KeyBindings
from rich.live import Live
from rich.table import Table
import msvcrt
from prompt_toolkit.formatted_text import HTML
from features.smart_suggestions import get_live_suggestion

# dependencies
from weather import Weather
from tasks import Task
from linux_commands import Commands
from git_commands import Git
from terminals import Terminal
from song import Song
from equations import Equations
from game import Game
from statistics_menu import show_statistics_menu
from graphs import GraphPlotter

console = Console()
USER_FILE = "users.json"
lock = threading.Lock()
scheduled_jobs = {}
commands = {} 
stop_scheduler = False
prompt_flag = True

# Animated ASCII Art for PyShell
ASCII_ART = [
    " ____        ____  _          _ _ ",
    "|  _ \\ _   _/ ___|| |__   ___| | |",
    "| |_) | | | \\___ \\| '_ \\ / _ \\ | |",
    "|  __/| |_| |___) | | | |  __/ | |",
    "|_|    \\__, |____/|_| |_|\\___|_|_|",
    "       |___/"
]

COLOR_WAVE = [
    "deep_pink3", "hot_pink", "magenta", "purple", 
    "blue_violet", "royal_blue1", "cyan", "turquoise2",
    "spring_green3", "lime", "yellow", "orange1",
    "red", "dark_red", "deep_pink2", "medium_purple"
]

WELCOME_ASCII = [
    " __        __   _                            ",
    " \\ \\      / /__| | ___ ___  _ __ ___   ___   ",
    "  \\ \\ /\\ / / _ \\ |/ __/ _ \\| '_ ` _ \\ / _ \\  ",
    "   \\ V  V /  __/ | (_| (_) | | | | | |  __/  ",
    "    \\_/\\_/ \\___|_|\\___\\___/|_| |_| |_|\\___|  "
]

def animate_welcome_zoom_out():
    max_padding = 12
    welcome_colors = ["deep_pink3", "hot_pink", "magenta", "purple", "blue_violet"]
    for pad in range(max_padding, -1, -2):  # 7 frames
        console.clear()
        for i, line in enumerate(WELCOME_ASCII):
            color = welcome_colors[i % len(welcome_colors)]
            console.print(" " * pad + f"[bold {color}]{line}[/bold {color}]", justify="left")
        time.sleep(0.05)
    console.clear()

def animate_welcome_ascii_reveal():
    welcome_colors = ["deep_pink3", "hot_pink", "magenta", "purple", "blue_violet"]
    for col in range(1, len(WELCOME_ASCII[0]) + 1):
        console.clear()
        for i, line in enumerate(WELCOME_ASCII):
            # Reveal up to the current column, mask the rest
            revealed = line[:col]
            masked = line[col:]
            color = welcome_colors[i % len(welcome_colors)]
            console.print(f"[bold {color}]{revealed}[/bold {color}][grey23]{masked}[/grey23]", justify='left')
        time.sleep(0.07)
    time.sleep(0.5)
    console.clear()

def animate_ascii_art_wave():
    animate_welcome_zoom_out()
    for frame in range(7):  # 7 frames
        console.clear()
        for idx, line in enumerate(ASCII_ART):
            wave_offset = (frame + idx) % len(COLOR_WAVE)
            styled_line = Text()
            for i, char in enumerate(line):
                color = COLOR_WAVE[(wave_offset + i) % len(COLOR_WAVE)]
                styled_line.append(char, style=color)
            console.print(styled_line)
        time.sleep(0.07)
    console.clear()
    # Final static display with gradient effect
    final_colors = ["deep_pink3", "hot_pink", "magenta", "purple", "blue_violet", "royal_blue1"]
    for i, line in enumerate(ASCII_ART):
        color = final_colors[i % len(final_colors)]
        console.print(Text(line, style=f"bold {color}"))

def show_command_feedback(cmd):
    table = Table.grid(padding=(0, 1))
    table.add_column("Status", style="cyan")
    table.add_column("Command", style="green")
    table.add_row("", cmd)
    with Live(table, refresh_per_second=10):
        time.sleep(0.1)  # Brief pause for visual feedback

def show_smart_suggestion():
    suggestions = [
        "Try 'git status' to check repository state",
        "Use 'weather' to get local forecast",
        "Run 'stats' for statistical calculations",
        "Type '~ai' to configure AI features"
    ]
    suggestion = random.choice(suggestions)
    console.print(f"\n[bold green]💡 {suggestion}[/bold green]")

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
        return
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    console.print(f"Generated Password: {password}", style="bold green")
    clipboard_copy(password)


# changing and displaying terminal 
terminal = Terminal()

def display_prompt(username):
    if config.current_terminal_layout == 1:  
        Terminal().terminal_1()
    elif config.current_terminal_layout == 2:
        Terminal().terminal_2()
    elif config.current_terminal_layout == 3:
        Terminal().terminal_3()
    elif config.current_terminal_layout == 4:
        Terminal().terminal_4()
    elif config.current_terminal_layout == 5:
        Terminal().terminal_5()
    elif config.current_terminal_layout == 6:
        Terminal().terminal_6()
    elif config.current_terminal_layout == 7:
        Terminal().terminal_7()
    elif config.current_terminal_layout == 8:
        Terminal().terminal_8()
        
    prompt = terminal.get_prompt()
    console.print(f"{prompt}", justify="left")
       
    
# clear console 
def clear(*args):
    os.system('cls' if os.name == 'nt' else 'clear')

def show_suggestions():
    suggestions = """
# Welcome to PyShell!

Here are some things you can try:

• File: rename, move, copy, delete, create, list, edit, cd  
• Processes: list, kill  
• Network: info  
• Clipboard: copy, paste  
• Password: generate  
• Math: calculator, math-help, equation, differential, stats  
• Weather: get weather  
• Tasks: schedule, list, unschedule, stop  
• Terminal: change style  
• Games: play games  
• Graphs: plot  
• Git: status, branches, create, switch, delete, merge, clone, add, commit, push, pull, stash, undo, recover, dashboard, auto_merge, voice, reminder, offline_sync, history, help  
• Music: play a song  
• Other: clear, exit  
"""
    panel = Panel.fit(Markdown(suggestions), title="💡 Suggestions", border_style="yellow", padding=(1, 2))
    console.print(panel)

def show_menu():
    menu_items = [
        ("1", "📊 Statistics", "Calculate statistics and generate plots"),
        ("2", "🌤️ Weather", "Get weather information"),
        ("3", "📝 Tasks", "Manage your tasks"),
        ("4", "🔧 Terminal", "Customize terminal appearance"),
        ("5", "🤖 AI Panel", "Configure AI features"),
        ("6", "📈 Graph", "Create and visualize graphs"),
        ("7", "🧮 Equations", "Solve mathematical equations"),
        ("8", "📂 Git", "Git repository management"),
        ("9", "⚙️ Settings", "Configure PyShell settings"),
        ("0", "❌ Exit", "Exit PyShell")
    ]
    
    selected_index = 0
    
    # Animate header
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            console.print("[bold cyan]╔════════════════════════════════════╗[/bold cyan]")
        elif i == 1:
            console.print("[bold cyan]║           PyShell Menu            ║[/bold cyan]")
        else:
            console.print("[bold cyan]╚════════════════════════════════════╝[/bold cyan]")
        time.sleep(0.05)
    
    # Print initial menu with fade-in effect
    for i, (no, name, desc) in enumerate(menu_items):
        if i == selected_index:
            console.print(f"[bold green]▶ {name}[/bold green]")
        else:
            console.print(f"  {name}")
        time.sleep(0.02)  # Fade-in effect
    
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            
            # Arrow key handling
            if key == b'\xe0':  # Arrow key prefix
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    # Move up one line
                    console.print("\033[A", end="")
                    # Clear current line
                    console.print("\033[K", end="")
                    # Print previous item without arrow
                    console.print(f"  {menu_items[selected_index][1]}")
                    # Move up one more line
                    console.print("\033[A", end="")
                    # Clear current line
                    console.print("\033[K", end="")
                    # Update selection
                    selected_index = (selected_index - 1) % len(menu_items)
                    # Print new selection with arrow and glow effect
                    console.print(f"[bold green]▶ {menu_items[selected_index][1]}[/bold green]")
                elif key == b'P':  # Down arrow
                    # Move down one line
                    console.print("\033[B", end="")
                    # Clear current line
                    console.print("\033[K", end="")
                    # Print next item without arrow
                    console.print(f"  {menu_items[selected_index][1]}")
                    # Move up one line
                    console.print("\033[A", end="")
                    # Clear current line
                    console.print("\033[K", end="")
                    # Update selection
                    selected_index = (selected_index + 1) % len(menu_items)
                    # Print new selection with arrow and glow effect
                    console.print(f"[bold green]▶ {menu_items[selected_index][1]}[/bold green]")
            
            # Enter key to select
            elif key == b'\r':
                # Animate selection
                for _ in range(3):
                    console.print(f"\033[A\033[K[bold green]▶ {menu_items[selected_index][1]}[/bold green]")
                    time.sleep(0.1)
                    console.print(f"\033[A\033[K  {menu_items[selected_index][1]}")
                    time.sleep(0.1)
                # Call the correct function for each menu item
                if menu_items[selected_index][0] == "4":
                    terminal.show_terminal_themes()
                    continue
                return menu_items[selected_index][0]
            
            # Escape key to exit
            elif key == b'\x1b':
                return "0"  # Exit option

def show_help(commands_dict):
    """Displays a list of all available commands."""
    console.print("\n[bold cyan]Available Commands:[/bold cyan]")
    for command in sorted(commands_dict.keys()):
        console.print(f"- {command}")
    console.print("\nType `~ai` to access AI features.")

def main():
    console.clear()
    animate_ascii_art_wave()
    global username
    username, role = register_user() if Prompt.ask("New user?", choices=["y", "n"]) == "y" else login_user()
    
    # Objects
    cmds = Commands()
    task = Task()
    weather = Weather()
    terminl = Terminal()
    git = Git()
    eq = Equations()
    graph = GraphPlotter()
    
    # AI Feature command stubs are removed from the 'commands' dictionary.
    # The '~ai' command is the single entry point.
    
    commands = {
        "rename": cmds.rename_item,
        "move": cmds.move_file,
        "copy": cmds.copy_file,
        "processes": list_processes,
        "kill": kill_process,
        "network": cmds.network_info,
        "copytext": clipboard_copy,
        "paste": clipboard_paste,
        "password": generate_password,
        "calc": cmds.calculator,
        "stats": lambda args: show_statistics_menu(),
        "equation": eq.solve_equation,
        "differential": lambda args: eq.solve_differential(args),
        "math-help": cmds.math_help,
        "weather": weather.get_weather,
        "schedule": task.schedule_task,  
        "tasks": task.list_scheduled_tasks,  
        "unschedule": task.remove_scheduled_task,
        "stop": task.stop_running_tasks,
        "cls": clear,
        "terminal": lambda args: terminl.show_terminal_themes(),
        "games": lambda *args: console.print('Game feature not implemented.'),
        "plot": lambda args: graph.run(),
        "help": lambda *args: show_help(commands),
        "exit": lambda _: exit(),
    }
    
    scheduler_thread = threading.Thread(target=Task().run_scheduler, daemon=True)
    scheduler_thread.start()
    
    show_suggestions()
    
    # Define required arguments for each command
    command_args = {
        "rename": ["<old_name>", "<new_name>"],
        "move": ["<source>", "<destination>"],
        "copy": ["<source>", "<destination>"],
        "kill": ["<PID>"],
        "copytext": ["<text>"],
        "equation": ["<equation>"],
        "differential": ["<equation>"],
        "weather": ["<location>"],
        "schedule": ["<task_name>", "<time>"],
        "unschedule": ["<task_name>"],
        "git-create": ["<branch_name>"],
        "git-switch": ["<branch_name>"],
        "git-merge": ["<branch_name>"],
        "git-delete": ["<branch_name>"],
        "git-clone": ["<repository_url>"],
        "git-add": ["<file>"],
        "git-commit": ["<message>"],
        "play": ["<song_name>"]
    }

    class CommandCompleter(Completer):
        def get_completions(self, document, complete_event):
            text = document.text_before_cursor
            words = text.split()
            if len(words) == 1:
                for cmd in commands.keys():
                    if cmd.startswith(words[0]):
                        yield Completion(cmd, start_position=-len(words[0]))
            elif len(words) == 2 and words[0] in command_args:
                for arg in command_args[words[0]]:
                    if arg.startswith(words[1]):
                        yield Completion(arg, start_position=-len(words[1]))

    def get_bottom_toolbar():
        if is_feature_enabled("smart_suggestions"):
            # This function is called on every render, making the suggestion live
            return HTML(get_live_suggestion(session.default_buffer.text, commands, command_args))
        return None

    session = PromptSession(
        completer=CommandCompleter(),
        bottom_toolbar=get_bottom_toolbar,
        refresh_interval=0.5  # Refresh toolbar every 0.5 seconds
    )
    
    while True:
        display_prompt(username)
        try:
            user_input = session.prompt("").strip().lower()
            if not user_input:
                continue
            command = user_input.split()
            cmd, *args = command
            start_time = time.time()

            # Show command feedback
            show_command_feedback(cmd)
            
            if cmd == "~ai":
                show_ai_panel()
                continue
            if cmd in commands:
                commands[cmd](args)
            else:
                if cmd == "ls":
                    cmds.list_files()
                elif cmd == "touch" and args:
                    cmds.create_file(args[0])
                elif cmd == "rm" and args:
                    cmds.delete_file(args[0])
                elif cmd == "mkdir" and args:
                    cmds.create_folder(args[0])
                elif cmd == "rmdir" and args:
                    cmds.delete_folder(args[0])
                elif cmd == "cd" and args:
                    cmds.change_directory(args[0])
                elif cmd == "edit" and args:
                    cmds.text_editor(args[0])
                elif cmd == "sysinfo":
                    cmds.system_info()
                elif cmd == "exit":
                    console.print("Exiting PyShell...", style="bold red")
                    break
                else:
                    console.print("Invalid command!", style="bold red")
            exec_time = time.time() - start_time
            console.print(f"Execution time: {exec_time:.4f} seconds", style="bold yellow")
                
            # Show smart suggestion occasionally
            if random.random() < 0.3:  # 30% chance
                show_smart_suggestion()
                
            time.sleep(1)
        except KeyboardInterrupt:
            console.print("\nUse 'exit' to quit", style="bold yellow")
        except Exception as e:
            console.print(f"Error: {str(e)}", style="bold red")

if __name__ == "__main__":
    main()
