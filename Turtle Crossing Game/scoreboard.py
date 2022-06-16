"""The Scoreboard module for the Turtle Crossing Game"""
from turtle import Turtle
FONT = ("Courier", 12, "bold")


class Scoreboard(Turtle):
    """The Scoreboard class for the Turtle Crossing Game"""

    def __init__(self):
        super().__init__()
        self.level = 1
        self.car_density = 1
        self.ht()
        self.pu()
        self.goto(-285, 275)
        self.update_scoreboard()


    def update_scoreboard(self):
        """Updates the scoreboard"""
        self.clear()
        self.write("_"*57, align="left", font=FONT)
        self.write(
            f"Level: {self.level} | Car density: {self.car_density}", align="left", font=FONT)


    def increase_level(self):
        """Updates the level number"""
        self.level += 1
        if self.level >= 25:
            self.car_density = 4
        elif self.level >= 20:
            self.car_density = 3
        elif self.level >= 15:
            self.car_density = 2
        self.update_scoreboard()


    def game_over(self):
        """GAME OVER screen"""
        self.goto(0, 0)
        self.write("GAME OVER", align="center", font=("Courier", 24, "bold"))


    def reset_game(self):
        """Resets the scoreboard"""
        self.reset()
        self.__init__()
