from turtle import Screen, Turtle
from reflector import LeftReflector, RightReflector
from ball import Object, PowerUp
from scoretrack import Score
from menu import Menu
from sound import Sound
import time
import random

# Setup screen
screen = Screen()
screen.title('ENHANCED PING-PONG')
screen.bgcolor('black')
screen.setup(height=750, width=950)
screen.tracer(0)

# Initialize sound
sound = Sound()

# Create divider line
def create_divider():
    tt = Turtle()
    tt.goto(0, 350)
    tt.hideturtle()
    tt.color('white')
    tt.right(90)
    tt.pensize(5)
    while True:
        tt.fd(20)
        tt.penup()
        tt.fd(20)
        tt.pendown()
        if (tt.ycor() <= -370):
            break

# Initialize game objects
left = LeftReflector()
right = RightReflector()
ball = Object()
powerup = PowerUp()
scoreboard = Score()
menu = Menu(screen)

# Game state variables
game_is_on = False
is_paused = False
difficulty_speeds = {"Easy": 0.15, "Normal": 0.1, "Hard": 0.05}
power_up_types = ["size", "speed"]
power_up_counter = 0
max_score = 5

# Show main menu
menu.show_main_menu()

# Key bindings
def start_game():
    global game_is_on, max_score
    if menu.active:
        menu.hide()
        create_divider()
        game_is_on = True
        max_score = menu.max_score
        # Set initial ball speed based on difficulty
        ball.base_speed = 8 if menu.difficulty == "Easy" else 10 if menu.difficulty == "Normal" else 12
        ball.reset_speed()

def toggle_pause():
    global is_paused
    if game_is_on:
        is_paused = ball.toggle_pause()
        if is_paused:
            menu.show_pause_menu()
        else:
            menu.hide()

def quit_game():
    global game_is_on
    if is_paused:
        game_is_on = False
        menu.show_main_menu()

def change_difficulty():
    if menu.active:
        menu.toggle_difficulty()

def change_max_score():
    if menu.active:
        menu.toggle_max_score()

# Set up key bindings
screen.listen()
screen.onkey(key='w', fun=left.up)
screen.onkey(key='s', fun=left.down)
screen.onkey(key='Up', fun=right.up)
screen.onkey(key='Down', fun=right.down)
screen.onkey(key='space', fun=start_game)
screen.onkey(key='p', fun=toggle_pause)
screen.onkey(key='q', fun=quit_game)
screen.onkey(key='d', fun=change_difficulty)
screen.onkey(key='m', fun=change_max_score)

# Main game loop
while True:
    if game_is_on and not is_paused:
        # Move the ball
        ball.move()
        
        # Update power-up status for paddles
        left.update_power_status()
        right.update_power_status()
        
        # Randomly spawn power-ups
        power_up_counter += 1
        if power_up_counter >= 100 and not powerup.is_active and random.random() < 0.02:
            powerup.activate()
            power_up_counter = 0
        
        # Check for wall collisions
        if abs(ball.ycor()) >= 350:
            ball.y_bounce()
            sound.play_bounce()
        
        # Check for scoring
        if ball.xcor() >= 480:
            scoreboard.l_point()
            scoreboard.update_score()
            sound.play_score()
            ball.reset_position()
            # Check for game over
            if scoreboard.l_score >= max_score:
                scoreboard.game_over("LEFT PLAYER")
                time.sleep(3)
                game_is_on = False
                menu.show_main_menu()
                scoreboard.l_score = 0
                scoreboard.r_score = 0
                scoreboard.update_score()
        
        if ball.xcor() <= -480:
            scoreboard.r_point()
            scoreboard.update_score()
            sound.play_score()
            ball.reset_position()
            # Check for game over
            if scoreboard.r_score >= max_score:
                scoreboard.game_over("RIGHT PLAYER")
                time.sleep(3)
                game_is_on = False
                menu.show_main_menu()
                scoreboard.l_score = 0
                scoreboard.r_score = 0
                scoreboard.update_score()
        
        # Check for paddle collisions
        for seg_lst in range(4):
            if right.segments[seg_lst].distance(ball) <= 25:
                ball.x_bounce()
                sound.play_bounce()
                # Increase ball speed occasionally
                if random.random() < 0.3:
                    ball.increase_speed()
            
            if left.segments[seg_lst].distance(ball) <= 25:
                ball.x_bounce()
                sound.play_bounce()
                # Increase ball speed occasionally
                if random.random() < 0.3:
                    ball.increase_speed()
        
        # Check for power-up collision
        if powerup.is_active and ball.distance(powerup) < 20:
            power_type = random.choice(power_up_types)
            # Apply power-up to the paddle that's on the same side as the ball
            if ball.xcor() < 0:
                left.apply_power_up(power_type)
                for segment in left.segments:
                    segment.color('yellow')
            else:
                right.apply_power_up(power_type)
                for segment in right.segments:
                    segment.color('yellow')
            
            powerup.deactivate()
            sound.play_powerup()
    
    # Update screen
    screen.update()
    
    # Control game speed based on difficulty
    if game_is_on and not is_paused:
        time.sleep(difficulty_speeds.get(menu.difficulty, 0.1))

screen.exitonclick()