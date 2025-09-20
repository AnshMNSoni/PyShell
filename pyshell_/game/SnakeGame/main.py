# Snake-Game:

from turtle import Turtle, Screen
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoard

tt = Turtle()
screen = Screen()
screen.setup(height=600, width=600)
tt.color('white')

for t in range(5, 0, -1):
    screen.bgcolor('black')
    tt.hideturtle()
    tt.write(f"Game starts in {t} sec...", align="Center", font=('Courier', 22, 'normal'))
    time.sleep(1)
    screen.clear()

screen.bgcolor('black')
screen.title("My Snake Game")
screen.tracer(0)

sap = Snake()
food = Food()
score = ScoreBoard()

screen.listen()
screen.onkey(sap.up, 'Up')
screen.onkey(sap.down, 'Down')
screen.onkey(sap.left, 'Left')
screen.onkey(sap.right, 'Right')

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)
    sap.move()
    
    # Detect collision with food:
    if sap.head.distance(food) < 22:
        score.increase_score()
        sap.extend()
        food.refresh()
    
    # Detect collision with wall:
    if sap.head.xcor() > 290 or sap.head.xcor() < -290 or sap.head.ycor() > 250 or sap.head.ycor() < -290:
        score.reset()
        score.update()
        food.refresh()
        sap.reset_snake()

        
    # Detect collision with tail:
    for segment in sap.segments[1:]:
        if sap.head.distance(segment) < 10:
            score.reset()
            score.update()
            food.refresh()
            sap.reset_snake()
    
    
screen.exitonclick()