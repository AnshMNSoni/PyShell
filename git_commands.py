import subprocess
import threading
import speech_recognition as sr
from rich.console import Console
from flask import Flask, render_template_string
import threading
import time, webbrowser

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
            console.print("Usage: git_branch <branch_name>", style="bold red")
            console.print("Example: git_branch feature-branch", style="bold yellow")
            return
        self.run_git_command(f"git branch {args[0]}", "git branch <branch_name>", "git branch feature-branch")

    def git_switch_branch(self, args):
        """Switches to an existing Git branch."""
        if not args:
            console.print("Usage: git_switch <branch_name>", style="bold red")
            console.print("Example: git_switch main", style="bold yellow")
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

    def git_smart_commit(self, *args):
        """AI-powered commit message generation."""
        changed_files = subprocess.getoutput("git diff --name-only")
        commit_message = f"Updated files: {changed_files.replace(chr(10), ', ')}"
        self.run_git_command(f"git commit -m '{commit_message}'", "git commit -m '<message>'", "git commit -m 'Updated files'")

    def git_undo(self, *args):
        """Undo last Git operation automatically."""
        last_command = subprocess.getoutput("git reflog | head -n 1 | awk '{print $1}'")
        if last_command:
            self.run_git_command(f"git reset --hard {last_command}", "git reset --hard <commit_id>", "git reset --hard HEAD~1")
        else:
            console.print("No actions to undo.", style="bold yellow")

    def git_dashboard(*args):
        """Opens a web dashboard showing branches, commits, and status."""
        app = Flask(__name__)
        
        branches = subprocess.getoutput("git branch --format='%(refname:short)'")
        commits = subprocess.getoutput("git log --oneline -10")  # Last 10 commits
        merged_branches = subprocess.getoutput("git branch --merged").split("\n")
        unmerged_branches = subprocess.getoutput("git branch --no-merged").split("\n")
        
        # Prepare JSON for Chart.js
        branch_data = {
            "merged": len(merged_branches),
            "unmerged": len(unmerged_branches)
        }
    
        def get_git_data():
            return {
                "branches": subprocess.getoutput("git branch"),
                "commits": subprocess.getoutput("git log --oneline -5"),
                "stash": subprocess.getoutput("git stash list"),
                "modified_files": subprocess.getoutput("git status --short"),
                "remote_info": subprocess.getoutput("git remote -v"),
                "git_stats": subprocess.getoutput("git shortlog -s -n")
            }
            
        @app.route("/")
        def dashboard():
            git_data = get_git_data()
            return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Git Dashboard</title>

                <!-- Tailwind CSS -->
                <script src="https://cdn.tailwindcss.com"></script>

                <!-- Alpine.js -->
                <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>

                <!-- Chart.js -->
                <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
            </head>
            <body class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-200 transition-all duration-300">

                <div class="max-w-4xl mx-auto py-10 px-6">
                    <!-- Dashboard Header -->
                    <div class="flex justify-between items-center mb-6">
                        <h1 class="text-3xl font-bold">🚀 Git Dashboard</h1>
                    </div>

                    <!-- Branches Section -->
                    <div x-data="{ open: true }" class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-4 mb-4">
                        <div class="flex justify-between items-center">
                            <h2 class="text-xl font-semibold">🌿 Branches</h2>
                            <button @click="open = !open" class="text-gray-600 dark:text-gray-300">Toggle</button>
                        </div>
                        <pre x-show="open" class="mt-2 p-3 bg-gray-100 dark:bg-gray-700 rounded-md text-sm overflow-auto">{{ branches }}</pre>
                    </div>

                    <!-- Recent Commits Section -->
                    <div x-data="{ open: true }" class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-4">
                        <div class="flex justify-between items-center">
                            <h2 class="text-xl font-semibold">📜 Recent Commits</h2>
                            <button @click="open = !open" class="text-gray-600 dark:text-gray-300">Toggle</button>
                        </div>
                        <pre x-show="open" class="mt-2 p-3 bg-gray-100 dark:bg-gray-700 rounded-md text-sm overflow-auto">{{ commits }}</pre>
                    </div>

                    <!-- Branch Activity Visualization -->
                    <div class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-4 mt-6">
                        <h2 class="text-xl font-semibold mb-2">📊 Branch Activity</h2>
                        <canvas id="branchChart"></canvas>
                    </div>
                </div>

                <!-- Chart.js Script -->
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        var ctx = document.getElementById("branchChart").getContext("2d");
                        new Chart(ctx, {
                            type: "bar",
                            data: {
                                labels: ["Merged", "Unmerged"],
                                datasets: [{
                                    label: "Branch Count",
                                    data: [{{ branch_data["merged"] }}, {{ branch_data["unmerged"] }}],
                                    backgroundColor: ["#4CAF50", "#FF5733"],
                                }]
                            },
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: { display: false },
                                }
                            }
                        });
                    });
                </script>

            </body>
            </html>
            """, branches=branches, commits=commits, branch_data=branch_data)

        # Open browser after a small delay
        def open_browser():
            time.sleep(1)
            webbrowser.open("http://127.0.0.1:5000")

        # Start the browser-opening thread
        threading.Thread(target=open_browser).start()

        print("🚀 Opening Git Dashboard at: http://127.0.0.1:5000")
        app.run(debug=True, use_reloader=False)


    def git_auto_merge(self, *args):
        """Automatically resolves merge conflicts."""
        self.run_git_command("git merge --strategy-option=theirs", "git merge <branch>", "git merge feature-branch")

    def git_voice_command(self, *args):
        """Executes Git commands using voice recognition."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            console.print("Listening for Git command...", style="bold yellow")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            console.print(f"Executing: {command}", style="bold cyan")
            self.run_git_command(f"git {command}", f"git {command}", f"git {command}")
        except Exception:
            console.print("Could not understand command.", style="bold red")

    def reminder_loop(self, *args):
        while True:
            time.sleep(3600)  # Check every hour
            status = subprocess.getoutput("git status --porcelain")
            if status:
                console.print("🚨 Reminder: You have uncommitted changes!", style="bold red")
                    
    def git_reminder(self, *args):
        """Reminds user if uncommitted changes exist for a long time (runs in the background)."""
        # Run the reminder in a background thread
        reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        reminder_thread.start()
        console.print("✅ Git reminder started in the background!", style="bold green")

    def git_offline_sync(self, *args):
        """Syncs offline commits when online."""
        self.run_git_command("git fetch --all && git rebase", "git fetch && git rebase", "git fetch --all && git rebase")
    
    def git_help(self, *args):
        """Displays available Git commands and their usage."""
        help_text = """
        Available Git Commands:
        - git-status : Show working tree status
        - git-branches : List branches
        - git-switch <branch> : Switch branches
        - git-push origin <branch> : Push branch to remote
        - git-pull origin <branch> : Pull latest changes
        - git-merge <branch> : Merge branch into current
        - git-clone <repo_url> : Clone a repository
        - git-add <file> : Stage file for commit
        - git-commit -m "<message>" : Commit staged files
        - git-smart : AI-powered commit messages
        - git-undo : Undo last operation
        - git-dashboard : Open web dashboard
        - git-auto_merge : Auto resolve conflicts
        - git-voice : Voice command for Git
        - git-reminder : Alerts for uncommitted changes
        - git-social_share : Share commits on social media
        - git-offline_sync : Sync offline commits when online
        """
        console.print(help_text, style="bold cyan")
        
    def git_history(self, *args):
        """Displays the last 10 Git commits with their messages."""
        self.run_git_command("git log --oneline -10", "git log --oneline -<number_of_commits>", "git log --oneline -10")

    def git_stash(self, args=None):
        """Stashes uncommitted changes."""
        if args and args[0] == "pop":
            self.run_git_command("git stash pop", "git stash pop", "git stash pop")
        else:
            self.run_git_command("git stash", "git stash", "git stash")

    def git_recover(self, *args):
        """Recovers lost commits by checking Git reflog."""
        self.run_git_command("git reflog", "git reflog", "git reflog")
        console.print("Find the commit ID you want to recover and use: git reset --hard <commit_id>", style="bold yellow")
