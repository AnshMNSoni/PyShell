import os
import time
import psutil
import socket
import subprocess
import platform
from datetime import datetime
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt
import config
import questionary
import itertools
from rich.color import Color
from rich.segment import Segment
from rich.style import Style
import threading
from rich.panel import Panel
from rich.table import Table
import msvcrt
from rich.live import Live
from menu_base import MojiSwitchMenu
from features import smart_suggestions, nl_to_code, error_explainer, snippet_search, code_refactor

console = Console()
prompt = None
prompt_flag = True

class Terminal:
    def set_prompt(self, value):
        global prompt
        prompt = value
    
    def get_prompt(self):
        global prompt
        return prompt

    def set_prompt_flag(self, value: bool):
        global prompt_flag
        prompt_flag = value
    
    def get_prompt_flag(self):
        global prompt_flag
        return prompt_flag

    def show_terminal_themes(self):
        # Define options for terminal themes
        options = [
            ("🌙 Solarized Night", "solarized"),
            ("💻 Hacker Green", "hacker"),
            ("🧩 Agnoster", "agnoster"),
            ("🟡 Marcduiker", "marcduiker"),
            ("🧼 Clean Detailed", "clean"),
            ("⚛️ Atomic-Lite", "atomic"),
            ("🐍 PyShell Default", "default"),
            ("🟦 Softline", "softline")
        ]
        
        def on_execute(state):
            # Find the selected theme
            selected = [i for i, (_, value) in enumerate(options, 1) if state[value]]
            if not selected:
                console.print("[bold red]No theme selected![/bold red]")
                return
            theme_index = selected[0]
            config.current_terminal_layout = theme_index
            # Call the corresponding terminal_X method
            getattr(self, f"terminal_{theme_index}")()
            console.clear()
            console.print(f"[bold green]Theme applied: {options[theme_index-1][0]}[/bold green]")
        
        # Create and run menu
        menu = MojiSwitchMenu(
            title="🎨 Terminal Themes",
            options=options,
            on_execute=on_execute
        )

        # --- SINGLE SELECTION LOGIC ---
        orig_handle_input = menu.handle_input
        def single_select_handle_input(choice):
            # Only one can be True at a time
            if choice in menu.key_map:
                for k in menu.state:
                    menu.state[k] = False
                menu.state[menu.key_map[choice]] = True
                return True
            return orig_handle_input(choice)
        menu.handle_input = single_select_handle_input
        menu.run()
        
    def display_terminal_table(self, themes):
        """Display terminal themes in a modern table format"""
        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=None,
            padding=(0, 1)
        )
        
        # Add columns
        table.add_column("No.", style="dim", width=4)
        table.add_column("Theme", style="bold")
        table.add_column("Description", style="italic")
        table.add_column("Status", justify="center", width=4)
        
        # Add rows with theme types
        features = [
            ("1", "Solarized Night", "Dark theme with solarized colors", "solarized"),
            ("2", "Hacker Green", "Classic terminal green on black", "hacker"),
            ("3", "Agnoster", "Powerline-inspired theme", "agnoster"),
            ("4", "Marcduiker", "Clean and minimal design", "marcduiker"),
            ("5", "Clean Detailed", "Detailed information display", "clean"),
            ("6", "Atomic-Lite", "Lightweight atomic design", "atomic"),
            ("7", "PyShell Default", "Default PyShell theme", "default"),
            ("8", "Softline", "Soft colors with line separators", "softline")
        ]
        
        for no, name, desc, key in features:
            status = "✅" if themes.get(key, False) else "❌"
            table.add_row(no, name, desc, status)
            
        # Create panel with table
        panel = Panel(
            table,
            title="🎨 Terminal Themes",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(panel)

    def animate_theme_change(self):
        """Animate theme change with a progress bar effect"""
        console.print("\n")
        for i in range(10):
            progress = "█" * i + "░" * (10 - i)
            console.print(f"\033[A\033[K[bold blue]Changing theme: [{progress}] {i*10}%[/bold blue]")
            time.sleep(0.2)
        console.print("\n")

    def animate_theme_display(self, themes):
        """Animate theme display with a fade-in effect"""
        console.print("\n")
        for i in range(3):
            console.print("\033[A\033[K", end="")
            if i == 0:
                for key, value in themes.items():
                    console.print(f"[grey50]{key}: {value}[/grey50]")
            elif i == 1:
                for key, value in themes.items():
                    console.print(f"[bold blue]{key}: {value}[/bold blue]")
            else:
                for key, value in themes.items():
                    console.print(f"[bold green]{key}: {value}[/bold green]")
            time.sleep(0.2)
        console.print("\n")

    def terminal_1(self):
        cwd = os.getcwd().split(os.sep)
        time_str = datetime.now().strftime("%H:%M")
        mem = psutil.virtual_memory()

        left = Text()
        left.append("\n ☾ ", style="white on dark_blue")
        left.append("Solar Night", style="bright_white on dark_blue")
        left.append(f"  {time_str} ", style="white on dark_blue")
        left.append(f" | 📁 {'/'.join(cwd[-2:])} ", style="cyan")

        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        right = Text()
        right.append("", style="black on blue")
        right.append(f"   {branch} ", style="black on blue")
        
        global prompt
        prompt = left + Text(" " * (console.width - len(left.plain) - len(right.plain))) + right
        self.set_prompt(prompt)
        return prompt
    

    def terminal_2(self):
        cwd = os.getcwd().split(os.sep)
        time_str = datetime.now().strftime("%H:%M")
        mem = psutil.virtual_memory()

        left = Text()
        left.append("\nHacker Mode", style="white on green")
        left.append(f" | ⏰ {time_str} | MEM: {mem.percent}% ", style="white on green")
        left.append(f" | 📁 {'/'.join(cwd[-2:])} ", style="bright_green")

        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        right = Text()
        right.append("", style="black on green")
        right.append(f"   {branch} ", style="black on green")
        
        global prompt
        prompt = left + Text(" " * (console.width - len(left.plain) - len(right.plain))) + right
        self.set_prompt(prompt)
        return prompt
    
    
    def terminal_3(self):
        # Extract current working directory
        cwd = os.getcwd().split(os.sep)
        hostname = platform.node()
        
        # Build left segment
        left = Text()
        left.append("\n", style="green")
        left.append("", style="black")
        left.append(f" {hostname} ", style="black on white")
        left.append("", style="white on black")

        # Build middle segment (folder path)
        for part in cwd:
            if part:
                left.append("", style="black on blue")
                left.append(f" {part} ", style="white on blue")
                left.append("", style="blue on black")

        # Build right segment (branch name)
        right = Text()
        right.append("", style="black on green")
            
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"
            
        right.append(f"  {branch} ", style="black on green")
        right.append("", style="green on black")

        # Combine everything
        global prompt
        prompt = left + right
        self.set_prompt(prompt)
        return prompt
    
    
    def terminal_4(self):
        # Get current folder
        folder = os.path.basename(os.getcwd())
        time_str = datetime.now().strftime("%H:%M")

        try:
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        try:
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            changes = len(status_output.splitlines())
        except subprocess.CalledProcessError:
            changes = 0

        # Left: folder name segment
        p = Text()
        p.append("\n", style="black on #FFD700")
        p.append(f" {folder} ", style="black on #FFD700")
        p.append("", style="#FFD700 on dark_orange")

        # Middle: branch and status
        p.append(f"  {branch} = ", style="black on dark_orange")
        p.append(f" {changes} ", style="black on dark_orange")

        # Right: bolt/power symbol
        p.append("", style="dark_orange on blue")
        p.append(f" {time_str} ", style="white on blue")
        p.append("", style="blue on black")

        global prompt
        prompt = p
        self.set_prompt(prompt)
        return prompt


    def terminal_5(self):
        folder = os.path.basename(os.getcwd())

        # Start timer
        start_time = time.time()

        # Git branch
        try:
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        # Git status
        try:
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            changes = len(status_output.splitlines())
        except subprocess.CalledProcessError:
            changes = 0

        # End timer
        end_time = time.time()
        exec_time_ms = int((end_time - start_time) * 1000)

        # Memory usage
        mem = psutil.virtual_memory()
        used_percent = mem.percent
        used = mem.used // (1024 ** 3)
        total = mem.total // (1024 ** 3)

        # Build left side of prompt
        left = Text()
        left.append("\n", style="white on #DCDCDC")
        left.append("  shell ", style="black on #DCDCDC")
        left.append("", style="#DCDCDC on black")
        left.append("", style="black on #4682B4")
        left.append(f" MEM: {used_percent:.2f}% ", style="white on #4682B4")
        left.append(f" {used}/{total}GB ", style="white on #4682B4")
        left.append("", style="#4682B4 on grey30")
        left.append(f" {exec_time_ms}ms ", style="white on grey30")
        left.append("", style="grey30 on black")
        left.append(f" → {folder} ", style="white on black")

        # Build right side of prompt
        right = Text()
        right.append("", style="bright_cyan on black")
        right.append(f"  {branch} = ", style="black on bright_cyan")
        right.append(f" {changes} ", style="black on bright_cyan")

        # Combine with spacing
        space = " " * max(console.width - len(left.plain) - len(right.plain), 1)
        
        global prompt
        prompt = left + Text(space) + right
        self.set_prompt(prompt)
        return prompt

    
    def terminal_6(self):
        start_time = time.time()

        # Current folder name
        folder = os.path.basename(os.getcwd())

        # Git info
        try:
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        try:
            status_output = subprocess.check_output(
                ["git", "status", "--porcelain"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            changes = len(status_output.splitlines())
        except subprocess.CalledProcessError:
            changes = 0

        end_time = time.time()
        exec_time = f"{int((end_time - start_time) * 1000)}ms"

        # Memory
        mem = psutil.virtual_memory()
        mem_used = mem.used / (1024 ** 3)
        mem_total = mem.total / (1024 ** 3)
        mem_percent = mem.percent

        # Host and Time
        hostname = socket.gethostname().split(".")[0]
        now = datetime.now().strftime("%a, %H:%M")

        left = Text()
        left.append("\n", style="black on blue")
        left.append(" shell ", style="white on blue")
        left.append("", style="blue on black")
        left.append("", style="black on dark_orange")
        left.append("  ", style="black on dark_orange")
        left.append(f"{folder} ", style="black on dark_orange")
        left.append("", style="dark_orange on black")
        left.append("", style="black on yellow")
        left.append(f" {branch} =  {changes} ", style="black on yellow")
        left.append("", style="yellow on black")
        left.append("", style="black on grey70")
        left.append(f" {exec_time} ", style="black on grey70")
        left.append("", style="grey70 on black")

        right = Text()
        right.append("", style="green on black")
        right.append(f" 󰾆  {mem_percent:.1f}% ", style="green on black")
        right.append("", style="blue on black")
        right.append(f" {hostname} ", style="white on blue")
        right.append("", style="black on blue")
        right.append("", style="grey70 on black")
        right.append(f"  {now} ", style="black on grey70")

        spacing = " " * max(console.width - len(left.plain) - len(right.plain), 1)
        
        global prompt
        prompt = left + Text(spacing) + right
        self.set_prompt(prompt)
        return prompt

    
    def terminal_7(self):
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
        
        global prompt
        prompt = left_prompt + Text(" " * (console.width - len(left_prompt.plain) - len(right_prompt.plain))) + right_prompt
        self.set_prompt(prompt)
        return prompt
    
    
    def terminal_8(self):
        start_time = time.time()

        # Gather information
        user = os.getenv("USER") or os.getenv("USERNAME") or "user"
        hostname = socket.gethostname().split('.')[0]
        folder = os.getcwd().split(os.sep)[-1]

        # Git branch info
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = ""

        end_time = time.time()
        exec_time = f"{int((end_time - start_time) * 1000)}ms"
        current_time = datetime.now().strftime("%d/%m/%y %H:%M")

        # LEFT prompt
        left = Text()
        left.append("\n", style="grey37")
        left.append(" shell ", style="black on grey37")
        left.append("\uE0B4", style="grey37")
        left.append("", style="grey85")
        left.append(f"  {user}@{hostname} ", style="black on grey85")
        left.append("\uE0B4", style="grey85")
        if branch:
            left.append("", style="khaki1")
            left.append(f"  {branch} ", style="black on khaki1")
            left.append("\uE0B4", style="khaki1")

        # Add directory
        full_path = os.getcwd()
        folders = full_path.split(os.sep)
        folder_path = " » ".join(folders[-2:])  # Show last 2 folders
        left.append(f"\n[   {folder_path} ]", style="white")

        # RIGHT prompt
        right = Text()
        right.append(f"{exec_time}  -  {current_time}", style="bold palegreen3")

        # Final combined prompt
        spacing = " " * max(console.width - len(left.plain.splitlines()[-1]) - len(right.plain), 1)
        
        global prompt
        prompt = left + Text(spacing) + right
        self.set_prompt(prompt)
        return prompt

    def change_terminal(self, *args):
        global prompt_flag
        prompt_flag = False

        self.set_prompt_flag(False)  # Update the flag globally

        # Use the new MojiSwitchMenu-based theme selector
        self.show_terminal_themes()
        # After theme selection, update config if needed
        # (You may want to add logic here to update config.current_terminal_layout)
        console.clear()
        console.print(f"Terminal theme selection complete!", style="bold green")
        # Optionally, update the prompt to reflect the new theme
        # self.terminal_1() or similar, based on user selection

        