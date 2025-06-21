from local_llm_client import run_llama_prompt
import sys

def run():
    print("\n🧹 Paste your code below (CTRL+D to end):")
    code = sys.stdin.read()
    prompt = f"Refactor this code for better readability and performance:\n{code}"
    result = run_llama_prompt(prompt)
    print("\n🔧 Refactored Code:\n")
    print(result) 