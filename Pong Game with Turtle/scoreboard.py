"""The Scoreboard module for the Pong game"""

from turtle import Turtle

class Scoreboard(Turtle):
    """The Scoreboard Class fot the Pong Game"""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.pu()
        self.ht()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        """Updates the scoreboard"""
        self.clear()
        self.goto(-50, 200)
        self.write(self.l_score, align="center", font=("Courier", 60, "normal"))
        self.goto(50, 200)
        self.write(self.r_score, align="center", font=("Courier", 60, "normal"))

    def l_point(self):
        """Increases the points for the left Paddle"""
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        """Increases the points for the left Paddle"""
        self.r_score += 1
        self.update_scoreboard()
