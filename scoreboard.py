'''A Scoreboard Class for the Snkae Game'''

from turtle import Turtle


ALIGNMENT = "center"
FONT = ("Calibri", "24", "bold")

class Scoreboard(Turtle):
    '''A Scoreboard Object'''

    def __init__(self):
        self.score = -1
        super().__init__()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.sety(310)
        self.refresh()


    def refresh(self):
        '''Refreshes the score of the food'''
        self.score += 1
        self.clear()
        self.write(f'Score: {self.score}', font=FONT, align=ALIGNMENT)


    def game_over(self):
        '''Announces Game Over'''
        self.goto(0, 0)
        self.write("GAME OVER!", align=ALIGNMENT, font=FONT)
