from sympy import symbols, sympify, Eq, solve, pretty
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import re

console = Console()

class Equations:
    def solve_equation(self, args):
        if not args:
            console.print("Usage: equation <expression> [= <rhs>] [<variable>]", style="bold red")
            return
        try:
            # Join arguments to form the equation string
            full_expr = " ".join(args)

            # Detect variables automatically, default to 'x' if none found
            variables = sorted(set(re.findall(r'[a-zA-Z]\w*', full_expr)))
            var = symbols(variables[0]) if variables else symbols('x')

            # Split into LHS and RHS
            if '=' in full_expr:
                lhs, rhs = full_expr.split('=')
                lhs_expr = sympify(lhs.strip())
                rhs_expr = sympify(rhs.strip())
                equation = Eq(lhs_expr, rhs_expr)
            else:
                lhs_expr = sympify(full_expr)
                equation = Eq(lhs_expr, 0)

            # Solve the equation
            solutions = solve(equation, var)

            # Format output
            if not solutions:
                console.print(Panel("No solutions found.", style="bold yellow"))
            else:
                pretty_eq = pretty(equation)
                pretty_solutions = "\n".join(
                    [f"[bold green]{i+1}.[/bold green] [cyan]{str(sol.evalf())}[/cyan]" for i, sol in enumerate(solutions)]
                )
            
                console.print(Panel.fit(
                    Text.from_markup(
                        f"[bold cyan]Equation:[/bold cyan]\n{pretty_eq}"
                        f"\n\n[bold white]Solutions w.r.t [bold cyan]{var}[/bold cyan]:[/bold white]\n{pretty_solutions}"
                    ),
                    title="[bold magenta]Equation Solver[/bold magenta]",
                    border_style="bright_blue"
                ))
            
            
        except Exception as e:
            console.print(Panel(f"Error: {e}", style="bold red"))
