"""The initialization module for the Pong game"""

from turtle import Turtle

class Scoreboard(Turtle):
    """The Scoreboard Class fot the Pong Game"""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.ht()
        self.pu()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()


    def middle_line(self):
        """Defines the Line in the middle of the Screen"""
        self.goto(0, 300)
        for num in range(-300, 320, 10):
            self.goto(0, num)
            if num % 20 == 0:
                self.pd()
            else:
                self.pu()
        self.pu()


    def update_scoreboard(self):
        """Updates the scoreboard"""
        self.clear()
        self.middle_line()
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
        """Defines "Bounce" from a Wall"""
        self.y_move *= -1


    def bounce_x(self):
        """Defines "Bounce" from a Paddle"""
        self.x_move *= -1
        self.move_speed *= 0.9


    def reset_position(self):
        """Defines the behaviour of the Ball being missed"""
        self.goto(0, 0)
        self.move_speed = 0.1
        self.x_move *= -1

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
