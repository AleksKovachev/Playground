'''A Food Class for the Snkae Game'''
# TODO: Make it so that fruit can't be spawned where the snake currently is
import random
import time
from turtle import Turtle
from snake import Snake
from walls import Walls

class Food(Turtle):
    '''A Food Object'''

    COLLISIONS = Snake.SEGMENTS + Walls.obstacles   

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
        self.check_positions(self)
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
            self.check_positions(self.bonus_apple)
            self.bonus_apple.st()

        if self.fruit_spawned and time.time() - self.bonus_counter > 15:
            self.bonus_fruit_eaten()

    def bonus_fruit_eaten(self):
        '''What happens when the Bonus Fruit gets eaten'''
        self.fruit_spawned = False
        self.bonus_counter = time.time()
        self.bonus_apple.ht()
        self.bonus_apple.goto(300, 325)

    def check_positions(self, obj):
        '''Only allows spawning objects at available positions'''
        obj.goto(random.randrange(-280, 280, 20), random.randrange(-280, 280, 20))
        for item in self.COLLISIONS:
            if item.distance(obj) < 15:
                self.check_positions(obj)
