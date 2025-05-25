from turtle import Turtle
import random

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.goto(x=0, y=-160)
        self.shape('circle')
        self.color('red')
        self.x_move = 15
        self.y_move = 15
        self.move_speed = 0.1  # Added speed control for difficulty increase

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def y_bounce(self):
        self.y_move *= -1

    def x_bounce(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, -160)
        self.y_bounce()
        
    def increase_speed(self):
        """Increase ball speed slightly to make game progressively harder"""
        if self.move_speed > 0.03:  # Don't make it too fast
            self.move_speed *= 0.9