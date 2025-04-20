from sympy import symbols, sympify, Eq, solve, pretty, Function, dsolve, Derivative, simplify
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import re

console = Console()

class Equations:
    def solve_equation(self, args):
        if not args:
            console.print("Usage: equation <equation1> [; <equation2>; ...]", style="bold red")
            return

        try:
            # Join args and split by semicolon for multiple equations
            input_str = " ".join(args)
            raw_equations = [eq.strip() for eq in input_str.split(';') if eq.strip()]

            # Extract all variable names from input string
            symbol_names = sorted(set(re.findall(r'[a-zA-Z_]\w*', input_str)))
            sym_vars_dict = {name: symbols(name) for name in symbol_names}

            # Parse equations
            equations = []
            for eq_str in raw_equations:
                if '=' in eq_str:
                    lhs, rhs = eq_str.split('=')
                    lhs_expr = sympify(lhs.strip(), locals=sym_vars_dict)
                    rhs_expr = sympify(rhs.strip(), locals=sym_vars_dict)
                    equations.append(Eq(lhs_expr, rhs_expr))
                else:
                    lhs_expr = sympify(eq_str, locals=sym_vars_dict)
                    equations.append(Eq(lhs_expr, 0))

            # Infer variables from equations
            vars_in_equations = list(set().union(*[eq.free_symbols for eq in equations]))

            # Limit number of variables if underdetermined
            if len(equations) < len(vars_in_equations):
                vars_to_solve = vars_in_equations[:len(equations)]
            else:
                vars_to_solve = vars_in_equations

            # Solve the system of equations
            solutions = solve(equations, vars_to_solve, dict=True)

            # Format output
            if not solutions:
                console.print(Panel("No solutions found or system is inconsistent.", style="bold yellow"))
            else:
                # Pretty print equations
                pretty_eqs = "\n".join([pretty(eq) for eq in equations])
                # Display all variable values
                pretty_solutions = ""
                for i, sol in enumerate(solutions, 1):
                    sol_lines = [f"[bold cyan]{str(k)}[/bold cyan] = [green]{str(v.evalf())}[/green]" for k, v in sol.items()]
                    pretty_solutions += f"[bold green]{i}.[/bold green]\n" + "\n".join(sol_lines) + "\n\n"

                console.print(Panel.fit(
                    Text.from_markup(
                        f"[bold cyan]System of Equations:[/bold cyan]\n{pretty_eqs}"
                        f"\n\n[bold white]Solutions:[/bold white]\n{pretty_solutions.strip()}"
                    ),
                    title="[bold magenta]Equation Solver[/bold magenta]",
                    border_style="bright_blue"
                ))

        except Exception as e:
            console.print(Panel(f"Error: {e}", style="bold red"))
    
    
    
    # Differential equation solver