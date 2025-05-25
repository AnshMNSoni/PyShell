from turtle import Turtle, Screen
import random

LEFT_POSITION = [(-450, 60), (-450, 40), (-450, 20), (-450, 0)]
RIGHT_POSITION = [(450, 60), (450, 40), (450, 20), (450, 0)]
screen = Screen()

class LeftReflector:
    def __init__(self):
        self.segments = []
        self.create_reflector()
        self.speed = 20
        self.powered_up = False
        self.power_timer = 0
        
    def create_reflector(self):
        for seg in LEFT_POSITION:
            new_turtle = Turtle('square')
            new_turtle.penup()
            new_turtle.color('white')  
            new_turtle.goto(seg)  
            self.segments.append(new_turtle)
        screen.update()
            
    def down(self):
        if self.segments[3].ycor() > -330:  # Boundary check
            self.segments[3].setheading(270)
            for turtles in range(len(self.segments) - 1):
                x = self.segments[turtles + 1].xcor()
                y = self.segments[turtles + 1].ycor()
                self.segments[turtles].goto(x, y)
            self.segments[3].fd(self.speed)
            screen.update() 
    
    def up(self):
        if self.segments[0].ycor() < 330:  # Boundary check
            self.segments[0].setheading(90)
            for turtles in range(len(self.segments) - 1, 0, -1):
                x = self.segments[turtles - 1].xcor()
                y = self.segments[turtles - 1].ycor()
                self.segments[turtles].goto(x, y)
            self.segments[0].fd(self.speed)
            screen.update()
            
    def apply_power_up(self, power_type):
        """Apply a power-up effect to the reflector"""
        self.powered_up = True
        self.power_timer = 50  # Duration of power-up
        
        if power_type == "size":
            # Increase paddle size
            for segment in self.segments:
                segment.shapesize(1, 1.5)
        elif power_type == "speed":
            # Increase paddle speed
            self.speed = 30
            
    def update_power_status(self):
        """Update power-up status"""
        if self.powered_up:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.reset_power()
                
    def reset_power(self):
        """Reset power-up effects"""
        self.powered_up = False
        self.speed = 20
        for segment in self.segments:
            segment.shapesize(1, 1)
            segment.color('white')

class RightReflector(LeftReflector):
    def __init__(self):
        self.segments = []
        self.speed = 20
        self.powered_up = False
        self.power_timer = 0
        self.create_reflector()
        
    def create_reflector(self):
        for seg in RIGHT_POSITION:
            new_turtle = Turtle('square')
            new_turtle.penup()
            new_turtle.color('white')  
            new_turtle.goto(seg)  
            self.segments.append(new_turtle)
        screen.update()