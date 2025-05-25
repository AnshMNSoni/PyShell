from turtle import Turtle
import time
COR = [(0, 0), (-20, 0), (-40, 0)]
DISTANCE = 20

class Snake:

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        
    def create_snake(self):
        for position in COR:
            self.add_segment(position)
            
    def add_segment(self, position):
        new_tutle = Turtle('square')
        new_tutle.color('white')
        new_tutle.penup()
        new_tutle.goto(position)
        self.segments.append(new_tutle)
        
    def extend(self):
        self.add_segment(self.segments[-1].pos())
            
    def move(self):
        for seg in range(len(self.segments) - 1, 0, -1):
            x = self.segments[seg - 1].xcor()
            y = self.segments[seg - 1].ycor()
            self.segments[seg].goto(x, y)
        self.head.fd(DISTANCE)
    
    def reset_snake(self):
        for seg in self.segments:
            seg.goto(1000, 1000)
        
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]
        
    def up(self):
        current = self.head.heading()
        new = 90
        if (abs(new - current) != 180):
            self.head.setheading(90)
    
    def down(self):
        current = self.head.heading()
        new = 270
        if (abs(new - current) != 180):
            self.head.setheading(270)
    
    def right(self):
        current = self.head.heading()
        new = 0
        if (abs(new - current) != 180):
            self.head.setheading(0)
    
    def left(self):
        current = self.head.heading()
        new = 180
        if (abs(new - current) != 180):
            self.head.setheading(180)