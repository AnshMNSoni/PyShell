# Enhanced Turtle Crossing Game

from turtle import Screen
from TurtleClass import Object
from obstacles import Obstacles
import time

screen = Screen()
screen.setup(height=800, width=1000)
screen.title("Turtle Crossing")
screen.tracer(0)

obj = Object()
cars = Obstacles()

# Keyboard events
screen.listen()
screen.onkey(fun=obj.up, key='Up')
screen.onkey(fun=obj.down, key='Down')
screen.onkey(fun=obj.toggle_pause, key='p')

count = 1
level = 1
game_is_on = True

while game_is_on:
    screen.update()
    
    if obj.paused:
        continue

    cars.create_cars(level)

    for go in range(len(cars.car_list)):
        time.sleep(0.001)
        screen.update()
        tle = cars.car_list[go]
        tle.backward(20 + level * 2)

        dis = tle.distance(obj.pos())
        if dis <= 30:
            obj.lives -= 1
            obj.update_scoreboard()
            obj.goto(0, -370)
            if obj.lives == 0:
                screen.clear()
                obj.gameover()
                game_is_on = False
                break

    if obj.ycor() >= 370:
        obj.score += 1
        level += 1
        obj.goto(0, -370)
        obj.update_scoreboard()

    count += 1

screen.exitonclick()
