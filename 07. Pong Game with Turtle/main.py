"""The Screen for Pong Game"""

from turtle import Screen
from time import sleep
from initialization import Scoreboard, Ball, Paddle

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")
screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")

GAME_IS_ON = True

while GAME_IS_ON:
    sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect Wall collision
    if ball.ycor() > 280 or ball.ycor() < - 280:
        ball.bounce_y()

    # Detect Paddle collision
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or \
        ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    # Detect if ball missed the Right Paddle
    if ball.xcor() > 380:
        sleep(1)
        ball.reset_position()
        scoreboard.r_point()
        screen.update()
        sleep(1)

    # Detect if ball missed the Left Paddle
    if ball.xcor() < -380:
        sleep(1)
        ball.reset_position()
        scoreboard.l_point()
        screen.update()
        sleep(1)

screen.mainloop()
