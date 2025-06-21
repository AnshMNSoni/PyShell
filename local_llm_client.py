from llama_cpp import Llama, CreateCompletionResponse
from rich.console import Console
import typing

console = Console()

# The model path provided by the user
MODEL_PATH = "C:/Users/Prince Patel/models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

_llm_cache = None

def get_llama_client():
    """Initializes and returns the Llama client, caching it for the session."""
    global _llm_cache
    if _llm_cache is None:
        try:
            console.print(f"[bold yellow]Loading model from: {MODEL_PATH}...[/bold yellow]")
            _llm_cache = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)
            console.print("[bold green]Model loaded successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error loading model: {e}[/bold red]")
            _llm_cache = None
    return _llm_cache

def run_llama_prompt(prompt: str, max_tokens=512, temperature=0.7) -> str:
    """Runs a prompt against the local LLM and returns the text response."""
    llm = get_llama_client()
    if not llm:
        return "Local model is not available."

    try:
        response = llm(prompt, max_tokens=max_tokens, temperature=temperature, stream=False)
        # We expect a dictionary, so we assert the type to satisfy the linter
        response_dict = typing.cast(CreateCompletionResponse, response)
        if response_dict and 'choices' in response_dict and response_dict['choices']:
            return response_dict['choices'][0]['text'].strip()
        return "Failed to get a valid response from the model."
    except Exception as e:
        console.print(f"[bold red]Error during model inference: {e}[/bold red]")
        return "An error occurred while generating a response." 