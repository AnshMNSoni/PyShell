# Basic Linux Commands

from rich.console import Console
from rich.prompt import Prompt
import os, psutil, shutil, math, threading, socket, requests
from sympy import symbols, sympify, diff, integrate, pretty

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
    def math_help(self, *args):
        """Displays available mathematical functions and their usage."""
        help_text = """
        Available Mathematical Functions:
        
        - abs(x)           : Returns the absolute value of x
        - ceil(x)          : Returns the ceiling of x (smallest integer >= x)
        - floor(x)         : Returns the floor of x (largest integer <= x)
        - trunc(x)         : Truncates x (removes the decimal part)
        - exp(x)           : Returns e^x (exponential function)
        - log(x)           : Returns the natural logarithm of x (base e)
        - log(x, base)     : Returns the logarithm of x with specified base
        - log10(x)         : Returns the base-10 logarithm of x
        - log2(x)          : Returns the base-2 logarithm of x
        - sqrt(x)          : Returns the square root of x
        - pow(x, y)        : Returns x raised to the power y (x^y)
        - sin(x)           : Returns the sine of x (x in radians)
        - cos(x)           : Returns the cosine of x (x in radians)
        - tan(x)           : Returns the tangent of x (x in radians)
        - asin(x)          : Returns the inverse sine of x (result in radians)
        - acos(x)          : Returns the inverse cosine of x (result in radians)
        - atan(x)          : Returns the inverse tangent of x (result in radians)
        - sinh(x)          : Returns the hyperbolic sine of x
        - cosh(x)          : Returns the hyperbolic cosine of x
        - tanh(x)          : Returns the hyperbolic tangent of x
        - degrees(x)       : Converts radians to degrees
        - radians(x)       : Converts degrees to radians
        - gcd(x, y)        : Returns the greatest common divisor of x and y
        - lcm(x, y)        : Returns the least common multiple of x and y (Python 3.9+)
        - factorial(x)     : Returns x! (factorial of x)
        - isfinite(x)      : Returns True if x is neither infinity nor NaN
        - isinf(x)         : Returns True if x is infinity
        - isnan(x)         : Returns True if x is NaN (Not a Number)
        - copysign(x, y)   : Returns x with the sign of y
        - fmod(x, y)       : Returns remainder of x / y
        
        Example Usage:
        
        - calc sin(3.14)         # Returns sine of 3.14 radians
        - calc log(10)           # Returns natural log of 10
        - calc sqrt(25)          # Returns 5.0
        - calc pow(2, 3)         # Returns 2^3 = 8
        - calc degrees(3.14)     # Converts 3.14 radians to degrees
        - calc gcd(54, 24)       # Returns GCD of 54 and 24
        """
        
        console.print(help_text, style="bold cyan")
    
    def calculator(self, args):
        if not args:
            console.print("Usage:\n- calc <expression>\n- calc diff <expression> <variable>\n- calc integrate <expression> <variable>", style="bold red")
            return
        try:
            command = args[0]

            if command == "diff" and len(args) >= 3:
                expression = " ".join(args[1:-1])
                var = symbols(args[-1])
                result = diff(sympify(expression), var)
                console.print(f"Derivative of [bold yellow]{pretty(expression)}[/bold yellow] w.r.t [cyan]{var}[/cyan]:\n{pretty(result)}", style="bold green")


            elif command == "integrate" and len(args) >= 3:
                expression = " ".join(args[1:-1])
                var = symbols(args[-1])
                result = integrate(sympify(expression), var)
                console.print(f"Integral of [bold yellow]{pretty(expression)}[/bold yellow] w.r.t [cyan]{var}[/cyan]:\n{pretty(result)}", style="bold green")

            else:
                expression = " ".join(args)
                result = eval(expression, {"__builtins__": None}, math.__dict__)
                console.print(f"Result: {result}", style="bold green")

        except Exception as e:
            console.print(f"Error: {e}", style="bold red")
