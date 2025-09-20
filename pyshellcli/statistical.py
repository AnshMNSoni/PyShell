from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
import statistics
import numpy as np
from scipy import stats
from InquirerPy import inquirer

console = Console()

class StatisticsCalculator:
    def get_dataset(self, prompt):
        while True:
            try:
                user_input = Prompt.ask(f"[bold cyan]{prompt}[/] (comma-separated)")
                data = list(map(float, user_input.split(',')))
                if not data:
                    raise ValueError
                return data
            except ValueError:
                console.print("❌ [red]Invalid input. Please enter comma-separated numbers.[/red]\n")

    def display_result(self, title, result):
        panel = Panel.fit(
            Text(f"{result}", style="bold green"),
            title=f"[bold magenta]{title}[/bold magenta]",
            border_style="bright_blue"
        )
        console.print(panel)

    def calculate_statistics(self):
        while True:
            choice = inquirer.select(
                message="📊 Select the statistical measure you want to calculate:",
                choices=[
                    "Mean", "Median", "Mode", "Standard Deviation", "Variance",
                    "Covariance & Correlation",
                    "Spearman Rank Correlation",
                    "Regression Analysis",
                    "❌ Exit"
                ],
            ).execute()

            if choice == "❌ Exit":
                console.print("[bold red]Exiting the Statistics Calculator. Goodbye![/bold red]")
                break

            # Single-dataset measures
            if choice in ["Mean", "Median", "Mode", "Standard Deviation", "Variance"]:
                data = self.get_dataset("Enter numbers for Dataset 1")
                try:
                    if choice == "Mean":
                        result = statistics.mean(data)
                    elif choice == "Median":
                        result = statistics.median(data)
                    elif choice == "Mode":
                        result = statistics.mode(data)
                    elif choice == "Standard Deviation":
                        result = statistics.stdev(data)
                    elif choice == "Variance":
                        result = statistics.variance(data)

                    self.display_result(choice, result)
                except Exception as e:
                    console.print(f"❌ [red]Error calculating {choice}: {e}[/red]")

            # Two-dataset measures
            elif choice in ["Covariance & Correlation", "Spearman Rank Correlation", "Regression Analysis"]:
                data1 = self.get_dataset("Enter numbers for Dataset 1")
                data2 = self.get_dataset("Enter numbers for Dataset 2")
                try:
                    if len(data1) != len(data2):
                        raise ValueError("Datasets must be of equal length.")

                    if choice == "Covariance & Correlation":
                        cov = np.cov(data1, data2)[0][1]
                        corr = np.corrcoef(data1, data2)[0][1]

                        table = Table(title="Covariance & Pearson Correlation", style="cyan")
                        table.add_column("Measure", style="bold yellow")
                        table.add_column("Value", style="bold green")
                        table.add_row("Covariance", f"{cov:.4f}")
                        table.add_row("Pearson Correlation", f"{corr:.4f}")
                        console.print(table)

                    elif choice == "Spearman Rank Correlation":
                        spearman_corr, _ = stats.spearmanr(data1, data2)
                        self.display_result("Spearman Rank Correlation", f"{spearman_corr:.4f}")

                    elif choice == "Regression Analysis":
                        slope, intercept, r_value, p_value, std_err = stats.linregress(data1, data2)

                        table = Table(title="Linear Regression Analysis", style="cyan")
                        table.add_column("Metric", style="bold yellow")
                        table.add_column("Value", style="bold green")
                        table.add_row("Regression Line", f"Y = {slope:.2f}X + {intercept:.2f}")
                        table.add_row("R-squared", f"{r_value**2:.4f}")
                        table.add_row("P-value", f"{p_value:.4f}")
                        table.add_row("Std. Error", f"{std_err:.4f}")
                        console.print(table)

                except Exception as e:
                    console.print(f"❌ [red]Error: {e}[/red]\n")
