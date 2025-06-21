import os
from typing import Dict, List, Tuple, Callable
from rich.console import Console
from rich.text import Text

console = Console()

class MojiSwitchMenu:
    def __init__(self, title: str, options: List[Tuple[str, str]], on_execute: Callable = None):
        """
        Initialize the menu with options and optional execute callback.
        
        Args:
            title: Menu title
            options: List of (display_name, value) tuples
            on_execute: Optional callback function when execute is pressed
        """
        self.title = title
        self.options = options
        self.on_execute = on_execute
        self.state = {value: False for _, value in options}
        self.key_map = {str(i+1): value for i, (_, value) in enumerate(options)}
        
    def clear_screen(self):
        """Clear the terminal screen efficiently."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display(self):
        """Display the current menu state."""
        self.clear_screen()
        console.print(f"\n[bold cyan]{self.title}[/bold cyan]\n")
        
        for idx, (name, value) in enumerate(self.options, 1):
            status = "✅" if self.state[value] else "❌"
            console.print(f"{idx}. {name}: {status}")
            
        console.print("\n[dim]Use number keys to toggle, E to execute, Q to quit[/dim]")
        
    def handle_input(self, choice: str) -> bool:
        """
        Handle user input and return True if should continue, False if should exit.
        
        Args:
            choice: User input string
            
        Returns:
            bool: True to continue, False to exit
        """
        choice = choice.strip().lower()
        
        if choice in self.key_map:
            # Toggle state
            value = self.key_map[choice]
            self.state[value] = not self.state[value]
            return True
            
        elif choice == 'e':
            # Execute with current state
            self.clear_screen()
            console.print("[bold green]Selected options:[/bold green]")
            for name, value in self.options:
                if self.state[value]:
                    console.print(f" - {name}")
                    
            if self.on_execute:
                self.on_execute(self.state)
                
            console.print("\n[dim]Press Enter to return to menu[/dim]")
            input()
            return True
            
        elif choice == 'q':
            return False
            
        return True
        
    def run(self):
        """Run the menu loop."""
        while True:
            self.display()
            choice = input("Choice: ")
            if not self.handle_input(choice):
                break

# Example usage:
if __name__ == "__main__":
    # Example menu for statistics
    stats_menu = MojiSwitchMenu(
        title="Statistical Operations",
        options=[
            ("Mean", "mean"),
            ("Median", "median"),
            ("Mode", "mode"),
            ("Standard Deviation", "stddev"),
            ("Variance", "variance")
        ],
        on_execute=lambda state: print(f"Executing with state: {state}")
    )
    stats_menu.run() 