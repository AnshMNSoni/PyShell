from local_llm_client import run_llama_prompt

def run():
    topic = input("\n🔍 What code snippet are you looking for? ")
    prompt = f"Give a Python snippet to: {topic}"
    snippet = run_llama_prompt(prompt)
    print(f"\n📚 Snippet:\n{snippet}") 