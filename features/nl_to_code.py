from local_llm_client import run_llama_prompt
import os

def run():
    instruction = input("\n💬 Describe your task: ")
    prompt = f"Convert this to a shell command:\nInstruction: {instruction}\nCommand:"
    command = run_llama_prompt(prompt)
    if command:
        print(f"\n🧠 Suggested Command: {command}")
        if input("Run it? (y/n): ").lower().startswith("y"):
            os.system(command)
    else:
        print("\nCould not generate a command.") 