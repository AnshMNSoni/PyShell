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
        pass
    
    
    def terminal_9(self):
        pass
    
    
    def terminal_10(self):
        pass


    def change_terminal(self, *args):
        global prompt_flag
        prompt_flag = False
        
        self.set_prompt_flag(False)  # Update the flag globally
        console.print("\nChoose Terminal Layout:", style="bold blue")
        console.print("[1] Solarized Night")
        console.print("[2] Hacker Green")
        console.print("[3] Agnoster")
        console.print("[4] Marcduiker")
        console.print("[5] Clean Detailed")
        console.print("[6] ")
        console.print("[7] PyShell Default")
        console.print("[8] ")
        console.print("[9] ")
        console.print("[10] ")
        choice = Prompt.ask("Enter layout number", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], default="1")
    
        current_terminal = int(choice)
        config.current_terminal_layout = current_terminal
        console.clear()
        console.print(f"Terminal switched to layout {choice}!", style="bold green")
    
        if current_terminal == 1:
            self.terminal_1()
        elif current_terminal == 2:
            self.terminal_2()
        elif current_terminal == 3:
            self.terminal_3()
        elif current_terminal == 4:
            self.terminal_4()
        elif current_terminal == 5:
            self.terminal_5()
        elif current_terminal == 6:
            self.terminal_6()
        elif current_terminal == 7:
            self.terminal_7()
        elif current_terminal == 8:
            self.terminal_8()
        elif current_terminal == 9:
            self.terminal_9()
        elif current_terminal == 10:
            self.terminal_10()
        