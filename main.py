'''Main module for Snake Game'''

from turtle import Screen
import time
from data import Snake, Food, Walls, Scoreboard, COLLISIONS


screen = Screen()
screen.colormode(255)
screen.setup(width=650, height=700)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

food = Food()
snake = Snake()
walls = Walls()

teleport = screen.textinput("Teleportation", "Do you want to have teleportation in the game?")
obstacles_question = screen.textinput("Obstacles", "Do you want to have obstacles in the game?")

score = Scoreboard(teleport, obstacles_question)

if obstacles_question is not None:
    walls.obstacle_walls()

COLLISIONS.extend(Snake.SEGMENTS)
COLLISIONS.extend(Walls.obstacles)

screen.listen()

screen.onkey(key = "Up", fun = snake.go_up)
screen.onkey(key = "w",  fun = snake.go_up)
screen.onkey(key = "Down",  fun = snake.down)
screen.onkey(key = "s",  fun = snake.down)
screen.onkey(key = "Left",  fun = snake.left)
screen.onkey(key = "a",  fun = snake.left)
screen.onkey(key = "Right",  fun = snake.right)
screen.onkey(key = "d",  fun = snake.right)
screen.onkey(key = "Escape",  fun = screen.bye)

screen.update()
if obstacles_question is not None:
    time.sleep(3)

GAME_IS_ON = True

while GAME_IS_ON:

    screen.update()

    # Check score and increase speed if needed
    if score.score < 5:
        SLEEP_TIME = 0.2
    elif score.score < 10:
        SLEEP_TIME = 0.15
    elif score.score < 15:
        SLEEP_TIME = 0.1
    elif score.score < 20:
        SLEEP_TIME = 0.075
    elif score.score < 25:
        SLEEP_TIME = 0.05
    elif score.score < 35:
        SLEEP_TIME = 0.035
    else:
        SLEEP_TIME = 0.025

    time.sleep(SLEEP_TIME)

    snake.move()
    food.bonus_fruit()

    # Detect Collision with Standard Food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        score.refresh("standard")

    # Detect Collision with Bonus Food
    if snake.head.distance(food.bonus_apple) < 15:
        snake.extend()
        score.refresh("bonus")
        food.bonus_fruit_eaten()

    # Detect collision with Obstacles
    for obstacle in walls.obstacles:
        if snake.head.distance(obstacle) < 10:
            # GAME_IS_ON = False
            # score.game_over()
            score.reset()
            snake.reset()
            # time.sleep(3)
            # screen.bye()

    if teleport is None:
        # Detect collision with wall
        if snake.head.xcor() > 285 or snake.head.xcor() < -285 or \
            snake.head.ycor() > 285 or snake.head.ycor() < -285:
            # GAME_IS_ON = False
            # score.game_over()
            score.reset()
            snake.reset()
            # time.sleep(3)
            # screen.bye()

    # Border teleportation logic
    elif snake.head.xcor() > 285:
        snake.head.setx(-280)
    elif snake.head.xcor() < -285:
        snake.head.setx(280)
    elif snake.head.ycor() > 285:
        snake.head.sety(-280)
    elif snake.head.ycor() < -285:
        snake.head.sety(280)

    # Detect collision with tail
    for segment in snake.SEGMENTS[1:]:
        if snake.head.distance(segment) < 10:
            # GAME_IS_ON = False
            # score.game_over()
            score.reset()
            snake.reset()
            # time.sleep(3)
            # screen.bye()

screen.mainloop()
