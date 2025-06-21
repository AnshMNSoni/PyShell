import time
import shlex
import subprocess
import schedule
from rich.console import Console
from rich.text import Text
from menu_base import MojiSwitchMenu
from statistics_menu import show_statistics_menu

console = Console()

scheduled_jobs = {}
commands = {} 
stop_scheduler = False 

def animate_task_creation():
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    console.print("\n")
    for _ in range(10):
        for char in spinner:
            console.print(f"\033[A\033[K[bold blue]{char} Creating task...[/bold blue]")
            time.sleep(0.1)
    console.print("\n")

def animate_task_completion():
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            console.print("[grey50]✓ Task completed[/grey50]")
        elif i == 1:
            console.print("[bold blue]✓ Task completed[/bold blue]")
        else:
            console.print("[bold green]✓ Task completed[/bold green]")
        time.sleep(0.2)
    console.print("\n")

def animate_task_deletion():
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            console.print("[bold red]Task deleted[/bold red]")
        elif i == 1:
            console.print("[red]Task deleted[/red]")
        else:
            console.print("[grey50]Task deleted[/grey50]")
        time.sleep(0.2)
    console.print("\n")

def animate_task_scheduling():
    console.print("\n")
    for i in range(10):
        progress = "█" * i + "░" * (10 - i)
        console.print(f"\033[A\033[K[bold blue]Scheduling task: [{progress}] {i*10}%[/bold blue]")
        time.sleep(0.2)
    console.print("\n")

def animate_task_list_display(tasks):
    console.print("\n")
    for i in range(3):
        console.print("\033[A\033[K", end="")
        if i == 0:
            for task in tasks:
                console.print(f"[grey50]{task}[/grey50]")
        elif i == 1:
            for task in tasks:
                console.print(f"[bold blue]{task}[/bold blue]")
        else:
            for task in tasks:
                console.print(f"[bold green]{task}[/bold green]")
        time.sleep(0.2)
    console.print("\n")

class Task:
    def __init__(self):
        self.tasks = []  # Simple in-memory task list
        self.completed = set()

    def create_task(self, name):
        self.tasks.append(name)
        animate_task_creation()
        console.print(f"[bold green]Task created:[/bold green] {name}")

    def list_tasks(self):
        if not self.tasks:
            console.print("No tasks available.", style="bold yellow")
        else:
            animate_task_list_display(self.tasks)

    def complete_task(self, idx):
        try:
            idx = int(idx) - 1
            if 0 <= idx < len(self.tasks):
                self.completed.add(self.tasks[idx])
                animate_task_completion()
                console.print(f"[bold green]Task completed:[/bold green] {self.tasks[idx]}")
            else:
                console.print("[bold red]Invalid task number![/bold red]")
        except Exception:
            console.print("[bold red]Invalid input![/bold red]")

    def delete_task(self, idx):
        try:
            idx = int(idx) - 1
            if 0 <= idx < len(self.tasks):
                animate_task_deletion()
                console.print(f"[bold yellow]Task deleted:[/bold yellow] {self.tasks[idx]}")
                del self.tasks[idx]
            else:
                console.print("[bold red]Invalid task number![/bold red]")
        except Exception:
            console.print("[bold red]Invalid input![/bold red]")

    def execute_command(self, args):
        if not args:
            console.print("[bold red]No command entered![/bold red]")
            return
        command_name = args[0]
        command_args = args[1:]
        if command_name in commands:
            try:
                commands[command_name](*command_args)
            except TypeError as e:
                console.print(f"[bold red]Error executing command '{command_name}': {e}[/bold red]")
        else:
            try:
                subprocess.run([command_name] + command_args, check=True, text=True)
            except FileNotFoundError:
                console.print(f"[bold red]Unknown command: {command_name}. Type 'help' for a list of commands.[/bold red]")
            except Exception as e:
                console.print(f"[bold red]Error executing command: {e}[/bold red]")

    def run_scheduled_task(self, args=None):
        global stop_scheduler
        if stop_scheduler:
            console.print("[bold red]Task execution stopped.[/bold red]")
            return
        if args is None or len(args) < 3:
            console.print("[bold red]Invalid task arguments![/bold red]")
            return
        command = " ".join(args[2:])
        console.print(f"[bold green]Running scheduled task:[/bold green] {command}")
        cmd_parts = shlex.split(command)
        self.execute_command(cmd_parts)

    def schedule_task(self, args):
        if len(args) < 3:
            console.print("Usage: schedule <interval> <unit> <command>", style="bold red")
            console.print("Example: schedule 10 seconds say 'Hello'", style="bold yellow")
            return
        try:
            interval = int(args[0])
        except ValueError:
            console.print("[bold red]Invalid interval! Must be an integer.[/bold red]")
            return
        unit = args[1].lower()
        if unit in ["seconds", "minutes", "hours"]:
            job = getattr(schedule.every(interval), unit).do(self.run_scheduled_task, args)
            job_id = len(scheduled_jobs) + 1
            scheduled_jobs[job_id] = job
            animate_task_scheduling()
            console.print(f"Task scheduled every {interval} {unit}. Task ID: {job_id}", style="bold cyan")
        else:
            console.print("[bold red]Invalid time unit! Use: seconds, minutes, or hours.[/bold red]")

    def stop_running_tasks(self, *args):
        global stop_scheduler
        stop_scheduler = True
        schedule.clear()
        console.print("[bold red]Stopping all scheduled tasks...[/bold red]")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def list_scheduled_tasks(self, _=None):
        if not scheduled_jobs:
            console.print("No scheduled tasks.", style="bold yellow")
        else:
            console.print("Scheduled Tasks:", style="bold cyan")
            for job_id, job in scheduled_jobs.items():
                console.print(f"[{job_id}] {job}", style="bold green")

    def remove_scheduled_task(self, args):
        if not args:
            console.print("Usage: unschedule <task_id>", style="bold red")
            return
        try:
            task_id = int(args[0])
            if task_id in scheduled_jobs:
                schedule.cancel_job(scheduled_jobs[task_id])
                del scheduled_jobs[task_id]
                console.print(f"Task {task_id} unscheduled.", style="bold yellow")
            else:
                console.print(f"No task found with ID {task_id}.", style="bold red")
        except ValueError:
            console.print("[bold red]Invalid task ID! Must be an integer.[/bold red]")

def show_tasks_menu():
    options = [
        ("📝 Create Task", "create"),
        ("📋 List Tasks", "list"),
        ("✅ Complete Task", "complete"),
        ("❌ Delete Task", "delete"),
        ("⏰ Schedule Task", "schedule"),
        ("📊 Task Stats", "stats")
    ]
    task = Task()
    def on_execute(state):
        enabled_ops = [name for name, value in options if state[value]]
        if not enabled_ops:
            console.print("[bold red]No operations selected![/bold red]")
            return
        for op in enabled_ops:
            if op == "📝 Create Task":
                name = console.input("Enter task name: ")
                task.create_task(name)
            elif op == "📋 List Tasks":
                task.list_tasks()
            elif op == "✅ Complete Task":
                idx = console.input("Enter task number to complete: ")
                task.complete_task(idx)
            elif op == "❌ Delete Task":
                idx = console.input("Enter task number to delete: ")
                task.delete_task(idx)
            elif op == "⏰ Schedule Task":
                args = console.input("Enter: <interval> <unit> <command>: ").split()
                task.schedule_task(args)
            elif op == "📊 Task Stats":
                show_statistics_menu()
    menu = MojiSwitchMenu(
        title="📝 Task Operations",
        options=options,
        on_execute=on_execute
    )
    menu.run() 