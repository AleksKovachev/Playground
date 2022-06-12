"""A Ball module for the Pong Game"""

from turtle import Turtle

class Ball(Turtle):
    """A Ball Class for the Pong Game"""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.pu()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1

    def move(self):
        """Defines the movement of the Ball"""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Defines what "Bounce" in the y coordinate means for the Ball"""
        self.y_move *= -1

    def bounce_x(self):
        """Defines what "Bounce" in the x coordinatemeans for the Ball"""
        self.x_move *= -1
        self.move_speed * 0.9

    def reset_position(self):
        """Defines the behaviour of the Ball being missed"""
        self.goto(0, 0)
        self.move_speed = 0.1
        self.x_move *= -1
        self.move_speed * 0.9
