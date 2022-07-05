"""Main Brain for the Snakes and Ladders Game"""

from sys import exit as sysexit
from random import randint
from time import sleep
from turtle import Screen, Turtle
from math import ceil
import data
from data import Player, Dice, positions, snakes, ladders


# TODO Use tkinter to display a dialog box for choosing colors
# TODO Use Tkinter to display a proper dialog for stabbing
# TODO Make the game window resizable
# TODO Make the game playable for up to 4 players
# TODO Add names to figures
# TODO Make Dice look like dice instead of using numbers


FONT = ("Calibri", "16", "bold")
FONT2 = ("Calibri", "12", "normal")
ALIGN = "center"
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1200

# Create main window
def create_window():
    """Creates the main window for the Snakes and Ladders Game"""
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.bgcolor("black")
    screen.bgpic(r"board.png")
    screen.colormode(255)
    screen.title("Snakes And Ladders")

    SnakesAndLadders()

    screen.listen()
    screen.mainloop()


class SnakesAndLadders:
    """Executes the game Snakes And Ladders"""

    def __init__(self):

        # Defining Info Box
        self.info = Turtle()
        self.info.speed(0)
        self.info.pu()
        self.info.ht()
        self.info.color("white")
        self.info.goto(-775, -350)
        self.prev_text = ["", "", "", "", "", ""]

        self.pl1 = Player(1)
        self.pl2 = Player(2)
        self.curr_player  = self.pl1
        self.other_player = self.pl2

        self.first_roll = 0
        self.roll_define = 0
        self.attacks = True
        self.dice_lock = False

        # Player name input
        self.scr = Screen()
        self.canvas = self.scr.getcanvas()
        self.canvas.bind('<1>', self.check_mouse_pos)
        self.dice = Dice()

        self.start_game()


    def start_game(self):
        """Executing the game"""

        # Asks players if they want to have stabbing in the game!
        self.ask_enable_stabbing()

        sleep(0.5)
        self.info_box(f"{self.pl1.name} press the Dice to Roll it", self.prev_text.copy())


    def ask_enable_stabbing(self):
        """Executes the stabbing dialog"""

        stabbing = self.scr.textinput("Stabbing", "Do you want stabbing to be enabled?\n"\
            "Type 'Info' for more info on 'Stabbing'")

        # If 'No' was typed - stabbing is turned Off
        if stabbing is None:
            self.attacks = False

        # If 'Yes' was typed - stabbing is turned On
        elif stabbing.lower() not in ("i", "info"):
            self.info_box("Stabbing is On", self.prev_text.copy())

        # If 'Info' was typed - Info text is displayed
        else:
            text = "Stabbing is when Player 'A' reaches\nthe same position as the Player 'B'.\n" \
                "This results in Player 'B'\nresetting their position back to 0!"
            self.info_box(text, self.prev_text.copy())
            self.ask_enable_stabbing()


    def check_mouse_pos(self, event):  # pylint: disable=unused-argument
        """Checks if mouse position is on the Dice and decides if this roll should
        determine player turn or it's an actual move

        Args:
            event (tkinter.event): A standard argument for functions that have binding in tkinter
        """
        # Calculate the mouse position on the board the same way the turtle onscreenclick command does
        xpos, ypos = ceil(event.x-self.canvas.winfo_width()/2-2), ceil(self.canvas.winfo_height()/2-event.y+2)

        if not self.dice_lock:
            self.dice_lock = True
            if 604 < xpos < 715 and -580 < ypos < -470:
                if self.roll_define < 2:
                    self.first_turn()
                else:
                    self.moves()
            self.dice_lock = False
        else:
            print("Wait for the other player to finish their turn!") #! Testing


    def first_turn(self):
        """Rolls the Dice to choose who's going to Roll first"""
        roll = self.dice_roll()
        if self.roll_define == 0:
            self.pl1.roll = roll
            self.info_box(f"{self.pl1.name} rolled : {self.pl1.roll}", self.prev_text.copy())
        elif self.roll_define == 1:
            self.pl2.roll = roll
            self.info_box(f"{self.pl2.name} rolled : {self.pl2.roll}", self.prev_text.copy())

            self.first_roll = self.first_roll_check()

        self.roll_define += 1


    def first_roll_check(self):
        """Desides which player is going to roll first in the game"""

        if self.pl1.roll > self.pl2.roll:
            self.info_box(f"{self.pl1.name} rolls first!", self.prev_text.copy())
            return self.pl1.name

        elif self.pl2.roll > self.pl1.roll:
            self.curr_player = self.pl2
            self.other_player = self.pl1
            self.info_box(f"{self.pl2.name} rolls first!", self.prev_text.copy())
            return self.pl2.name

        else:
            self.roll_define = -1
            self.info_box("Roll again!", self.prev_text.copy())


    def moves(self):
        """Defines Player movement"""

        self.curr_player.roll = self.dice_roll()
        self.game_roll()

        if self.curr_player.roll != 6:
            self.roll_define += 1
            self.curr_player, self.other_player  = self.other_player, self.curr_player


    def board(self):
        """Snakes and Ladders logic"""

        if self.curr_player.position[0] in ladders:
            self.update_figure_positions()
            self.info_box(f"{self.curr_player.name}, you encountered a ladder!\nCongrats!\n" \
                f"Your position changes from {self.curr_player.position[0]} to {ladders[self.curr_player.position[0]]}", self.prev_text.copy())
            self.curr_player.position[0] = ladders[self.curr_player.position[0]]
            self.update_figure_positions()

            return self.curr_player.position

        if self.curr_player.position[0] in snakes:
            self.update_figure_positions()
            self.info_box(f"{self.curr_player.name}, you encountered a snake!\nSorry!\n" \
                f"Your position changes from {self.curr_player.position[0]} to {snakes[self.curr_player.position[0]]}", self.prev_text.copy())
            self.curr_player.position[0] = snakes[self.curr_player.position[0]]
            self.update_figure_positions()

            return self.curr_player.position


    def dice_roll(self):
        """Rolls the Dice"""
        self.scr.delay(0.1)
        result = randint(1, 6)
        for _ in range(9):
            new_result = randint(1, 6)
            while new_result == result:
                new_result = randint(1, 6)
            result = new_result
            self.dice.dice_num.clear()
            self.dice.dice_num.write(result, font=('Calibri', '48', 'bold'), align='center')
            sleep(0.05)
        self.scr.delay(10)

        return result


    def pl_pos_check(self):
        """Check if player has reached the finish line"""
        if self.curr_player.position[0] < 100:
            check = self.board()

            if check is not None:
                self.curr_player.position[0] = check[0]
            return self.curr_player.position

        # If position exceeds 100 then player stays at the same position
        elif self.curr_player.position[0] > 100:
            self.curr_player.position[0] -= self.curr_player.roll
            self.info_box(f"{self.curr_player.name}'s position remains : {self.curr_player.position[0]}", self.prev_text.copy())
            return self.curr_player.position

        # If position is 100 - Congradulates the winner and asks if a new game should be started
        self.info_box(f"{self.curr_player.name}, you WIN!!! Congrats!", self.prev_text.copy())
        self.new_game()


    def game_roll(self):
        """Rolling the dice in the game"""

        self.info_box(f'{self.curr_player.name} rolled : {self.curr_player.roll}', self.prev_text.copy())
        self.curr_player.position[0] += self.curr_player.roll

        snl_pos = self.curr_player.position[0]
        self.curr_player.position = self.pl_pos_check()
        if snl_pos == self.curr_player.position[0]:
            self.update_figure_positions()

        # Resets player position if stabbing is turned 'On'
        if self.attacks is True and self.curr_player.position == self.other_player.position:
            self.info_box(f"Sorry {self.other_player.name},\n{self.curr_player.name} stabbed you from behind!\n"
                    "You're back to position 0!", self.prev_text.copy())
            self.other_player.position[0] = 0

            figs = [self.pl1.figure, self.pl2.figure]
            figs.remove(self.curr_player.figure)

            self.update_figure_positions(self.other_player)


    def new_game(self):
        """Rematch dialog"""

        rematch = self.scr.textinput("New Game?", "Do you want to start a new game?: ")

        # Restart the game if 'yes' was typed
        if rematch is not None:
            if rematch.lower() not in ["no", "n", "0", "x"]:
                self.scr.clearscreen()
                data.PLAYER_NAMES = []
                data.PLAYER_COLORS = ["Red", "Green", "Blue", "Yellow"]
                create_window()

        # Announce the winner and quit!
        else:

            if self.pl1.position[0] > self.pl2.position[0]:
                self.info_box(f"Congrats to {self.pl1.name} for the win!", self.prev_text.copy())

            elif self.pl2.position[0] > self.pl1.position[0]:
                self.info_box(f"Congrats to {self.pl2.name} for the win!", self.prev_text.copy())

            else:
                self.info_box("It's a draw!", self.prev_text.copy())

            self.info_box("Goodbye!", self.prev_text.copy())
            sleep(1)
            sysexit()


    def info_box(self, text, prev_text):
        """
        Takes text and displays it into the Info Box
        Allows the info to disappear on screen click
        """

        pos1 = -775
        pos2 = -200
        self.info.clear()

        self.info.write(text, font=FONT, align=ALIGN)

        self.info.goto(pos1, pos2)
        self.info.write(self.prev_text[0], font=FONT2, align=ALIGN)

        pos2 += 80

        for txt in prev_text[1:]:
            self.info.goto(pos1, pos2)
            self.info.write(txt, font=FONT2, align=ALIGN)
            pos2 += 80

        for index, txt in enumerate(prev_text[1:]):
            self.prev_text[index+1] = prev_text[index]

        self.prev_text[0] = text
        self.info.goto(-775, -350)


    def update_figure_positions(self, player=None):
        """Updates Player Positions"""

        if player is None:
            player = self.curr_player

        player.figure.clear()
        player.figure.pd()
        player.figure.goto(positions[player.position[0]])
        player.figure.pu()


if __name__ == "__main__":
    create_window()
