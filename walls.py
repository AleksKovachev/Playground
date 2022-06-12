'''A Walls Class for the Snkae Game'''
# TODO: Random Wall Forms

import random
from turtle import Turtle

class Walls(Turtle):
    '''A Food Object'''

    obstacles = []

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("red")
        self.speed(0)
        self.draw_wall()

    # def draw_wall(self):
    #     self.goto(-295, 295)
    #     self.pendown()
    #     self.pensize(10)
    #     self.goto(295, 295)
    #     self.right(90)
    #     self.goto(295, -295)
    #     self.right(90)
    #     self.goto(-295, -295)
    #     self.right(90)
    #     self.goto(-295, 295)

    def draw_wall(self):
        '''Puts a wall surrounding the playing area'''
        for i in range(-300, 301, 20):
            new_turtle = Turtle(shape="square")
            new_turtle.shapesize(0.8, 0.8)
            new_turtle.color((112, 128, 144), (178, 34, 34))
            new_turtle.penup()
            new_turtle.goto(i, 300)

        for i in range(-300, 301, 20):
            new_turtle = Turtle(shape="square")
            new_turtle.shapesize(0.8, 0.8)
            new_turtle.color((112, 128, 144), (178, 34, 34))
            new_turtle.penup()
            new_turtle.goto(300, i)

        for i in range(-300, 301, 20):
            new_turtle = Turtle(shape="square")
            new_turtle.shapesize(0.8, 0.8)
            new_turtle.color((112, 128, 144), (178, 34, 34))
            new_turtle.penup()
            new_turtle.goto(i, -300)

        for i in range(-300, 301, 20):
            new_turtle = Turtle(shape="square")
            new_turtle.shapesize(0.8, 0.8)
            new_turtle.color((112, 128, 144), (178, 34, 34))
            new_turtle.penup()
            new_turtle.goto(-300, i)

    def obstacle_walls(self):
        '''Creates obstacles on the field'''
        for _ in range(random.randint(5, 20)):
            new_turtle = Turtle(shape="square")
            new_turtle.shapesize(0.8, 0.8)
            new_turtle.color((112, 128, 144), (178, 34, 34))
            new_turtle.penup()
            new_turtle.goto(random.randrange(-280, 280, 20), random.randrange(-280, 280, 20))
            for obs in self.obstacles:
                while obs.distance(new_turtle) < 15 and obs.position() not in ((0, 0), (20, 0)):
                    new_turtle.goto(random.randrange(-280, 280, 20), random.randrange(-280, 280, 20))
            self.obstacles.append(new_turtle)
