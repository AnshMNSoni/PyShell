from turtle import Turtle
from random import *

class Food(Turtle):
    
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('circle')
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color('red')
        self.speed('fastest')
        self.refresh()
        
    def refresh(self):
        random_x = randint(-240, 240)
        random_y = randint(-240, 240)
        self.goto(random_x, random_y)
        