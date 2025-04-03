import subprocess
from rich.console import Console

console = Console()

class Git:
    def run_git_command(self, command, syntax, example):
        """Runs a Git command and provides syntax if incorrect."""
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)

            if result.returncode != 0:
                console.print(f"Error: {result.stderr.strip()}", style="bold red")
                console.print(f"Usage: {syntax}", style="bold yellow")
                console.print(f"Example: {example}", style="bold green")
            else:
                console.print(result.stdout, style="bold cyan")

        except Exception as e:
            console.print(f"An error occurred: {str(e)}", style="bold red")

    def git_status(self, _=None):
        """Displays the current Git status."""
        self.run_git_command("git status", "git status", "git status")

    def git_branches(self, _=None):
        """Lists all Git branches."""
        self.run_git_command("git branch", "git branch", "git branch")

    def git_create_branch(self, args):
        """Creates a new Git branch."""
        if not args:
            console.print("Usage: git branch <branch_name>", style="bold red")
            console.print("Example: git branch feature-branch", style="bold yellow")
            return
        self.run_git_command(f"git branch {args[0]}", "git branch <branch_name>", "git branch feature-branch")

    def git_switch_branch(self, args):
        """Switches to an existing Git branch."""
        if not args:
            console.print("Usage: git checkout <branch_name>", style="bold red")
            console.print("Example: git checkout main", style="bold yellow")
            return
        self.run_git_command(f"git checkout {args[0]}", "git checkout <branch_name>", "git checkout main")

    def git_push(self, args):
        """Pushes the current branch to remote."""
        if not args:
            console.print("Usage: git push origin <branch_name>", style="bold red")
            console.print("Example: git push origin main", style="bold yellow")
            return
        self.run_git_command(f"git push origin {args[0]}", "git push origin <branch_name>", "git push origin main")

    def git_pull(self, args):
        """Pulls the latest changes from a remote branch."""
        if not args:
            console.print("Usage: git pull origin <branch_name>", style="bold red")
            console.print("Example: git pull origin main", style="bold yellow")
            return
        self.run_git_command(f"git pull origin {args[0]}", "git pull origin <branch_name>", "git pull origin main")

    def git_merge(self, args):
        """Merges a specified branch into the current branch."""
        if not args:
            console.print("Usage: git merge <branch_name>", style="bold red")
            console.print("Example: git merge feature-branch", style="bold yellow")
            return
        self.run_git_command(f"git merge {args[0]}", "git merge <branch_name>", "git merge feature-branch")

    def git_delete_branch(self, args):
        """Deletes a local Git branch."""
        if not args:
            console.print("Usage: git branch -d <branch_name>", style="bold red")
            console.print("Example: git branch -d feature-branch", style="bold yellow")
            return
        self.run_git_command(f"git branch -d {args[0]}", "git branch -d <branch_name>", "git branch -d feature-branch")
    
    def git_clone(self, args):
        """Clones a Git repository."""
        if not args:
            console.print("Usage: git clone <repository_url>", style="bold red")
            console.print("Example: git clone https://github.com/user/repo.git", style="bold yellow")
            return
        self.run_git_command(f"git clone {args[0]}", "git clone <repository_url>", "git clone https://github.com/user/repo.git")
        
    def git_add(self, args):
        """Stages files for commit."""
        if not args:
            console.print("Usage: git add <file_name> OR git add .", style="bold red")
            console.print("Example: git add myfile.py", style="bold yellow")
            console.print("Example: git add . (stages all files)", style="bold green")
            return
        self.run_git_command(f"git add {args[0]}", "git add <file_name>", "git add myfile.py")

    def git_commit(self, args):
        """Commits staged files with a message."""
        if not args:
            console.print("Usage: git commit -m \"<commit_message>\"", style="bold red")
            console.print("Example: git commit -m \"Added new feature\"", style="bold yellow")
            return
        self.run_git_command(f"git commit -m \"{args[0]}\"", "git commit -m \"<commit_message>\"", "git commit -m \"Added new feature\"")
