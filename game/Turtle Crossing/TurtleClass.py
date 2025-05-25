from turtle import Turtle, Screen

ALIGNMENT = 'Center'
FONT = ('Courier', 22, 'normal')

class Object(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.shapesize(1.3)
        self.speed('fastest')
        self.penup()
        self.goto(0, -370)
        self.setheading(90)
        self.score = 0
        self.lives = 3
        self.paused = False

        self.display = Turtle()
        self.display.hideturtle()
        self.display.penup()
        self.display.goto(-450, 350)
        self.update_scoreboard()

    def up(self):
        if not self.paused:
            self.forward(20)

    def down(self):
        if not self.paused:
            self.backward(20)

    def toggle_pause(self):
        self.paused = not self.paused

    def update_scoreboard(self):
        self.display.clear()
        self.display.write(f"Score: {self.score}  Lives: {self.lives}", align='left', font=FONT)

    def win(self):
        t = Turtle()
        t.hideturtle()
        t.color('green')
        t.write(f':: Win ::', align=ALIGNMENT, font=FONT)

    def gameover(self):
        t = Turtle()
        t.hideturtle()
        t.color('red')
        t.write(f':: Game Over ::', align=ALIGNMENT, font=FONT)
