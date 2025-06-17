import random
from datetime import datetime

def simple_chatbot():
    greetings = [
        "Hello! How can I help you?",
        "Hi there! What can I do for you today?",
        "Hey! Need any assistance?",
        "Greetings! How may I assist you?"
    ]
    farewells = [
        "Goodbye! Have a great day!",
        "See you later!",
        "Bye! Take care!",
        "Farewell!"
    ]
    help_text = (
        "You can try asking things like:\n"
        "- hello\n"
        "- what time is it?\n"
        "- what is your name?\n"
        "- help\n"
        "- exit\n"
    )
    print("Welcome to the Terminal Chatbot! Type 'help' for options or 'exit' to quit.")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            print(f"Bot: {random.choice(farewells)}")
            break
        elif "hello" in user_input or "hi" in user_input or "hey" in user_input:
            print(f"Bot: {random.choice(greetings)}")
        elif "time" in user_input:
            print(f"Bot: The current time is {datetime.now().strftime('%H:%M:%S')}")
        elif "name" in user_input:
            print("Bot: I'm PyShellBot, your terminal assistant!")
        elif "help" in user_input:
            print(f"Bot: {help_text}")
        else:
            print("Bot: Sorry, I don't understand. Try asking something else or type 'help'.")

if __name__ == "__main__":
    simple_chatbot()
