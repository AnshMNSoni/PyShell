import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
from probes import *

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.face_up = True
    
    def get_value(self):
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11  # Ace is initially 11, can be adjusted to 1 if needed
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            # Rebuild deck if empty
            self.build()
            return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += card.get_value()
        
        # Track aces
        if card.rank == "A":
            self.aces += 1
        
        # Adjust for aces if busting
        self.adjust_for_ace()
    
    def adjust_for_ace(self):
        # Convert ace from 11 to 1 if would bust
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1
    
    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

class Player:
    def __init__(self, name, bankroll=1000):
        self.name = name
        self.bankroll = bankroll
        self.hands = [Hand()]  # Support for splitting
    
    def place_bet(self, amount):
        if amount > self.bankroll:
            return False
        self.bankroll -= amount
        return True
    
    def add_winnings(self, amount):
        self.bankroll += amount

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt, min_value=1, max_value=None):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.configure(bg=DARK_COLOR)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Position dialog in center of parent
        x = parent.winfo_x() + parent.winfo_width() // 2 - 150
        y = parent.winfo_y() + parent.winfo_height() // 2 - 75
        self.geometry(f"300x150+{x}+{y}")
        
        # Create widgets
        frame = tk.Frame(self, bg=DARK_COLOR, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        prompt_label = tk.Label(
            frame, 
            text=prompt, 
            font=("Helvetica", 12),
            bg=DARK_COLOR,
            fg=LIGHT_COLOR,
            wraplength=260
        )
        prompt_label.pack(pady=(0, 10))
        
        self.entry = ttk.Entry(frame, font=("Helvetica", 12), width=15)
        self.entry.pack(pady=5)
        self.entry.focus_set()
        
        button_frame = tk.Frame(frame, bg=DARK_COLOR)
        button_frame.pack(pady=10)
        
        ok_button = ttk.Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Store validation values
        self.min_value = min_value
        self.max_value = max_value
        
        # Bind events
        self.bind("<Return>", lambda event: self.on_ok())
        self.bind("<Escape>", lambda event: self.on_cancel())
        
        # Wait for window to be destroyed
        self.wait_window()
    
    def on_ok(self):
        try:
            value = int(self.entry.get())
            if self.min_value is not None and value < self.min_value:
                messagebox.showerror("Error", f"Value must be at least {self.min_value}")
                return
            if self.max_value is not None and value > self.max_value:
                messagebox.showerror("Error", f"Value cannot exceed {self.max_value}")
                return
            self.result = value
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def on_cancel(self):
        self.result = None
        self.destroy()