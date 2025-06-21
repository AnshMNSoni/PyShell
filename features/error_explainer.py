from local_llm_client import run_llama_prompt

def run():
    error = input("\n❌ Paste the error message: ")
    prompt = f"Explain and fix this error:\n{error}"
    explanation = run_llama_prompt(prompt)
    print(f"\n🛠️ Explanation:\n{explanation}") 