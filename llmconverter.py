import openai
import json
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  

def few_shot_examples(file_path='prompt_templates.json'):
    try:
        with open(file_path, 'r') as f:
            examples = json.load(f)
        return examples
    except FileNotFoundError:
        print('Few-shot examples file not found.')
        return []

def build_prompt(user_input, examples):
    msgs = []

    msgs.append({
        "role": "system",
        "content": "You are a helpful assistant that converts natural language into safe and efficient Linux shell commands. Only return the command—no explanations."
    })

    for ex in examples:
        msgs.append({"role": "user", "content": ex["input"]})
        msgs.append({"role": "assistant", "content": ex["output"]})

    msgs.append({
        "role": "user",
        "content": user_input
    })

    return msgs  


def generate_command(user_input):
    examples = few_shot_examples()
    messages = build_prompt(user_input, examples)
    
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4', 
            messages=messages,
            max_tokens=100,
            temperature=0.2
        )
        return response

    except Exception as e:
        print("Command generation failed:", e)
        return 'Error generating command.'

if __name__ == "__main__":
    while True:
        query = input("Enter your natural language (or 'exit'): ")
        if query.lower() == "exit":
            break
        result = generate_command(query)
        print("Generated shell command:", result)