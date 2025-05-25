from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.lives = 3
        self.update_scoreboard()
        
    def update_scoreboard(self):
        self.clear()
        self.goto(-450, -320)
        self.write(f"Score: {self.score}", align="left", font=("Courier", 16, "normal"))
        self.goto(450, -320)
        self.write(f"Lives: {self.lives}", align="right", font=("Courier", 16, "normal"))
    
    def increase_score(self, points=10):
        self.score += points
        self.update_scoreboard()
        
    def lose_life(self):
        self.lives -= 1
        self.update_scoreboard()
        return self.lives <= 0
        
    def game_over(self, won=False):
        self.goto(0, 0)
        if won:
            self.write("YOU WIN!", align="center", font=("Courier", 30, "bold"))
        else:
            self.write("GAME OVER", align="center", font=("Courier", 30, "bold"))
        self.goto(0, -50)
        self.write(f"Final Score: {self.score}", align="center", font=("Courier", 20, "normal"))