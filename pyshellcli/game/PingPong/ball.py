from turtle import Turtle, Screen
import random

screen = Screen()

class Object(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('circle')
        self.color('red')
        self.shapesize(1, 1)
        self.speed_level = 1
        self.base_speed = 10
        self.x_move = self.base_speed
        self.y_move = self.base_speed
        self.is_paused = False
        
    def move(self):
        if not self.is_paused:
            screen.update()
            new_x = self.xcor() + self.x_move
            new_y = self.ycor() + self.y_move
            self.goto(new_x, new_y)
    
    def y_bounce(self):
        self.y_move *= -1
        
    def x_bounce(self):
        self.x_move *= -1
        # Add a slight random angle after bounce for unpredictability
        self.y_move += random.uniform(-2, 2)
    
    def reset_position(self):
        self.goto(0, 0)
        self.x_bounce()
        
    def increase_speed(self):
        """Increase ball speed for higher difficulty"""
        if self.speed_level < 5:
            self.speed_level += 1
            speed_factor = 1 + (self.speed_level * 0.2)
            self.x_move = self.base_speed * speed_factor * (1 if self.x_move > 0 else -1)
            self.y_move = self.base_speed * speed_factor * (1 if self.y_move > 0 else -1)
            
    def reset_speed(self):
        """Reset ball to initial speed"""
        self.speed_level = 1
        self.x_move = self.base_speed * (1 if self.x_move > 0 else -1)
        self.y_move = self.base_speed * (1 if self.y_move > 0 else -1)
        
    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        return self.is_paused


class PowerUp(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('circle')
        self.color('yellow')
        self.shapesize(0.8, 0.8)
        self.speed(0)
        self.hideturtle()
        self.is_active = False
        
    def activate(self):
        """Activate a power-up at a random position"""
        if not self.is_active:
            x = random.randint(-400, 400)
            y = random.randint(-300, 300)
            self.goto(x, y)
            self.showturtle()
            self.is_active = True
            
    def deactivate(self):
        """Deactivate the power-up"""
        self.hideturtle()
        self.is_active = False