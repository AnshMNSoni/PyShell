from turtle import Turtle, Screen

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.writer = Turtle()
        self.writer.hideturtle()
        self.writer.penup()
        self.writer.color("white")
        self.active = True
        self.difficulty = "Normal"
        self.max_score = 5
        
    def show_main_menu(self):
        """Display the main menu"""
        self.writer.clear()
        self.screen.tracer(0)
        
        # Title
        self.writer.goto(0, 150)
        self.writer.write("PING PONG", align="center", font=("Courier", 60, "bold"))
        
        # Menu options
        self.writer.goto(0, 50)
        self.writer.write(f"Difficulty: {self.difficulty}", align="center", font=("Courier", 24, "normal"))
        
        self.writer.goto(0, 0)
        self.writer.write(f"Max Score: {self.max_score}", align="center", font=("Courier", 24, "normal"))
        
        self.writer.goto(0, -50)
        self.writer.write("Press SPACE to start", align="center", font=("Courier", 24, "normal"))
        
        self.writer.goto(0, -100)
        self.writer.write("Press D to change difficulty", align="center", font=("Courier", 18, "normal"))
        
        self.writer.goto(0, -130)
        self.writer.write("Press M to change max score", align="center", font=("Courier", 18, "normal"))
        
        self.screen.update()
        
    def toggle_difficulty(self):
        """Toggle between difficulty levels"""
        difficulties = ["Easy", "Normal", "Hard"]
        current_index = difficulties.index(self.difficulty)
        next_index = (current_index + 1) % len(difficulties)
        self.difficulty = difficulties[next_index]
        self.show_main_menu()
        
    def toggle_max_score(self):
        """Toggle between max score options"""
        score_options = [5, 10, 15]
        current_index = score_options.index(self.max_score)
        next_index = (current_index + 1) % len(score_options)
        self.max_score = score_options[next_index]
        self.show_main_menu()
        
    def show_pause_menu(self):
        """Display pause menu"""
        self.writer.clear()
        self.writer.goto(0, 50)
        self.writer.write("GAME PAUSED", align="center", font=("Courier", 36, "bold"))
        self.writer.goto(0, -20)
        self.writer.write("Press P to resume", align="center", font=("Courier", 24, "normal"))
        self.writer.goto(0, -70)
        self.writer.write("Press Q to quit", align="center", font=("Courier", 24, "normal"))
        self.screen.update()
        
    def hide(self):
        """Hide the menu"""
        self.writer.clear()
        self.active = False