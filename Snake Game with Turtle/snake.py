'''A Snake Class for the Snkae Game'''
# TODO: Fix input self-colision issue!
from turtle import Turtle

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:
    '''A Snake Character'''

    SEGMENTS = []
    MOVE_DISTANCE = 20


    def __init__(self):
        self.create_snake()
        self.head = self.SEGMENTS[0]


    def create_snake(self):
        '''Initializing the Snake'''
        segment = Turtle(shape="triangle")
        segment.color("medium aquamarine")
        segment.penup()
        segment.shapesize(stretch_len=0.9, stretch_wid=0.9)
        self.SEGMENTS.append(segment)

        segment = Turtle(shape="square")
        segment.color("sea green")
        segment.penup()
        segment.goto(self.SEGMENTS[-1].position())
        self.SEGMENTS.append(segment)

        segment = Turtle(shape="square")
        segment.color("medium sea green")
        segment.penup()
        segment.shapesize(stretch_len=0.8, stretch_wid=0.8)
        segment.goto(self.SEGMENTS[-1].position())
        self.SEGMENTS.append(segment)


    def extend(self):
        '''Extends the body if the Snake'''
        segment = Turtle(shape="square")
        if len(self.SEGMENTS) % 2 != 0:
            segment.color("sea green")
        else:
            segment.color("medium sea green")
            segment.shapesize(stretch_len=0.8, stretch_wid=0.8)
        segment.penup()
        segment.goto(self.SEGMENTS[-1].position())
        self.SEGMENTS.append(segment)


    def move(self):
        '''Move Method for the Snake'''
        for seg_num in range(len(self.SEGMENTS) -1 , 0 , -1):
            self.SEGMENTS[seg_num].goto(self.SEGMENTS[seg_num - 1].position())

        self.head.forward(self.MOVE_DISTANCE)


    def up(self):
        '''Turns Up'''
        if self.head.heading() != DOWN:
            self.head.setheading(UP)


    def down(self):
        '''Turns Down'''
        if self.head.heading() != UP:
            self.head.setheading(DOWN)


    def left(self):
        '''Turns Left'''
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)


    def right(self):
        '''Turns Right'''
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
