import time
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from menu_base import MojiSwitchMenu
from rich.prompt import Prompt
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
import statistics
import numpy as np

console = Console()

def show_statistics_menu():
    # Define options for statistical operations
    options = [
        ("📊 Descriptive Stats", "descriptive"),
        ("📈 Regression", "regression"),
        ("📉 Correlation", "correlation"),
        ("📊 Hypothesis Test", "hypothesis"),
        ("📈 Time Series", "timeseries"),
        ("📊 Distribution", "distribution")
    ]
    
    def on_execute(state):
        selected = [name for name, value in options if state[value]]
        if not selected:
            console.print("[bold red]No operation selected![/bold red]")
            return
        if len(selected) > 1:
            console.print("[bold red]Please select only one operation at a time![/bold red]")
            return
        op = selected[0]
        step_text = f"Selected option: {op}"
        with Live(status_table(step_text, "Pending"), refresh_per_second=10, transient=True) as live:
            time.sleep(0.7)
            live.update(status_table(step_text, "In Progress"))
            time.sleep(0.7)
        try:
            if op == "📊 Descriptive Stats":
                data = Prompt.ask("[cyan]Enter numbers (comma-separated)[/cyan]")
                nums = [float(i) for i in data.split(",")]
                animate_calculation()
                mean = statistics.mean(nums)
                median = statistics.median(nums)
                try:
                    mode = statistics.mode(nums)
                except Exception:
                    mode = "No unique mode"
                stdev = statistics.stdev(nums) if len(nums) > 1 else "N/A"
                variance = statistics.variance(nums) if len(nums) > 1 else "N/A"
                result = {
                    "Mean": mean,
                    "Median": median,
                    "Mode": mode,
                    "Std Dev": stdev,
                    "Variance": variance
                }
                animate_results_display(result)
            elif op == "📈 Regression":
                data1 = Prompt.ask("[cyan]Enter numbers for Dataset 1 (comma-separated)[/cyan]")
                data2 = Prompt.ask("[cyan]Enter numbers for Dataset 2 (comma-separated)[/cyan]")
                x = [float(i) for i in data1.split(",")]
                y = [float(i) for i in data2.split(",")]
                if len(x) != len(y):
                    raise ValueError("Datasets must be of equal length.")
                animate_calculation()
                slope, intercept = np.polyfit(x, y, 1)
                result = {op: f"Y = {slope:.2f}X + {intercept:.2f}"}
                animate_results_display(result)
            elif op == "📉 Correlation":
                data1 = Prompt.ask("[cyan]Enter numbers for Dataset 1 (comma-separated)[/cyan]")
                data2 = Prompt.ask("[cyan]Enter numbers for Dataset 2 (comma-separated)[/cyan]")
                x = [float(i) for i in data1.split(",")]
                y = [float(i) for i in data2.split(",")]
                if len(x) != len(y):
                    raise ValueError("Datasets must be of equal length.")
                animate_calculation()
                corr = np.corrcoef(x, y)[0][1]
                result = {op: f"Correlation: {corr:.4f}"}
                animate_results_display(result)
            elif op == "📊 Hypothesis Test":
                with Live(status_table("Hypothesis Test", "Not implemented"), refresh_per_second=10, transient=True) as live:
                    time.sleep(1.2)
            elif op == "📈 Time Series":
                with Live(status_table("Time Series", "Not implemented"), refresh_per_second=10, transient=True) as live:
                    time.sleep(1.2)
            elif op == "📊 Distribution":
                with Live(status_table("Distribution", "Not implemented"), refresh_per_second=10, transient=True) as live:
                    time.sleep(1.2)
            else:
                animate_calculation()
                result = {op: f"Result for {op}"}
                animate_results_display(result)
        except Exception as e:
            error_table = Table(title="Error", show_header=False)
            error_table.add_row(f"[bold red]Error: {e}[/bold red]", "❌")
            with Live(error_table, refresh_per_second=10, transient=True):
                time.sleep(1.5)
    
    # Create and run menu (single-select logic)
    menu = MojiSwitchMenu(
        title="📊 Statistical Operations (Select ONE)",
        options=options,
        on_execute=on_execute
    )
    # Patch menu to only allow one selection at a time
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

def display_statistics_table(stats):
    """Display statistics in a modern table format"""
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
    
    # Add rows with statistical operations
    features = [
        ("1", "Descriptive Stats", "Calculate mean, median, mode, variance", "descriptive"),
        ("2", "Regression", "Linear and non-linear regression analysis", "regression"),
        ("3", "Correlation", "Measure relationships between variables", "correlation"),
        ("4", "Hypothesis Test", "Test statistical significance", "hypothesis"),
        ("5", "Time Series", "Analyze temporal data patterns", "timeseries"),
        ("6", "Distribution", "Probability distribution analysis", "distribution")
    ]
    
    for no, name, desc, key in features:
        status = "✅" if stats.get(key, False) else "❌"
        table.add_row(no, name, desc, status)
        
    # Create panel with table
    panel = Panel(
        table,
        title="📊 Statistical Analysis",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(panel)

def animate_calculation():
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("Calculating...", total=None)
        time.sleep(1.5)
        progress.update(task, description="Done!")
        time.sleep(0.5)

def animate_results_display(result_dict):
    table = Table(title="Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    for k, v in result_dict.items():
        table.add_row(str(k), str(v))
    with Live(table, refresh_per_second=10):
        time.sleep(1.2)

def animate_data_loading():
    """Animate data loading with a progress bar effect"""
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Loading data: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n")

def animate_export_progress():
    """Animate export progress with a progress bar effect"""
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Exporting results: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n") 

def status_table(step, status):
    table = Table(title="PyShell Statistics", show_header=True, header_style="bold blue")
    table.add_column("Step", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_row(step, status)
    return table 