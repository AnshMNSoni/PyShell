# Basic Linux Commands

from rich.console import Console
from rich.prompt import Prompt
import os, psutil, shutil, threading, socket, requests

console = Console()
lock = threading.Lock()

class Commands:
    # Commands
    def list_files(self, ):
        console.print("\nFiles and Directories:", style="bold cyan")
        for item in os.listdir():
            console.print(f" - {item}")

    def create_file(self, filename):
        with open(filename, 'w') as f:
            content = Prompt.ask("Enter content")
            f.write(content)
        console.print(f"File '{filename}' created.", style="bold green")

    def delete_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
            console.print(f"File '{filename}' deleted.", style="bold red")
        else:
            console.print("File not found.", style="bold yellow")

    def system_info(self, ):
        console.print("\n[bold blue]System Info:[/bold blue]")
        console.print(f" CPU Usage: {psutil.cpu_percent()}%")
        console.print(f" RAM Usage: {psutil.virtual_memory().percent}%")
        
    def network_info(self, *args):
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            external_ip = requests.get("https://api64.ipify.org").text
            console.print(f"Local IP: {local_ip}")
            console.print(f"External IP: {external_ip}")
        except Exception as e:
            console.print(f"Network Error: {e}", style="bold red")

    def create_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)
        console.print(f"Folder '{folder_name}' created.", style="bold green")

    def delete_folder(self, folder_name):
        if os.path.exists(folder_name):
            os.rmdir(folder_name)
            console.print(f"Folder '{folder_name}' deleted.", style="bold red")
        else:
            console.print("Folder not found or not empty.", style="bold yellow")

    def change_directory(self, path):
        try:
            os.chdir(path)
            console.print(f"Changed directory to {os.getcwd()}", style="bold green")
        except Exception as e:
            console.print(str(e), style="bold red")

    def text_editor(self, filename):
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
        
    def rename_item(self, args):
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

    def move_file(self, args):
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
                
    # Built-in Calculator
    def calculator(self, args):
        if not args:
            console.print("Usage: calc <expression>", style="bold red")
            return
        try:
            expression = " ".join(args)
            result = eval(expression)
            console.print(f"Result: {result}", style="bold green")
        except Exception as e:
            console.print(f"Error: {e}", style="bold red")
            