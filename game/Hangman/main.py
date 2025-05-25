import random
import tkinter as tk
from tkinter import messagebox
from words import word_list

# Hangman stages
stages = [
    """
    +---+
    |   |
        |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    =========
    """
]

class HangmanGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Hangman Game")
        self.window.geometry("400x500")
        self.window.config(bg="lightblue")


        self.any_letter = random.choice(word_list)
        self.display_word = ["_"] * len(self.any_letter)
        self.count = 0
        self.guessed_letters = set()


        self.display_stage()
        self.create_widgets()


    def display_stage(self):
        self.canvas = tk.Canvas(self.window, width=200, height=200, bg="white")
        self.canvas.create_text(100, 100, text=stages[self.count], font=("Courier", 14))
        self.canvas.pack(pady=10)


    def update_stage(self):
        self.canvas.delete("all")
        self.canvas.create_text(100, 100, text=stages[self.count], font=("Courier", 14))


    def create_widgets(self):
        self.word_label = tk.Label(self.window, text=" ".join(self.display_word), font=("Courier", 20, 'bold'), bg="lightblue")
        self.word_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.window, font=("Courier", 15, 'bold'), width=5)
        self.guess_entry.pack(pady=10)

        self.submit_button = tk.Button(self.window, text="Guess", command=self.guess_letter, font=('Times-New-Roman', 15, 'bold'), bg='brown', fg='white',bd=6)
        self.submit_button.pack(pady=5)

        self.message_label = tk.Label(self.window, text="", font=("Times-New-Roman", 12, 'italic'), bg="lightblue", fg="black")
        self.message_label.pack(pady=10)

        self.reset_button = tk.Button(self.window, text="Reset Game", command=self.reset_game, font=('Times-New-Roman', 15, 'bold'), bg='brown', fg='white', bd=6)
        self.reset_button.pack(pady=10)


    def guess_letter(self):
        guess = self.guess_entry.get().lower()
        
        if guess == "":
            messagebox.showwarning(title="Empty Space Found!", message="Please enter the character!")
            return
        
        if guess in self.guessed_letters:
            self.message_label.config(text=f"You've already guessed '{guess}'. Try another letter.")
            self.guess_entry.delete(0, tk.END)
            return

        self.guessed_letters.add(guess)
        self.guess_entry.delete(0, tk.END)

        # Check if guess is correct
        if guess in self.any_letter:
            for i, letter in enumerate(self.any_letter):
                if letter == guess:
                    self.display_word[i] = guess
            self.word_label.config(text=" ".join(self.display_word))
            self.message_label.config(text=f"Good job! '{guess}' is in the word.")

            if "_" not in self.display_word:
                self.message_label.config(text="Congratulations! You've won!")
                messagebox.showinfo("Hangman", "You win!")
        else:
            self.count += 1
            self.update_stage()
            self.message_label.config(text=f"Oops! '{guess}' is not in the word. You lost a life.")

            if self.count == len(stages) - 1:
                self.message_label.config(text=f"Game Over! The word was '{self.any_letter}'.")
                messagebox.showinfo("Hangman", f"You lose! The word was '{self.any_letter}'.")

    def reset_game(self):
        self.any_letter = random.choice(word_list)
        self.display_word = ["_"] * len(self.any_letter)
        self.count = 0
        self.guessed_letters.clear()

        self.word_label.config(text=" ".join(self.display_word))
        self.message_label.config(text="")
        self.update_stage()

# Main application loop
if __name__ == "__main__":
    window = tk.Tk()
    game = HangmanGame(window)
    window.mainloop()