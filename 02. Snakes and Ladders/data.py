'''The UI for the game Snakes And Ladders'''
# Imported Libraries
from turtle import Turtle, Screen
from sys import exit as sysexit

PLAYER_NAMES = [""]
PLAYER_COLORS = ["Red", "Green", "Blue", "Yellow"]


positions = {
    "pl1_start":(-660, -500),
    "pl2_start":(-660, -550),
    "dice_pos":(660, -525),
    "dice_num_pos":(660, -560),
    0:(-660, -525),
    1:(-540, -525),
    2:(-430, -525),
    3:(-310, -525),
    4:(-190, -525),
    5:(-70, -525),
    6:(60, -525),
    7:(180, -525),
    8:(300, -525),
    9:(425, -525),
    10:(545, -525),
    11:(540, -410),
    12:(420, -410),
    13:(300, -410),
    14:(180, -410),
    15:(60, -410),
    16:(-70, -410),
    17:(-190, -410),
    18:(-310, -410),
    19:(-430, -410),
    20:(-540, -410),
    21:(-540, -290),
    22:(-430, -290),
    23:(-310, -290),
    24:(-190, -290),
    25:(-70, -290),
    26:(60, -290),
    27:(180, -290),
    28:(300, -290),
    29:(420, -290),
    30:(540, -290),
    31:(540, -170),
    32:(420, -170),
    33:(300, -170),
    34:(175, -170),
    35:(60, -170),
    36:(-65, -170),
    37:(-180, -170),
    38:(-300, -170),
    39:(-420, -170),
    40:(-540, -170),
    41:(-535, -60),
    42:(-417, -60),
    43:(-300, -60),
    44:(-180, -60),
    45:(-60, -60),
    46:(55, -60),
    47:(175, -60),
    48:(295, -60),
    49:(415, -60),
    50:(535, -60),
    51:(530, 55),
    52:(410, 55),
    53:(290, 55),
    54:(170, 55),
    55:(50, 55),
    56:(-60, 55),
    57:(-180, 55),
    58:(-300, 55),
    59:(-420, 55),
    60:(-535, 55),
    61:(-540, 170),
    62:(-420, 170),
    63:(-300, 170),
    64:(-180, 170),
    65:(-60, 170),
    66:(55, 170),
    67:(175, 170),
    68:(295, 170),
    69:(410, 170),
    70:(530, 170),
    71:(540, 290),
    72:(420, 290),
    73:(300, 290),
    74:(180, 290),
    75:(60, 290),
    76:(-65, 290),
    77:(-185, 290),
    78:(-300, 290),
    79:(-420, 290),
    80:(-540, 290),
    81:(-540, 405),
    82:(-420, 405),
    83:(-300, 405),
    84:(-180, 405),
    85:(-60, 405),
    86:(60, 405),
    87:(180, 405),
    88:(300, 405),
    89:(420, 405),
    90:(540, 405),
    91:(540, 520),
    92:(420, 520),
    93:(300, 520),
    94:(180, 520),
    95:(60, 520),
    96:(-65, 520),
    97:(-185, 520),
    98:(-305, 520),
    99:(-425, 520),
    100:(-540, 520),
}

ladders = {
    3:20, 11:28, 15:34,
    17:74,22:37,38:59,
    49:67, 52:71, 57:76,
    61:78, 73:86, 81:98, 88:91,
    }

snakes = {
    26:10, 39:5, 51:6,
    54:36, 56:1, 60:23,
    75:28, 83:45, 85:59,
    90:48, 92:25, 97:87, 99:63,
    }

class Player:
    """Creates a Player"""

    def __init__(self, player: int):
        self.player = player

        self.position = [0]
        self.roll = 0

        self.figure = Turtle(shape="circle", visible=False)
        self.figure.pu()
        self.figure.pensize(5)
        self.figure.speed(0)
        self.figure.goto(positions[f"pl{self.player}_start"])
        self.figure.shapesize(2, 2, 5)
        self.figure.color("black", "white")
        self.figure.st()
        self.figure.speed(6)

        self.screen = Screen()
        self.name = self.choose_name()
        self.choose_color()


    def choose_name(self):
        """Choose Player Name"""

        name = self.screen.textinput(f"Player {self.player}", f"Please Enter Player {self.player}'s name: ")
        while True:
            if name is None:
                sysexit()
            elif name in PLAYER_NAMES:
                name = self.screen.textinput(f"Player {self.player}", f"Please Enter Player {self.player}'s name: ")
            else:
                PLAYER_NAMES.append(name)
                self.figure.write(" ")
                return name


    def choose_color(self):
        """Choose Player color"""

        color = self.screen.textinput(
            f"{self.name} Color", f"{self.name}, Please Enter the desired color!\n" \
                f"Choose from {str(PLAYER_COLORS).strip('()')}")

        if color is not None:
            while color.title() not in PLAYER_COLORS:
                color = self.screen.textinput(
                    f"{self.name} Color", f"{self.name}, Please Enter the desired color!\n" \
                        f"Choose from {str(PLAYER_COLORS).strip('()')}")
            PLAYER_COLORS.remove(color.title())
            self.figure.color("dark goldenrod", color) if color.lower() == "yellow" else self.figure.color(f"dark {color}", color) # pylint: disable=expression-not-assigned
        else:
            sysexit()


class Dice:
    '''All Turtles for the Snakes And Ladders game'''

    def __init__(self):
        # Turtle
        self.dice = Turtle(shape="square", visible=False)
        self.dice_num = Turtle(visible=False)

        # Deactivating the pen
        self.dice.pu()
        self.dice_num.pu()

        # Setting the speed to 0 for faster start
        self.dice.speed(0)
        self.dice_num.speed(0)

        # Moves thte Turtle to its starting posiitons
        self.dice.goto(positions["dice_pos"])
        self.dice_num.goto(positions["dice_num_pos"])

        # Tuning the size and color for the Turtle
        self.dice.shapesize(5, 5, 10)
        self.dice.color((50, 50, 50), "white")

        # Shows the Turtle and sets the speed back to normal
        self.dice.st()
        self.dice.speed(6)
        self.dice_num.speed(6)
