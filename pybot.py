from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text


class PyBotChat:
    def __init__(self, name='PyBot'):
        self.console = Console()
        self.chatbot = self._create_chatbot(name)
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)

    def _create_chatbot(self, name):
        """Initialize the ChatBot with desired settings."""
        return ChatBot(
            name,
            logic_adapters=['chatterbot.logic.BestMatch'],
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///database.sqlite3'
        )

    def train_bot(self):
        """Train the chatbot using ChatterBot's English corpus."""
        self.console.print("[bold green]Training the chatbot...[/bold green]")
        self.trainer.train("chatterbot.corpus.english")
        self.console.print("[bold green]Training complete![/bold green]\n")

    def greet_user(self):
        """Print welcome message."""
        self.console.print(
            Panel(
                "🤖 [bold green]Welcome to PyBot![/bold green]\nType [bold yellow]'exit'[/bold yellow] to end the chat.",
                title="PyBot Chat",
                expand=False
            )
        )

    def chat_loop(self):
        chat_app = PyBotChat()
        chat_app.train_bot()
        chat_app.greet_user()
        """Start the user interaction loop."""
        while True:
            user_input = Prompt.ask("[bold blue]👤 You")
            if user_input.lower() in ['exit', 'quit']:
                break
            response = self.chatbot.get_response(user_input)
            self.console.print(Text("🤖 PyBot: ", style="bold magenta") + Text(str(response), style="white"))
            self.console.print()
