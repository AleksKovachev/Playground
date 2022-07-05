"""The Car module for the Turtle Crossing Game"""
from turtle import Turtle
from random import choice, randrange

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 1


class CarManager:
    """The Car class for the Turtle Crossing Game"""

    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE
        self.car_density = 6


    def create_car(self):
        """Creates a new car and appends it to the list of all cars"""
        random_chance = randrange(1, self.car_density)
        if random_chance == 1:
            new_car = Turtle("square")
            new_car.shapesize(1, 2)
            new_car.pu()
            new_car.color(choice(COLORS))
            random_y = randrange(-240, 240, 20)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)


    def move_cars(self):
        """Defines Car movement"""
        for car in self.all_cars:
            car.backward(self.car_speed)


    def level_up(self):
        """Increases Car speed"""
        self.car_speed += MOVE_INCREMENT
        if self.car_speed >= 25:
            self.car_density = 3
        elif self.car_speed >= 20:
            self.car_density = 4
        elif self.car_speed >= 15:
            self.car_density = 5


    def reset_game(self):
        """Resets Car Manager"""
        for car in self.all_cars:
            car.reset()
        self.__init__()
