from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
import os, shutil, math, threading, socket, requests
import cmd, subprocess
from termcolor import colored
import pyfiglet


class PyShell(cmd.Cmd):
    intro = colored("Welcome to PyShell! Type 'help' or 'chabot' to start.\n", "cyan")
    prompt = colored("PyShell ", "blue")

    def show_poster(self):
        poster = pyfiglet.figlet_format("PyShell")
        print(colored(poster, "blue"))
        print(colored("A Python Shell with Chatbot Features", "cyan"))

    def list_files(self):
        print(colored("\nFiles and Directories:", "yellow"))
        for item in os.listdir():
            print(f" - {item}")

    def run_command(self, command=None):
        if not command:
            command = prompt("Enter command: ")
        try:
            output = subprocess.run(command, shell=True, check=True, text=True)
            print(colored(output.stdout, "white"))
        except subprocess.CalledProcessError as e:
            print(colored(f"Command failed: {e}", "red"))

    def run_python_code(self):
        code = prompt("Enter Python code: ")
        try:
            exec(code)
        except Exception as e:
            print(colored(f"Error: {e}", "red"))

    def exit_shell(self):
        print(colored("Exiting PyShell. Goodbye!", "cyan"))
        return True

    def make_directory(self, dir_name):
        try:
            os.makedirs(dir_name)
            print(colored(f"Directory '{dir_name}' created successfully.", "green"))
        except FileExistsError:
            print(colored(f"Directory '{dir_name}' already exists.", "red"))

    def chat_with_terminal(self):
        while True:
            print(colored("\nPyShell Chatbot: How can I help you today? Type 'exit' to quit.", "green"))
            user_input = prompt("You: ").strip().lower()

            if user_input == 'exit':
                break
            elif user_input == 'python':
                self.run_python_code()
            elif user_input in ['help']:
                print(colored(
                    """Commands you can try:
                - ls / dir / show files     : List files
                - delete file               : Delete a file
                - python                    : Run Python code
                - any system cmd            : Try ls, mkdir, etc.
                - exit / quit               : Close PyBot
                """, "yellow"))
            elif user_input in ['ls', 'dir', 'show files']:
                self.list_files()
            elif user_input == 'delete file':
                file_name = prompt("Enter the file name to delete: ")
                if os.path.isfile(file_name):
                    os.remove(file_name)
                    print(colored(f"File '{file_name}' deleted successfully.", "green"))
                else:
                    print(colored(f"File '{file_name}' does not exist.", "red"))
            else:
                self.run_command(user_input)

    def do_chabot(self, arg):
        """Start the PyShell Chatbot"""
        self.show_poster()
        self.chat_with_terminal()

    def do_ls(self, arg):
        """List current directory contents"""
        self.list_files()

    def do_mkdir(self, arg):
        """Create a new directory: mkdir dirname"""
        if not arg:
            print(colored("Usage: mkdir <dirname>", "red"))
        else:
            self.make_directory(arg)

    def do_exit(self, arg):
        """Exit the PyShell"""
        return self.exit_shell()

    def default(self, line):
        """Handle unknown commands as shell commands"""
        self.run_command(line)


if __name__ == '__main__':
    shell = PyShell()
    shell.show_poster()
    shell.cmdloop()
