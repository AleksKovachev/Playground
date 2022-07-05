"""The Player module for the Turtle Crossing Game"""
from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 20
FINISH_LINE_Y = 260


class Player(Turtle):
    """The Player class for the Turtle Crossing Game"""

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.pu()
        self.go_to_start()
        self.left(90)


    def move(self):
        """Defines the Turtle's movement"""
        self.forward(MOVE_DISTANCE)


    def is_at_finish_line(self):
        """Checks if player reached the finish line"""
        return self.ycor() > FINISH_LINE_Y


    def go_to_start(self):
        """Resets Player's position"""
        self.goto(STARTING_POSITION)


    def reset_game(self):
        """Resets Player"""
        self.reset()
        self.__init__()
