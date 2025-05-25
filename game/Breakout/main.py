from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import random
import time
import turtle

# Setup screen
screen = Screen()
screen.tracer(0)
screen.bgcolor('black')
screen.title('Breakout Game')
screen.setup(width=1000, height=650)

# Initialize game components
paddle = Paddle(screen)
ball = Ball()
scoreboard = Scoreboard()

# Function to generate random colors
def random_clr():
    turtle.colormode(255)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# Create bricks
box_lst = []
X = -490
Y = 290

# Different rows have different point values
row_values = [30, 20, 20, 10, 10, 10]
row = 0

for y_pos in range(290, -100, -60):
    X = -490
    points = row_values[row] if row < len(row_values) else 10
    row += 1
    
    for _ in range(7):  # Create 7 bricks per row
        tut = Turtle('square')
        tut.penup()
        tut.shapesize(stretch_len=7.5, stretch_wid=2.5)
        tut.color(random_clr())
        tut.goto(x=X, y=y_pos)
        # Store the brick and its point value
        box_lst.append((tut, points))
        X += 160

screen.update()

# Setup keyboard controls
screen.listen()
# Single key press movement
screen.onkey(key='Right', fun=paddle.on_right)
screen.onkey(key='Left', fun=paddle.on_left)

# Continuous movement for smoother control
screen.onkeypress(key='Right', fun=paddle.start_move_right)
screen.onkeyrelease(key='Right', fun=paddle.stop_move_right)
screen.onkeypress(key='Left', fun=paddle.start_move_left)
screen.onkeyrelease(key='Left', fun=paddle.stop_move_left)

# Keep the pause controls
screen.onkey(key='p', fun=lambda: pause_game())
screen.onkey(key='space', fun=lambda: resume_game())

# Game state variables
game_is_on = True
paused = False
level = 1

def pause_game():
    global paused
    paused = True
    # Display pause message
    pause_text = Turtle()
    pause_text.penup()
    pause_text.hideturtle()
    pause_text.color("white")
    pause_text.goto(0, 0)
    pause_text.write("PAUSED - Press SPACE to continue", align="center", font=("Courier", 20, "normal"))
    return pause_text

def resume_game():
    global paused
    paused = False

# Main game loop
while game_is_on:
    if paused:
        screen.update()
        continue
        
    time.sleep(ball.move_speed)
    ball.move()
    screen.update()

    # Detect collision with wall
    if ball.xcor() > 480 or ball.xcor() < -480:
        ball.x_bounce()

    if ball.ycor() > 320:
        ball.y_bounce()
        
    # Detect collision with paddle - UPDATED for single paddle
    if ball.distance(paddle) < 50 and ball.ycor() < -280:
        # Calculate bounce angle based on where the ball hits the paddle
        # This makes the game more interesting
        relative_x = ball.xcor() - paddle.xcor()
        normalized_x = relative_x / 40  # Normalize based on paddle width
        ball.x_move = 15 * normalized_x  # Adjust horizontal direction based on hit position
        
        # Make sure the ball always moves upward after hitting the paddle
        if ball.y_move < 0:
            ball.y_bounce()

    # Detect collision with bricks
    for box, points in box_lst[:]:
        if ball.distance(box) < 60:
            ball.y_bounce()
            box.goto(2000, 2000)  # Move the box off-screen
            box_lst.remove((box, points))
            scoreboard.increase_score(points)
            
            # Increase ball speed slightly after hitting a brick
            ball.increase_speed()
            
            # Check if all bricks are cleared
            if len(box_lst) == 0:
                scoreboard.game_over(won=True)
                game_is_on = False

    # Reset ball position if it goes out of bounds
    if ball.ycor() < -320:
        game_over = scoreboard.lose_life()
        if game_over:
            scoreboard.game_over(won=False)
            game_is_on = False
        else:
            ball.reset_position()
            time.sleep(1)  # Pause briefly before continuing

    screen.update()

# Wait for user to close the window
screen.exitonclick()