import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from rich.panel import Panel
from rich import box
import time
from rich.text import Text
from rich.table import Table
from menu_base import MojiSwitchMenu

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
        equation = Prompt.ask("[bold blue]Enter f(x, y) = 0[/bold blue] (e.g., x**2 + y**2 - 1, mod(x, 2) - y)")
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

        try:
            choice = Prompt.ask("[bold green]Enter choice (1 or 2)[/bold green]")
        
            if choice == "1":
                self.plot_explicit()
            elif choice == "2":
                self.plot_implicit()
            else:
                self.console.print("[bold red]Invalid choice. Please enter 1 or 2.[/bold red]")
                
        except KeyboardInterrupt:
            print("\n")

def show_graphs_menu():
    # Define options for graph operations
    options = [
        ("📈 Line Plot", "line"),
        ("📊 Bar Chart", "bar"),
        ("📉 Scatter Plot", "scatter"),
        ("📊 Histogram", "histogram"),
        ("📈 Pie Chart", "pie"),
        ("📊 3D Plot", "3d")
    ]
    
    def on_execute(state):
        # Get list of enabled operations
        enabled_ops = [name for name, value in options if state[value]]
        if not enabled_ops:
            console.print("[bold red]No operations selected![/bold red]")
            return
            
        # Animate plot creation
        animate_plot_creation()
        
        # Process each enabled operation
        results = {}
        for op in enabled_ops:
            # Simulate plot creation
            time.sleep(0.5)
            results[op] = f"Plot created for {op}"
            
        # Display results
        animate_plot_display(results)
    
    # Create and run menu
    menu = MojiSwitchMenu(
        title="📊 Graph Operations",
        options=options,
        on_execute=on_execute
    )
    menu.run()

def display_graph_table(graphs):
    """Display graphs in a modern table format"""
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=None,
        padding=(0, 1)
    )
    
    # Add columns
    table.add_column("No.", style="dim", width=4)
    table.add_column("Type", style="bold")
    table.add_column("Description", style="italic")
    table.add_column("Status", justify="center", width=4)
    
    # Add rows with graph types
    features = [
        ("1", "Line Plot", "Plot continuous data points", "line"),
        ("2", "Bar Chart", "Compare categorical data", "bar"),
        ("3", "Scatter Plot", "Show relationships between variables", "scatter"),
        ("4", "Histogram", "Display data distribution", "histogram"),
        ("5", "Pie Chart", "Show proportional data", "pie"),
        ("6", "3D Plot", "Visualize three-dimensional data", "3d")
    ]
    
    for no, name, desc, key in features:
        status = "✅" if graphs.get(key, False) else "❌"
        table.add_row(no, name, desc, status)
        
    # Create panel with table
    panel = Panel(
        table,
        title="📊 Graph Types",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(panel)

def animate_plot_creation():
    """Animate plot creation with a progress bar effect"""
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Creating plot: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n")

def animate_plot_display(plots):
    """Animate plot display with a fade-in effect"""
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            for key, value in plots.items():
                console.print(f"[grey50]{key}: {value}[/grey50]")
        elif i == 1:
            for key, value in plots.items():
                console.print(f"[bold blue]{key}: {value}[/bold blue]")
        else:
            for key, value in plots.items():
                console.print(f"[bold green]{key}: {value}[/bold green]")
        time.sleep(0.2)
    console.print("\n")

def animate_data_loading():
    """Animate data loading with a spinning effect"""
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    console.print("\n")
    for _ in range(10):  # 1 second of animation
        for char in spinner:
            console.print(f"\033[A\033[K[bold blue]{char} Loading data...[/bold blue]")
            time.sleep(0.1)
    console.print("\n")

def animate_export_progress():
    """Animate export progress with a progress bar effect"""
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Exporting plot: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n")