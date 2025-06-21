import os
import json
import html

COMMAND_HINTS = {
    "git": "Try: 'git status', 'git add <file>', 'git commit -m \"message\"'",
    "ls": "Try: 'ls -l' for details, 'ls -a' to show hidden files",
    "cd": "Try: 'cd ..' to go up, 'cd /path/to/dir' for absolute path",
    "python": "Try: 'python my_script.py'",
    "pip": "Try: 'pip install <package>', 'pip freeze > requirements.txt'",
    "docker": "Try: 'docker ps', 'docker build .', 'docker run <image>'",
    "conda": "Try: 'conda activate <env>', 'conda list'",
    "help": "Shows a list of available commands.",
    "~ai": "Opens the AI feature configuration panel.",
    "exit": "Exits PyShell."
}

# Subcommand and syntax hints for commands with sub-features
SUBCOMMAND_HINTS = {
    "git": [
        ("status", "git status"),
        ("add", "git add <file>"),
        ("commit", 'git commit -m "<message>"'),
        ("push", "git push"),
        ("pull", "git pull"),
        ("branch", "git branch"),
        ("checkout", "git checkout <branch>"),
        ("merge", "git merge <branch>")
    ],
    "pip": [
        ("install", "pip install <package>"),
        ("uninstall", "pip uninstall <package>"),
        ("freeze", "pip freeze > requirements.txt")
    ],
    # Add more subcommand hints as needed
}

def get_live_suggestion(text: str, commands_dict: dict, command_args: dict) -> str:
    """Generates a live suggestion with syntax based on all available CLI commands."""
    if not text.strip():
        return "💡 Tip: Type a command or '~ai' for options."

    words = text.split()
    if not words:
        return ""
        
    command = words[0].lower()
    rest = words[1:] if len(words) > 1 else []

    # If the command is a known subcommand group (like git)
    if command in SUBCOMMAND_HINTS:
        if not rest:
            # Show all subcommands
            subcmds = [f"{name} ({syntax})" for name, syntax in SUBCOMMAND_HINTS[command]]
            return f"💡 Subcommands: {html.escape(', '.join(subcmds))}"
        else:
            # Suggest subcommands that match the next word
            sub = rest[0].lower()
            matches = [syntax for name, syntax in SUBCOMMAND_HINTS[command] if name.startswith(sub)]
            if matches:
                return f"💡 Did you mean: {html.escape(', '.join(matches))}?"

    if command in commands_dict:
        if command in command_args:
            syntax = " ".join(command_args[command])
            return f"✅ Usage: {command} {html.escape(syntax)}"
        else:
            return f"✅ Command '{command}' is valid. Press Enter to execute."

    # Check for partial command matches from the full command list
    possible_matches = [cmd for cmd in commands_dict if cmd.startswith(command)]
    if possible_matches:
        # Suggest the first few matches
        suggestions = ", ".join(possible_matches[:3])
        return f"💡 Did you mean: {suggestions}?"
    
    return "" # Return empty string if no specific hint

def run():
    history_path = os.path.join(os.path.dirname(__file__), '..', 'history.json')
    try:
        with open(history_path, 'r') as f:
            history = json.load(f)
    except Exception:
        history = {}
    recent = history.get('commands', [])[-1] if history.get('commands') else ''
    # Simple rule-based suggestion
    if 'git status' in recent:
        suggestion = 'git add .'
    elif 'ls' in recent:
        suggestion = 'cd <folder>'
    else:
        suggestion = 'echo Hello World'
    print(f"\n💡 Based on '{recent}', try: {suggestion}") 