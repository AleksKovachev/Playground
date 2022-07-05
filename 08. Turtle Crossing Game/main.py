"""Main module for the Turtle Crossing Game"""

from time import sleep
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(player.move, "Up")

GAME_IS_ON = True
while GAME_IS_ON:
    sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    # Check Turtle collision with cars
    for car in car_manager.all_cars:
        if car.distance(player) < 20:
            GAME_IS_ON = False
            scoreboard.game_over()
            sleep(5)
            screen.reset()
            car_manager.reset_game()
            player.reset_game()
            scoreboard.reset_game()
            GAME_IS_ON = True

    # Detect if Turtle finished
    if player.is_at_finish_line():
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()

screen.mainloop()
