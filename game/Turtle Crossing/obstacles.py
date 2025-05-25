import turtle as t
from turtle import Turtle
import random

class Obstacles(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.car_list = []

    def random_clr(self):
        t.colormode(255)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def create_cars(self, level):
        if random.randint(1, 6) <= 2 + min(level, 3):  # more cars as level increases
            new_turtle = Turtle()
            new_turtle.penup()
            new_turtle.shape('square')
            new_turtle.shapesize(1, 3)
            new_turtle.color(self.random_clr())
            y = random.randint(-350, 350)
            new_turtle.goto(500, y)
            self.car_list.append(new_turtle)
