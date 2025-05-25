from turtle import Turtle, Screen
screen = Screen()
ALIGNMENT = 'Center'
FONT = ('Courier', 22, 'normal')

class ScoreBoard(Turtle):
    def __init__(self):
        self.count = 0
        self.high_count = 0
        with open('game/Snake-Game/high-score.txt') as data:
            self.high_count = int(data.read())
            
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color('white')
        self.goto(0, 250)
        self.write(f'Score :: {self.count} | High Score :: {self.high_count}', align=ALIGNMENT, font=FONT)
    
    def update(self):
        self.clear()
        self.write(f'Score :: {self.count} | High Score :: {self.high_count}', align=ALIGNMENT, font=FONT)
        
    def reset(self):
        if (self.count > self.high_count):
            self.high_count = self.count
            
            with open('high-score.txt', 'w') as h:
                h.write(f"{self.high_count}")
                
        self.count = 0
        
    
    def increase_score(self):
        self.hideturtle()
        self.count += 1
        self.update()
        