from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=8)  # Create a wide paddle
        self.penup()
        self.goto(0, -300)
        self.speed("fastest")
        
        # Movement speed (pixels per move)
        self.move_speed = 20
        
    def on_right(self):
        if self.xcor() < 420:  # Boundary check
            self.setx(self.xcor() + self.move_speed)
            self.screen.update()
        
    def on_left(self):
        if self.xcor() > -420:  # Boundary check
            self.setx(self.xcor() - self.move_speed)
            self.screen.update()
            
    # Add continuous movement for smoother control
    def start_move_right(self):
        self.move_right = True
        self.move_continuously()
        
    def start_move_left(self):
        self.move_left = True
        self.move_continuously()
        
    def stop_move_right(self):
        self.move_right = False
        
    def stop_move_left(self):
        self.move_left = False
        
    def move_continuously(self):
        if hasattr(self, 'move_right') and self.move_right and self.xcor() < 420:
            self.setx(self.xcor() + 10)  # Smaller increment for smoother movement
            self.screen.update()
            self.screen.ontimer(self.move_continuously, 10)  # Call again after 10ms
        elif hasattr(self, 'move_left') and self.move_left and self.xcor() > -420:
            self.setx(self.xcor() - 10)  # Smaller increment for smoother movement
            self.screen.update()
            self.screen.ontimer(self.move_continuously, 10)  # Call again after 10ms