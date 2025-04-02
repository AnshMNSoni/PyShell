# Task Scheduling

from rich.console import Console
import shlex, subprocess, time, schedule

console = Console()
scheduled_jobs = {}
commands = {} 
stop_scheduler = False 

class Task:      
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
        """Executes a scheduled command."""
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
            console.print(f"Task scheduled every {interval} {unit}. Task ID: {job_id}", style="bold cyan")
        else:
            console.print("[bold red]Invalid time unit! Use: seconds, minutes, or hours.[/bold red]")

    def stop_running_tasks(self, *args):
        """Sets the stop flag to True to prevent new tasks from running."""
        global stop_scheduler
        stop_scheduler = True
        schedule.clear()
        console.print("[bold red]Stopping all scheduled tasks...[/bold red]")

    def run_scheduler(self):
        """Continuously runs pending scheduled tasks in the background."""
        while True:
            schedule.run_pending()
            time.sleep(1)  

    def list_scheduled_tasks(self, _):
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