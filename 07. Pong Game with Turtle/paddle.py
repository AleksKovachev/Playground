"""A Paddle module for the Pong Game"""

from turtle import Turtle

class Paddle(Turtle):
    """A Paddle Class for the Pong Game"""

    def  __init__(self, position):
        super().__init__()

        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.color("white")
        self.pu()
        self.goto(position)


    def go_up(self):
        """Allows the Paddle to Move Up"""
        if self.ycor() <= 240:
            new_y = self.ycor() + 20
            self.goto(self.xcor(), new_y)


    def go_down(self):
        """Allows the Paddle to Move Down"""
        if self.ycor() >= -230:
            new_y = self.ycor() - 20
            self.goto(self.xcor(), new_y)
