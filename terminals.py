import os
import psutil
import subprocess
from datetime import datetime
from rich.text import Text
from rich.console import Console
from rich.prompt import Prompt

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

    def terminal_1(self):
        cwd = os.getcwd().split(os.sep)
        time_str = datetime.now().strftime("%H:%M")
        mem = psutil.virtual_memory()

        left = Text()
        left.append(" ☾ ", style="white on dark_blue")
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
        left.append(" 👨‍💻 ", style="black on green")
        left.append("Hacker Mode", style="white on green")
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
        cwd = os.getcwd().split(os.sep)
        time_str = datetime.now().strftime("%H:%M")

        left = Text()
        left.append(" 🪐 ", style="white on magenta")
        left.append("Galactic", style="white on magenta")
        left.append(f" | 🕓 {time_str} ", style="white on magenta")
        left.append(f" | 📂 {'/'.join(cwd[-2:])} ", style="magenta")

        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            branch = "no-branch"

        right = Text()
        right.append("", style="black on magenta")
        right.append(f"   {branch} ", style="black on magenta")
        
        global prompt
        prompt = left + Text(" " * (console.width - len(left.plain) - len(right.plain))) + right
        self.set_prompt(prompt)
        return prompt

    def change_terminal(self, *args):
        global prompt_flag
        prompt_flag = False
        self.set_prompt_flag(False)  # Update the flag globally
        console.print("\nChoose Terminal Layout:", style="bold blue")
        console.print("[1] Solarized Night 🌙")
        console.print("[2] Hacker Green 💻")
        console.print("[3] Galactic Magenta 🪐")
        choice = Prompt.ask("Enter layout number", choices=["1", "2", "3"], default="1")
    
        current_terminal = int(choice)
        console.clear()
        console.print(f"Terminal switched to layout {choice}!", style="bold green")
    
        if current_terminal == 1:
            self.terminal_1()
        elif current_terminal == 2:
            self.terminal_2()
        elif current_terminal == 3:
            self.terminal_3()
            