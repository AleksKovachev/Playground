'''A Data Class for the Snkae Game'''

from turtle import Turtle
import random
import time

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0
ALIGNMENT = "center"
FONT = ("Calibri", "24", "bold")
FONT2 = ("Calibri", "20", "normal")
COLLISIONS = []


def check_positions(obj):
    '''Only allows spawning objects at available positions'''
    obj.goto(random.randrange(-280, 280, 20), random.randrange(-280, 280, 20))
    for item in COLLISIONS:
        if item.distance(obj) < 15:
            check_positions(obj)


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
        COLLISIONS.append(segment)


    def reset(self):
        """Resets the Snake to starting position"""
        for seg in self.SEGMENTS:
            seg.goto(1000, 1000)
        self.SEGMENTS.clear()
        self.create_snake()
        self.head = self.SEGMENTS[0]


    def move(self):
        '''Move Method for the Snake'''
        for seg_num in range(len(self.SEGMENTS) -1 , 0 , -1):
            self.SEGMENTS[seg_num].goto(self.SEGMENTS[seg_num - 1].position())

        self.head.forward(self.MOVE_DISTANCE)


    def go_up(self):
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


class Food(Turtle):
    '''A Food Object'''

    def __init__(self):
        super().__init__()
        self.bonus_counter = time.time()
        self.fruit_spawned = False

        self.bonus_apple = Turtle(shape = "circle")
        self.bonus_apple.color((240, 220, 0))
        self.bonus_apple.penup()
        self.bonus_apple.ht()
        self.bonus_apple.goto(300, 325)

        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color((random.randint(150, 255), random.randint(0, 100), random.randint(0, 100)))
        self.speed(0)
        self.refresh()


    def refresh(self):
        '''Refreshes the location of the food'''

        # Sets the location at a position divisible by 20
        # so that the Snake is always aligned with the Food
        self.clear()
        check_positions(self)
        self.color((random.randint(150, 255), random.randint(0, 100), random.randint(0, 100)))

    def bonus_fruit(self):
        '''Adds a bonus Fruit'''

        for i in range(15):
            if self.fruit_spawned and i == int(time.time() - self.bonus_counter):
                self.bonus_apple.color((240, 220, 17 * i))
            if self.fruit_spawned and time.time() - self.bonus_counter > 5:
                if int(time.time() - self.bonus_counter) % 2 == 0:
                    self.bonus_apple.ht()
                else:
                    self.bonus_apple.st()

        if time.time() - self.bonus_counter > random.randint(30, 50):
            self.fruit_spawned = True
            self.bonus_counter = time.time()
            check_positions(self.bonus_apple)
            self.bonus_apple.st()

        if self.fruit_spawned and time.time() - self.bonus_counter > 15:
            self.bonus_fruit_eaten()


    def bonus_fruit_eaten(self):
        '''What happens when the Bonus Fruit gets eaten'''
        self.fruit_spawned = False
        self.bonus_counter = time.time()
        self.bonus_apple.ht()
        self.bonus_apple.goto(300, 325)


class Walls(Turtle):
    '''A Food Object'''

    obstacles = []

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("red")
        self.speed(0)
        self.draw_border()

    # def draw_border(self):
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


    def draw_border(self):
        '''Puts a wall surrounding the playing area'''
        for k in range(4):
            for i in range(-300, 301, 20):
                new_turtle = Turtle(shape="square")
                new_turtle.shapesize(0.8, 0.8)
                new_turtle.color((112, 128, 144), (178, 34, 34))
                new_turtle.penup()
                if k == 0:
                    new_turtle.goto(i, 300)
                elif k == 1:
                    new_turtle.goto(300, i)
                elif k == 2:
                    new_turtle.goto(i, -300)
                elif k == 3:
                    new_turtle.goto(-300, i)


    def obstacle_walls(self):
        '''Creates obstacles on the field'''
        for _ in range(random.randint(5, 20)):
            new_turtle = Turtle(shape="square")
            new_turtle.shapesize(0.8, 0.8)
            new_turtle.color((112, 128, 144), (178, 34, 34))
            new_turtle.penup()
            new_turtle.goto(random.randrange(-280, 280, 20), random.randrange(-280, 280, 20))
            check_positions(new_turtle)
            self.obstacles.append(new_turtle)


class Scoreboard(Turtle):
    '''A Scoreboard Object'''

    def __init__(self, teleportation, rand_obstacles):
        self.teleportation = teleportation
        self.rand_obstacles = rand_obstacles
        super().__init__()
        try:
            score_data = open("data.txt", encoding="utf-8")
            self.scores = score_data.read().split()
        except ValueError:
            self.scores = [0, 0, 0, 0]
        except:
            self.scores = [0, 0, 0, 0]
            with open("data.txt", "w", encoding="utf-8") as dat:
                for _ in range(4):
                    dat.write("0" + "\n")

        options = Turtle()
        options.color("white")
        options.ht()
        options.pu()
        options.goto((0, -345))

        if teleportation is None and rand_obstacles is None:
            h_score = int(self.scores[0])
            options.write("Teleportation: OFF | Obstacles: OFF", font=FONT2, align=ALIGNMENT)
        elif teleportation is None:
            h_score = int(self.scores[1])
            options.write("Teleportation: OFF | Obstacles: ON", font=FONT2, align=ALIGNMENT)
        elif rand_obstacles is None:
            h_score = int(self.scores[2])
            options.write("Teleportation: ON | Obstacles: OFF", font=FONT2, align=ALIGNMENT)
        else:
            h_score = int(self.scores[3])
            options.write("Teleportation: ON | Obstacles: ON", font=FONT2, align=ALIGNMENT)

        self.score = -1
        self.high_score = h_score
        self.color("white")
        self.hideturtle()
        self.penup()
        self.sety(310)
        self.refresh("standard")


    def refresh(self, fruit):
        '''Refreshes the score of the food'''
        if fruit == "standard":
            self.score += 1
        elif fruit == "bonus":
            self.score += 3
        self.clear()
        self.write(f"Score: {self.score} High Score: {self.high_score}", font=FONT, align=ALIGNMENT)


    # def game_over(self):
    #     '''Announces Game Over'''
    #     self.goto(0, 0)
    #     self.write("GAME OVER!", align=ALIGNMENT, font=FONT)


    def reset(self):
        '''Writes the high score'''
        if self.score > self.high_score:
            self.high_score = self.score

            if self.teleportation is None and self.rand_obstacles is None:
                self.scores[0] = self.score
            elif self.teleportation is None:
                self.scores[1] = self.score
            elif self.rand_obstacles is None:
                self.scores[2] = self.score
            else:
                self.scores[3] = self.score

            with open("data.txt", "w", encoding="utf-8") as dat:
                for score in self.scores:
                    dat.write(f"{score}\n")


        self.score = 0
        self.refresh(0)
