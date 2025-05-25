import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from rich.panel import Panel
from rich import box

# Safe functions for eval
SAFE_FUNCTIONS = {
    "np": np,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "log": np.log,
    "log10": np.log10,
    "exp": np.exp,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "mod": np.mod,
    "pi": np.pi,
    "e": np.e,
}

console = Console()


class GraphPlotter:
    def __init__(self):
        self.console = console

    def plot_explicit(self):
        equation = Prompt.ask("[bold blue]Enter f(x)[/bold blue] (e.g., x**2, sin(x), mod(x,2))")
        x_min = FloatPrompt.ask("[green]Enter minimum x-value[/green]")
        x_max = FloatPrompt.ask("[green]Enter maximum x-value[/green]")
        x = np.linspace(x_min, x_max, 500)

        try:
            y = eval(equation, {**SAFE_FUNCTIONS, "x": x})
            plt.plot(x, y, label=f"f(x) = {equation}", color='blue')
            plt.title("Explicit Graph of the Function")
            plt.xlabel("x-axis")
            plt.ylabel("f(x)")
            plt.grid(True)
            plt.legend()
            plt.show()
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def plot_implicit(self):
        equation = Prompt.ask("[bold blue]Enter f(x, y) = 0[/bold blue] (e.g., x**2 + y**2 - 1)")
        x_min = FloatPrompt.ask("[green]Enter minimum x-value[/green]")
        x_max = FloatPrompt.ask("[green]Enter maximum x-value[/green]")
        y_min = FloatPrompt.ask("[green]Enter minimum y-value[/green]")
        y_max = FloatPrompt.ask("[green]Enter maximum y-value[/green]")

        x = np.linspace(x_min, x_max, 400)
        y = np.linspace(y_min, y_max, 400)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(equation, {**SAFE_FUNCTIONS, "x": X, "y": Y})
            plt.contour(X, Y, Z, levels=[0], colors='red')
            plt.title("Implicit Graph (Contour Plot)")
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
            plt.grid(True)
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.show()
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def run(self):
        self.console.print(Panel.fit("📈 [bold cyan]PyShell Graph Plotter[/bold cyan] 📊", box=box.DOUBLE, style="bold green"))
        self.console.print("[yellow]What type of function would you like to plot?[/yellow]")
        self.console.print("[blue]1.[/blue] Explicit: y = f(x)")
        self.console.print("[blue]2.[/blue] Implicit: f(x, y) = 0")

        choice = Prompt.ask("[bold green]Enter choice (1 or 2)[/bold green]")
        
        if choice == "1":
            self.plot_explicit()
        elif choice == "2":
            self.plot_implicit()
        else:
            self.console.print("[bold red]Invalid choice. Please enter 1 or 2.[/bold red]")

