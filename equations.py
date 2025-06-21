from sympy import symbols, sympify, Eq, solve, pretty, Function, dsolve, Derivative, simplify, pretty_print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from sympy.parsing.sympy_parser import parse_expr
import re
from sympy.abc import x
import time
import msvcrt
from rich.table import Table
from menu_base import MojiSwitchMenu
from statistics_menu import show_statistics_menu

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
    def solve_differential(self, args):
        console = Console()

        console.print(Panel.fit(
            "[bold cyan]🧠 Solve n-th Order Differential Equations[/bold cyan]",
            subtitle="[magenta]PyShell[/magenta]",
            border_style="green"
        ))

        console.print(Panel(
            "[bold yellow]Input Format:[/bold yellow]\n"
            "- Use [bold]y(x)[/bold] as the dependent variable\n"
            "- Use [bold]Derivative(y(x), x)[/bold] for dy/dx\n"
            "- Higher orders: [bold]Derivative(y(x), x, x)[/bold], etc.\n"
            "- Separate LHS and RHS with '='\n\n"
            "🔹 Example: [italic]Derivative(y(x), x, x) + 2*Derivative(y(x), x) = exp(2*x)*tan(x)[/italic]",
            title="📝 How to Enter", border_style="blue"
        ))

        user_input = Prompt.ask("[green]📥 Enter your differential equation")

        y = Function('y')

        try:
            lhs_str, rhs_str = user_input.split('=')
            lhs = parse_expr(lhs_str.strip(), evaluate=False)
            rhs = parse_expr(rhs_str.strip(), evaluate=False)

            equation = Eq(lhs, rhs)
            solution = dsolve(equation, y(x))

            console.print(Panel.fit("[bold green]✅ Solved Successfully![/bold green]", border_style="green"))

            console.print(Panel(
                "[bold white]🖨 Solution:[/bold white]",
                border_style="cyan"
            ))

            pretty_print(solution)

        except Exception as e:
            console.print(Panel(
                f"[red]❌ Error:[/red] {str(e)}\n"
                "Please ensure your equation is in the correct format.",
                title="⚠️ Invalid Input", border_style="red"
            ))

def show_equations_menu():
    # Define options for equation operations
    options = [
        ("➕ Basic Math", "basic"),
        ("📐 Algebra", "algebra"),
        ("📊 Calculus", "calculus"),
        ("📈 Statistics", "stats"),
        ("🔢 Matrix", "matrix")
    ]
    
    def on_execute(state):
        # Get list of enabled operations
        enabled_ops = [name for name, value in options if state[value]]
        if not enabled_ops:
            console.print("[bold red]No operations selected![/bold red]")
            return
            
        # Animate calculation
        animate_calculation()
        
        # Process each enabled operation
        results = {}
        for op in enabled_ops:
            # Simulate calculation
            time.sleep(0.5)
            results[op] = f"Result for {op}"
            
        # Display results
        animate_results_display(results)
    
    # Create and run menu
    menu = MojiSwitchMenu(
        title="🧮 Equation Operations",
        options=options,
        on_execute=on_execute
    )
    menu.run()

def display_equation_table(equations):
    """Display equations in a modern table format"""
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
    
    # Add rows with equation types
    features = [
        ("1", "Basic Math", "Arithmetic and algebraic operations", "basic"),
        ("2", "Algebra", "Solve linear and quadratic equations", "algebra"),
        ("3", "Calculus", "Derivatives and integrals", "calculus"),
        ("4", "Statistics", "Statistical formulas and calculations", "stats"),
        ("5", "Matrix", "Matrix operations and determinants", "matrix")
    ]
    
    for no, name, desc, key in features:
        status = "✅" if equations.get(key, False) else "❌"
        table.add_row(no, name, desc, status)
        
    # Create panel with table
    panel = Panel(
        table,
        title="🧮 Equation Types",
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(panel)

def animate_calculation():
    """Animate calculation with a spinning effect"""
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    console.print("\n")
    for _ in range(20):  # 2 seconds of animation
        for char in spinner:
            console.print(f"\033[A\033[K[bold blue]{char} Calculating...[/bold blue]")
            time.sleep(0.1)
    console.print("\n")

def animate_results_display(results):
    """Animate results display with a fade-in effect"""
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            for key, value in results.items():
                console.print(f"[grey50]{key}: {value}[/grey50]")
        elif i == 1:
            for key, value in results.items():
                console.print(f"[bold blue]{key}: {value}[/bold blue]")
        else:
            for key, value in results.items():
                console.print(f"[bold green]{key}: {value}[/bold green]")
        time.sleep(0.2)
    console.print("\n")

def animate_equation_solving(equation):
    """Animate equation solving with a step-by-step effect"""
    console.print("\n")
    steps = [
        f"Original equation: {equation}",
        "Simplifying...",
        "Solving for x...",
        "Checking solution..."
    ]
    
    for step in steps:
        console.print(f"\033[A\033[K[bold blue]{step}[/bold blue]")
        time.sleep(0.5)
    console.print("\n")

def animate_matrix_operation():
    """Animate matrix operation with a progress bar effect"""
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Performing matrix operation: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n")

def solve_equation(equation_str):
    try:
        # Split equation into left and right sides
        left, right = equation_str.split('=')
        
        # Convert strings to sympy expressions
        left_expr = parse_expr(left.strip())
        right_expr = parse_expr(right.strip())
        
        # Create equation
        equation = Eq(left_expr, right_expr)
        
        # Solve equation
        solution = solve(equation, x)
        
        return solution
    except Exception as e:
        console.print(f"Error solving equation: {e}", style="bold red")
        return None