from turtle import Turtle
import os

FONT = ('Courier', 42, 'normal')
SMALL_FONT = ('Courier', 24, 'normal')

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.l_score = 0
        self.r_score = 0
        self.high_score = self.load_high_score()
        
        self.hideturtle()
        self.penup()
        self.color('white')
        self.update_score()
        
    def update_score(self):
        self.clear()
        self.goto(-50, 300)
        self.write(f"{self.l_score} {self.r_score}", font=FONT)
        self.goto(-400, 300)
        self.write(f"HIGH: {self.high_score}", font=SMALL_FONT)
    
    def l_point(self):
        self.l_score += 1
        self.check_high_score()
    
    def r_point(self):
        self.r_score += 1
        self.check_high_score()
        
    def check_high_score(self):
        current_max = max(self.l_score, self.r_score)
        if current_max > self.high_score:
            self.high_score = current_max
            self.save_high_score()
            
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))
            
    def game_over(self, winner):
        self.goto(0, 0)
        self.write(f"GAME OVER! {winner} WINS!", align="center", font=FONT)