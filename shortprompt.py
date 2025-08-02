import google.generativeai as genai
import questionary
from rich.console import Console
from rich.panel import Panel
import os

api_key = os.getenv("PROMPT_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
console = Console()


class ShortPrompt:
    def get_subtopics(self, keyword):
        prompt = f"""
You are an assistant. Given a keyword or topic: "{keyword}", generate a list of 5-7 most relevant subtopics that a user might be interested in.
Only return the list in numbered format without extra explanation.
"""
        response = model.generate_content(prompt)
        return [line.split(".", 1)[1].strip() for line in response.text.strip().splitlines() if "." in line]

    def get_content(self, keyword, chosen_subtopic):
        prompt = f"""
Generate a detailed explanation for the topic: "{keyword}" with focus on the subtopic: "{chosen_subtopic}".
Make it beginner-friendly and well-structured in points or paragraphs.
"""
        response = model.generate_content(prompt)
        return response.text.strip()

    def run(self):
        console.rule("[bold green]Prompt Assistant[/]")
        keyword = questionary.text("Enter your keyword(s):").ask().strip()

        console.print("\n[cyan]Generating subtopics...[/]\n")
        subtopics = self.get_subtopics(keyword)

        selected_subtopic = questionary.select(
            "Choose a subtopic:",
            choices=subtopics
        ).ask()

        console.print("\n[yellow]Generating content. Please wait...[/]\n")
        output = self.get_content(keyword, selected_subtopic)

        console.rule("[bold magenta]Generated Output[/]")
        console.print(Panel.fit(
            f"[bold cyan]Topic:[/] {keyword}\n[bold cyan]Subtopic:[/] {selected_subtopic}\n\n{output}",
            border_style="blue",
            title="Prompt Assistant",
            padding=(1, 2)
        ))
