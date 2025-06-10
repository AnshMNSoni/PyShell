import tkinter as tk
from tkinter import ttk, messagebox, font
import pyttsx3
import random
import pygame
from questions import get_questions

class KBCGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kaun Banega Karodpati (KBC)")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Initialize pygame mixer for sounds
        pygame.mixer.init()
        
        # Load sounds
        self.sound_enabled = True
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

        # Initialize sounds as TTS messages
        self.sounds = {}
        self.load_sound("correct", "Sahi Jawab!")
        self.load_sound("wrong", "Galat Jawab!")
        self.load_sound("timer", "Time is running out!")
        self.load_sound("lifeline", "Lifeline used.")
        self.load_sound("applause", "Congratulations!")
        self.load_sound("intro", "Welcome to KBC!")
        
        # Set monochromatic color scheme
        self.colors = {
            "bg_dark": "#1a1a1a",
            "bg_medium": "#2a2a2a",
            "bg_light": "#3a3a3a",
            "text_light": "#e0e0e0",
            "text_highlight": "#ffffff",
            "accent": "#808080",
            "button": "#4a4a4a",
            "button_hover": "#5a5a5a",
            "correct": "#a0a0a0",
            "wrong": "#505050",
            "timer_normal": "#808080",
            "timer_warning": "#a0a0a0",
            "timer_danger": "#c0c0c0"
        }
        
        # Game variables
        self.amount = 0
        self.lifeline_1 = 0  # 50/50
        self.lifeline_2 = 0  # Hint
        self.current_question = 0
        self.timer_running = False
        self.timer_value = 0
        self.timer_thread = None
        self.timer_id = None
        self.sound_enabled = True
        
        # Get all questions and prepare game questions
        self.all_questions = get_questions()
        self.game_questions = []
        
        # Create custom fonts
        self.update_fonts()
        
        # Create frames
        self.create_frames()
        
        # Bind window resize event
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Start with welcome screen
        self.play_sound("intro")
        self.show_welcome_screen()
    
    def load_sound(self, sound_name, text):
        """Store TTS text for a given sound name"""
        self.sounds[sound_name] = text

    
    def play_sound(self, sound_name):
        """Speak a sound phrase by name using pyttsx3"""
        if not self.sound_enabled:
            return

        message = self.sounds.get(sound_name)
        if message:
            self.engine.say(message)
            self.engine.runAndWait()

    
    def stop_sound(self, sound_name=None):
        """Stop a specific sound or all sounds"""
        if sound_name:
            if sound_name == "background":
                pygame.mixer.Channel(0).stop()
            else:
                pygame.mixer.Channel(1).stop()
        else:
            pygame.mixer.stop()
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            self.stop_sound()
        
        # Update sound button text
        for widget in self.footer_frame.winfo_children():
            if hasattr(widget, 'sound_button') and widget.sound_button:
                widget.config(text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF")
    
    def update_fonts(self):
        """Update fonts based on window size"""
        # Get window dimensions
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Base size on the smaller dimension
        base_size = min(width, height) // 40
        
        # Ensure minimum sizes
        title_size = max(12, base_size * 2)
        question_size = max(10, int(base_size * 1.5))
        option_size = max(8, base_size)
        info_size = max(8, int(base_size * 0.8))
        
        # Create fonts
        self.title_font = font.Font(family="Helvetica", size=title_size, weight="bold")
        self.question_font = font.Font(family="Helvetica", size=question_size, weight="bold")
        self.option_font = font.Font(family="Helvetica", size=option_size)
        self.info_font = font.Font(family="Helvetica", size=info_size)
        self.timer_font = font.Font(family="Helvetica", size=question_size * 2, weight="bold")
    
    def on_window_resize(self, event):
        """Handle window resize event"""
        # Only respond to root window resizing, not child widgets
        if event.widget == self.root:
            # Update fonts
            self.update_fonts()
            
            # Update UI elements if needed
            if hasattr(self, 'current_screen'):
                if self.current_screen == "welcome":
                    self.show_welcome_screen()
                elif self.current_screen == "rules":
                    self.show_rules_screen()
                elif self.current_screen == "game":
                    # Redisplay current question without resetting timer
                    self.redisplay_current_question()
    
    def redisplay_current_question(self):
        """Redisplay the current question without resetting the timer"""
        # Save current timer value
        current_timer = self.timer_value
        
        # Clear frames
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.lifelines_frame.winfo_children():
            widget.destroy()
        for widget in self.footer_frame.winfo_children():
            widget.destroy()
        
        # Get current question data
        q_data = self.game_questions[self.current_question]
        
        # Header - Question number and amount
        question_num_label = tk.Label(
            self.header_frame,
            text=f"Question {self.current_question + 1} of ${q_data['value']}",
            font=self.question_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_highlight"]
        )
        question_num_label.pack(side=tk.LEFT, padx=10)
        
        amount_label = tk.Label(
            self.header_frame,
            text=f"Current: ${self.amount}",
            font=self.question_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        amount_label.pack(side=tk.RIGHT, padx=10)
        
        # Timer display
        self.timer_canvas = tk.Canvas(
            self.header_frame, 
            width=60, 
            height=60, 
            bg=self.colors["bg_medium"],
            highlightthickness=0
        )
        self.timer_canvas.pack(side=tk.RIGHT, padx=10)
        
        # Draw timer circle
        self.timer_circle = self.timer_canvas.create_oval(5, 5, 55, 55, outline=self.colors["timer_normal"], width=3)
        
        # Timer text
        self.timer_text = self.timer_canvas.create_text(30, 30, text=str(current_timer), fill=self.colors["text_highlight"], font=self.info_font)
        
        # Question
        question_label = tk.Label(
            self.question_frame,
            text=q_data["question"],
            font=self.question_font,
            bg=self.colors["bg_light"],
            fg=self.colors["text_highlight"],
            wraplength=self.root.winfo_width() - 100,  # Responsive wrapping
            justify=tk.CENTER,
            pady=20
        )
        question_label.pack(fill=tk.BOTH, expand=True)
        
        # Options
        option_letters = ['a', 'b', 'c', 'd']
        self.option_buttons = []
        
        for i, option in enumerate(q_data["options"]):
            option_frame = tk.Frame(self.options_frame, bg=self.colors["bg_medium"])
            option_frame.pack(fill=tk.X, padx=20, pady=5)
            
            option_button = tk.Button(
                option_frame,
                text=f"{option_letters[i]}) {option}",
                font=self.option_font,
                bg=self.colors["button"],
                fg=self.colors["text_light"],
                activebackground=self.colors["button_hover"],
                activeforeground=self.colors["text_highlight"],
                relief=tk.RAISED,
                width=50,
                height=2,
                anchor=tk.W,
                padx=20,
                command=lambda opt=option: self.check_answer(opt)
            )
            option_button.pack(fill=tk.X)
            self.option_buttons.append(option_button)
        
        # Lifelines
        lifeline_label = tk.Label(
            self.lifelines_frame,
            text="Lifelines:",
            font=self.info_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        lifeline_label.pack(side=tk.LEFT, padx=10)
        
        fifty_fifty_button = tk.Button(
            self.lifelines_frame,
            text="50:50",
            font=self.info_font,
            bg=self.colors["button"] if self.lifeline_1 == 0 else self.colors["bg_dark"],
            fg=self.colors["text_light"],
            state=tk.NORMAL if self.lifeline_1 == 0 else tk.DISABLED,
            command=self.use_fifty_fifty
        )
        fifty_fifty_button.pack(side=tk.LEFT, padx=10)
        
        hint_button = tk.Button(
            self.lifelines_frame,
            text="Hint",
            font=self.info_font,
            bg=self.colors["button"] if self.lifeline_2 == 0 else self.colors["bg_dark"],
            fg=self.colors["text_light"],
            state=tk.NORMAL if self.lifeline_2 == 0 else tk.DISABLED,
            command=self.use_hint
        )
        hint_button.pack(side=tk.LEFT, padx=10)
        
        # Sound toggle button
        sound_button = tk.Button(
            self.footer_frame,
            text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF",
            font=self.info_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            command=self.toggle_sound
        )
        sound_button.sound_button = True  # Mark this as the sound button
        sound_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Warning for questions 6 and 7
        if self.current_question >= 5:  # 0-indexed, so 5 is question 6
            penalty = q_data.get("penalty", 0)
            warning_label = tk.Label(
                self.footer_frame,
                text=f"Warning: Wrong answer will deduct ${penalty} from your winnings!",
                font=self.info_font,
                bg=self.colors["bg_medium"],
                fg=self.colors["wrong"]
            )
            warning_label.pack(side=tk.RIGHT, pady=5, padx=10)
    
    def create_frames(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg_dark"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Welcome frame
        self.welcome_frame = tk.Frame(self.main_frame, bg=self.colors["bg_medium"])
        
        # Rules frame
        self.rules_frame = tk.Frame(self.main_frame, bg=self.colors["bg_medium"])
        
        # Game frame
        self.game_frame = tk.Frame(self.main_frame, bg=self.colors["bg_medium"])
        
        # Header frame (inside game frame)
        self.header_frame = tk.Frame(self.game_frame, bg=self.colors["bg_medium"])
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Question frame (inside game frame)
        self.question_frame = tk.Frame(self.game_frame, bg=self.colors["bg_light"], padx=20, pady=20)
        self.question_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Options frame (inside game frame)
        self.options_frame = tk.Frame(self.game_frame, bg=self.colors["bg_medium"])
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lifelines frame (inside game frame)
        self.lifelines_frame = tk.Frame(self.game_frame, bg=self.colors["bg_medium"])
        self.lifelines_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Footer frame (inside game frame)
        self.footer_frame = tk.Frame(self.game_frame, bg=self.colors["bg_medium"])
        self.footer_frame.pack(fill=tk.X, padx=10, pady=10)
    
    def prepare_game_questions(self):
        """Prepare a set of 7 randomized questions with increasing difficulty"""
        # Group questions by value
        questions_by_value = {}
        for q in self.all_questions:
            value = q["value"]
            if value not in questions_by_value:
                questions_by_value[value] = []
            questions_by_value[value].append(q)
        
        # Select questions for each value level
        self.game_questions = []
        
        # First 5 questions (no penalty)
        for value in [1000, 2000, 3000, 4000, 5000]:
            if value in questions_by_value and questions_by_value[value]:
                question = random.choice(questions_by_value[value])
                self.game_questions.append(question)
                questions_by_value[value].remove(question)
            else:
                # Fallback if we don't have enough questions at this value
                fallback_question = random.choice(self.all_questions)
                fallback_question["value"] = value
                self.game_questions.append(fallback_question)
        
        # Last 2 questions (with penalty)
        for value in [6000, 7000]:
            penalty_questions = [q for q in self.all_questions if q.get("value") == value and "penalty" in q]
            if penalty_questions:
                question = random.choice(penalty_questions)
                self.game_questions.append(question)
            else:
                # Fallback if we don't have enough penalty questions
                fallback_question = random.choice([q for q in self.all_questions if q.get("value") >= 5000])
                fallback_question["value"] = value
                fallback_question["penalty"] = 1000 if value == 6000 else 2000
                self.game_questions.append(fallback_question)
        
        # Ensure we have exactly 7 questions
        while len(self.game_questions) < 7:
            fallback_question = random.choice(self.all_questions)
            self.game_questions.append(fallback_question)
        
        # Trim to 7 questions if we somehow have more
        self.game_questions = self.game_questions[:7]
        
        # Sort by value to ensure proper order
        self.game_questions.sort(key=lambda x: x["value"])
        
        # Add timer values based on difficulty
        for i, q in enumerate(self.game_questions):
            # Easier questions get more time
            if i < 2:  # Questions 1-2
                q["timer"] = 30
            elif i < 4:  # Questions 3-4
                q["timer"] = 25
            elif i < 6:  # Questions 5-6
                q["timer"] = 20
            else:  # Question 7
                q["timer"] = 15
    
    def show_welcome_screen(self):
        self.current_screen = "welcome"
        
        # Stop any running timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Hide other frames
        self.rules_frame.pack_forget()
        self.game_frame.pack_forget()
        
        # Clear and show welcome frame
        for widget in self.welcome_frame.winfo_children():
            widget.destroy()
        
        self.welcome_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            self.welcome_frame, 
            text="Kaun Banega Karodpati (KBC)",
            font=self.title_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_highlight"],
            pady=20
        )
        title_label.pack(fill=tk.X)
        
        # Logo or image placeholder
        logo_frame = tk.Frame(self.welcome_frame, bg=self.colors["bg_light"], height=200)
        logo_frame.pack(fill=tk.X, padx=50, pady=20)
        
        logo_label = tk.Label(
            logo_frame, 
            text="KBC",
            font=font.Font(family="Helvetica", size=48, weight="bold"),
            bg=self.colors["bg_light"],
            fg=self.colors["text_highlight"],
            height=4
        )
        logo_label.pack(fill=tk.BOTH, expand=True)
        
        # Start button
        start_button = tk.Button(
            self.welcome_frame,
            text="Start Game",
            font=self.question_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            activebackground=self.colors["button_hover"],
            activeforeground=self.colors["text_highlight"],
            padx=20,
            pady=10,
            relief=tk.RAISED,
            command=self.show_rules_screen
        )
        start_button.pack(pady=30)
        
        # Question count info
        question_count_label = tk.Label(
            self.welcome_frame,
            text=f"Game includes {len(self.all_questions)} unique questions!",
            font=self.info_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        question_count_label.pack(pady=10)
        
        # Sound toggle button
        sound_button = tk.Button(
            self.welcome_frame,
            text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF",
            font=self.info_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            command=self.toggle_sound
        )
        sound_button.pack(pady=10)
    
    def show_rules_screen(self):
        self.current_screen = "rules"
        
        # Stop intro music and start background music
        self.stop_sound("intro")
        
        # Hide other frames
        self.welcome_frame.pack_forget()
        self.game_frame.pack_forget()
        
        # Clear and show rules frame
        for widget in self.rules_frame.winfo_children():
            widget.destroy()
        
        self.rules_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            self.rules_frame, 
            text="Rules and Information",
            font=self.title_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_highlight"],
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Rules text
        rules_text = tk.Text(
            self.rules_frame,
            font=self.info_font,
            bg=self.colors["bg_light"],
            fg=self.colors["text_light"],
            relief=tk.FLAT,
            height=15,
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        rules_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        rules = """
Please Read the Rules and Information carefully

:: Rules and Information ::

-> Total 2 Lifelines
-> Questions are randomly selected from a pool of over 50 unique questions
-> Each question has a time limit! If time runs out, it counts as a wrong answer
-> Easier questions have more time (30 seconds) while harder ones have less (15 seconds)
-> To each Question their are 4 options

-> Lifeline-1 = (50/50) means out of 4 options 2 options filter out
-> Lifeline-2 = (Hint) means Some Hint will given regarding correct answer

-> You can use each lifeline for single time
-> You can't use both lifeline in a single question

-> Best of luck!
        """
        
        rules_text.insert(tk.END, rules)
        rules_text.config(state=tk.DISABLED)
        
        # Start game button
        start_button = tk.Button(
            self.rules_frame,
            text="Let's Play!",
            font=self.question_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            activebackground=self.colors["button_hover"],
            activeforeground=self.colors["text_highlight"],
            padx=20,
            pady=10,
            relief=tk.RAISED,
            command=self.start_game
        )
        start_button.pack(pady=20)
        
        # Sound toggle button
        sound_button = tk.Button(
            self.rules_frame,
            text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF",
            font=self.info_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            command=self.toggle_sound
        )
        sound_button.pack(pady=10)
    
    def start_game(self):
        self.current_screen = "game"
        
        # Reset game variables
        self.amount = 0
        self.lifeline_1 = 0
        self.lifeline_2 = 0
        self.current_question = 0
        
        # Prepare random questions for this game
        self.prepare_game_questions()
        
        # Hide other frames
        self.welcome_frame.pack_forget()
        self.rules_frame.pack_forget()
        
        # Show game frame
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start countdown
        self.countdown_to_question(5)
    
    def countdown_to_question(self, seconds):
        # Clear frames
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.lifelines_frame.winfo_children():
            widget.destroy()
        for widget in self.footer_frame.winfo_children():
            widget.destroy()
        
        # Show countdown
        countdown_label = tk.Label(
            self.question_frame,
            text=f"Get Ready! Starting in {seconds}...",
            font=self.title_font,
            bg=self.colors["bg_light"],
            fg=self.colors["text_highlight"]
        )
        countdown_label.pack(fill=tk.BOTH, expand=True)
        
        if seconds > 0:
            self.timer_id = self.root.after(1000, lambda: self.countdown_to_question(seconds - 1))
        else:
            self.display_question()
    
    def display_question(self):
        # Clear frames
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.lifelines_frame.winfo_children():
            widget.destroy()
        for widget in self.footer_frame.winfo_children():
            widget.destroy()
        
        # Get current question data
        q_data = self.game_questions[self.current_question]
        
        # Header - Question number and amount
        question_num_label = tk.Label(
            self.header_frame,
            text=f"Question {self.current_question + 1} of ${q_data['value']}",
            font=self.question_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_highlight"]
        )
        question_num_label.pack(side=tk.LEFT, padx=10)
        
        amount_label = tk.Label(
            self.header_frame,
            text=f"Current: ${self.amount}",
            font=self.question_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        amount_label.pack(side=tk.RIGHT, padx=10)
        
        # Timer display
        self.timer_canvas = tk.Canvas(
            self.header_frame, 
            width=60, 
            height=60, 
            bg=self.colors["bg_medium"],
            highlightthickness=0
        )
        self.timer_canvas.pack(side=tk.RIGHT, padx=10)
        
        # Draw timer circle
        self.timer_circle = self.timer_canvas.create_oval(5, 5, 55, 55, outline=self.colors["timer_normal"], width=3)
        
        # Timer text
        self.timer_text = self.timer_canvas.create_text(30, 30, text=str(q_data["timer"]), fill=self.colors["text_highlight"], font=self.info_font)
        
        # Question
        question_label = tk.Label(
            self.question_frame,
            text=q_data["question"],
            font=self.question_font,
            bg=self.colors["bg_light"],
            fg=self.colors["text_highlight"],
            wraplength=self.root.winfo_width() - 100,  # Responsive wrapping
            justify=tk.CENTER,
            pady=20
        )
        question_label.pack(fill=tk.BOTH, expand=True)
        
        # Options
        option_letters = ['a', 'b', 'c', 'd']
        self.option_buttons = []
        
        for i, option in enumerate(q_data["options"]):
            option_frame = tk.Frame(self.options_frame, bg=self.colors["bg_medium"])
            option_frame.pack(fill=tk.X, padx=20, pady=5)
            
            option_button = tk.Button(
                option_frame,
                text=f"{option_letters[i]}) {option}",
                font=self.option_font,
                bg=self.colors["button"],
                fg=self.colors["text_light"],
                activebackground=self.colors["button_hover"],
                activeforeground=self.colors["text_highlight"],
                relief=tk.RAISED,
                width=50,
                height=2,
                anchor=tk.W,
                padx=20,
                command=lambda opt=option: self.check_answer(opt)
            )
            option_button.pack(fill=tk.X)
            self.option_buttons.append(option_button)
        
        # Lifelines
        lifeline_label = tk.Label(
            self.lifelines_frame,
            text="Lifelines:",
            font=self.info_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        lifeline_label.pack(side=tk.LEFT, padx=10)
        
        fifty_fifty_button = tk.Button(
            self.lifelines_frame,
            text="50:50",
            font=self.info_font,
            bg=self.colors["button"] if self.lifeline_1 == 0 else self.colors["bg_dark"],
            fg=self.colors["text_light"],
            state=tk.NORMAL if self.lifeline_1 == 0 else tk.DISABLED,
            command=self.use_fifty_fifty
        )
        fifty_fifty_button.pack(side=tk.LEFT, padx=10)
        
        hint_button = tk.Button(
            self.lifelines_frame,
            text="Hint",
            font=self.info_font,
            bg=self.colors["button"] if self.lifeline_2 == 0 else self.colors["bg_dark"],
            fg=self.colors["text_light"],
            state=tk.NORMAL if self.lifeline_2 == 0 else tk.DISABLED,
            command=self.use_hint
        )
        hint_button.pack(side=tk.LEFT, padx=10)
        
        # Sound toggle button
        sound_button = tk.Button(
            self.footer_frame,
            text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF",
            font=self.info_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            command=self.toggle_sound
        )
        sound_button.sound_button = True  # Mark this as the sound button
        sound_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Warning for questions 6 and 7
        if self.current_question >= 5:  # 0-indexed, so 5 is question 6
            penalty = q_data.get("penalty", 0)
            warning_label = tk.Label(
                self.footer_frame,
                text=f"Warning: Wrong answer will deduct ${penalty} from your winnings!",
                font=self.info_font,
                bg=self.colors["bg_medium"],
                fg=self.colors["wrong"]
            )
            warning_label.pack(side=tk.RIGHT, pady=5, padx=10)
        
        # Start the timer
        self.timer_value = q_data["timer"]
        self.start_timer()
    
    def start_timer(self):
        """Start the question timer"""
        if self.timer_value > 0:
            # Update timer display
            self.timer_canvas.itemconfig(self.timer_text, text=str(self.timer_value))
            
            # Update timer color based on remaining time
            if self.timer_value <= 5:
                self.timer_canvas.itemconfig(self.timer_circle, outline=self.colors["timer_danger"])
                if self.timer_value <= 5 and self.sound_enabled:
                    self.play_sound("timer")
            elif self.timer_value <= 10:
                self.timer_canvas.itemconfig(self.timer_circle, outline=self.colors["timer_warning"])
            else:
                self.timer_canvas.itemconfig(self.timer_circle, outline=self.colors["timer_normal"])
            
            # Decrement timer and schedule next update
            self.timer_value -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            # Time's up - count as wrong answer
            self.stop_sound("timer")
            self.play_sound("wrong")
            self.show_wrong_answer(self.game_questions[self.current_question].get("penalty", 0))
    
    def use_fifty_fifty(self):
        if self.lifeline_1 == 1:
            return
        
        self.play_sound("lifeline")
        self.lifeline_1 = 1
        
        # Get current question data
        q_data = self.game_questions[self.current_question]
        correct_option = q_data["correct"]
        
        # Find the correct option index
        correct_index = -1
        for i, option in enumerate(q_data["options"]):
            if option == correct_option:
                correct_index = i
                break
        
        # Disable two incorrect options
        disabled_count = 0
        for i, button in enumerate(self.option_buttons):
            if i != correct_index and disabled_count < 2:
                button.config(state=tk.DISABLED, bg=self.colors["bg_dark"])
                disabled_count += 1
        
        # Update lifeline button
        for widget in self.lifelines_frame.winfo_children():
            if widget.cget("text") == "50:50":
                widget.config(bg=self.colors["bg_dark"], state=tk.DISABLED)
    
    def use_hint(self):
        if self.lifeline_2 == 1:
            return
        
        self.play_sound("lifeline")
        self.lifeline_2 = 1
        
        # Get current question data
        q_data = self.game_questions[self.current_question]
        hint_text = q_data["hint"]
        
        # Show hint in a messagebox
        messagebox.showinfo("Hint", hint_text)
        
        # Update lifeline button
        for widget in self.lifelines_frame.winfo_children():
            if widget.cget("text") == "Hint":
                widget.config(bg=self.colors["bg_dark"], state=tk.DISABLED)
    
    def check_answer(self, selected_option):
        # Cancel the timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Stop timer sound if playing
        self.stop_sound("timer")
        
        # Get current question data
        q_data = self.game_questions[self.current_question]
        correct_option = q_data["correct"]
        
        # Disable all option buttons
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
        
        # Highlight the selected option
        for button in self.option_buttons:
            if selected_option in button.cget("text"):
                if selected_option == correct_option:
                    button.config(bg=self.colors["correct"])
                else:
                    button.config(bg=self.colors["wrong"])
        
        # Check if answer is correct
        if selected_option == correct_option:
            self.play_sound("correct")
            self.show_correct_answer(q_data["value"])
        else:
            self.play_sound("wrong")
            self.show_wrong_answer(q_data.get("penalty", 0))
    
    def show_correct_answer(self, value):
        # Update amount
        self.amount += value
        
        # Show correct answer message
        result_label = tk.Label(
            self.footer_frame,
            text="$ Sahi Jawab $",
            font=self.question_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["correct"]
        )
        result_label.pack(pady=5)
        
        amount_label = tk.Label(
            self.footer_frame,
            text=f"Inbox :: ${self.amount}",
            font=self.info_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        amount_label.pack(pady=5)
        
        # Move to next question or end game
        self.current_question += 1
        if self.current_question < len(self.game_questions):
            next_label = tk.Label(
                self.footer_frame,
                text="Next Question!",
                font=self.info_font,
                bg=self.colors["bg_medium"],
                fg=self.colors["text_light"]
            )
            next_label.pack(pady=5)
            
            self.timer_id = self.root.after(2000, lambda: self.countdown_to_question(5))
        else:
            self.play_sound("applause")
            self.timer_id = self.root.after(2000, lambda: self.show_game_over(True))
    
    def show_wrong_answer(self, penalty):
        # Update amount with penalty
        if penalty > 0:
            self.amount -= penalty
        
        # Show wrong answer message
        result_label = tk.Label(
            self.footer_frame,
            text="x Galat Jawab x",
            font=self.question_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["wrong"]
        )
        result_label.pack(pady=5)
        
        amount_label = tk.Label(
            self.footer_frame,
            text=f"Won :: ${self.amount}",
            font=self.info_font,
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"]
        )
        amount_label.pack(pady=5)
        
        # End game
        self.timer_id = self.root.after(2000, lambda: self.show_game_over(False))
    
    def show_game_over(self, completed):
        # Clear frames
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        for widget in self.question_frame.winfo_children():
            widget.destroy()
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        for widget in self.lifelines_frame.winfo_children():
            widget.destroy()
        for widget in self.footer_frame.winfo_children():
            widget.destroy()
        
        # Game over message
        if completed:
            message = "Congratulations! You've completed all questions!"
        else:
            message = "Game Over!"
        
        game_over_label = tk.Label(
            self.question_frame,
            text=message,
            font=self.title_font,
            bg=self.colors["bg_light"],
            fg=self.colors["text_highlight"]
        )
        game_over_label.pack(pady=20)
        
        # Final amount
        amount_label = tk.Label(
            self.question_frame,
            text=f"You won: ${self.amount}",
            font=self.question_font,
            bg=self.colors["bg_light"],
            fg=self.colors["text_light"]
        )
        amount_label.pack(pady=10)
        
        # Play again button
        play_again_button = tk.Button(
            self.footer_frame,
            text="Play Again",
            font=self.question_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            activebackground=self.colors["button_hover"],
            activeforeground=self.colors["text_highlight"],
            padx=20,
            pady=10,
            relief=tk.RAISED,
            command=self.start_game
        )
        play_again_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Exit button
        exit_button = tk.Button(
            self.footer_frame,
            text="Exit",
            font=self.question_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            activebackground=self.colors["button_hover"],
            activeforeground=self.colors["text_highlight"],
            padx=20,
            pady=10,
            relief=tk.RAISED,
            command=self.root.quit
        )
        exit_button.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Sound toggle button
        sound_button = tk.Button(
            self.footer_frame,
            text="🔊 Sound: ON" if self.sound_enabled else "🔇 Sound: OFF",
            font=self.info_font,
            bg=self.colors["button"],
            fg=self.colors["text_light"],
            command=self.toggle_sound
        )
        sound_button.pack(side=tk.BOTTOM, pady=10)

# Main function to run the application
def main():
    root = tk.Tk()
    app = KBCGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()