'''Main Brain for the Snakes and Ladders Game'''
# Imported Libraries
import sys
import random


LADDERS = {
    3:20, 11:28, 15:34,
    17:74,22:37,38:59,
    49:67, 52:71, 57:76,
    61:78, 73:86, 81:98, 88:91,
    }

SNAKES = {
    26:10, 39:5, 51:6,
    54:36, 56:1, 60:23,
    75:28, 83:45, 85:59,
    90:48, 92:25, 97:87, 99:63,
    }


class SnakesAndLadders:
    '''Executes the game Snakes And Ladders'''

    def __init__(self):

        # Player Positions
        self.p1_pos = [0]
        self.p2_pos = [0]
        self.player_first_roll = 0
        self.attacks = True

        # Player name input
        self.player1 = input("Please Enter the name of the first player: ")
        self.player2 = input("Please Enter the name of the second player: ")

        self.start_game()


    def start_game(self):
        '''Executing the game'''

        # Players choose their colors
        self.player1_color = input(
            f"{self.player1}, choose a color : 1 = Red, 2 = Blue, 3 = Green, 4 = Yellow\n")

        self.player_color(self.player1_color, self.player1)

        self.player2_color = input(
            f"{self.player2}, choose a color : 1 = Red, 2 = Blue, 3 = Green, 4 = Yellow\n")

        self.player_color(self.player2_color, self.player2)

        # Asks players if they want to have stabbing in the game!
        stabs()

        # Execution of first dice roll!
        self.first_roll()

        # Checks who rolls the dice first!
        if self.player_first_roll == 1:
            self.game_roll(self.player1, self.player2, self.p1_pos, self.p2_pos)

        if self.player_first_roll == 2:
            self.game_roll(self.player2, self.player1, self.p2_pos, self.p1_pos)


    def player_color(self, input_color, player):
        '''Assigning colors to Players'''

        # Looks for 'x' to close the game
        x_to_exit(input_color)

        if player == self.player2 and input_color == self.player1_color:
            print(f"{self.player1} already took that color!")
            input_color = input(
                f"{player}, choose a color : 1 = Red, 2 = Blue, 3 = Green, 4 = Yellow\n")
            self.player_color(input_color, player)

        # Pick the color by integer
        elif input_color.isnumeric() and input_color in ("1", "2", "3", "4"):

            colors = {
                "1":"is now red!", "2":"is now Blue!", "3":"is now Green!", "4":"is now Yellow!"
            }
            print(f"{player} {colors[input_color]}")

        else:
            print(f"There's no color assigned to {input_color}, enter a number between 1 and 4")
            input_color = input(
                f"{player}, choose a color : 1 = Red, 2 = Blue, 3 = Green, 4 = Yellow\n")
            self.player_color(input_color, player)


    def first_roll(self):
        '''Desides which player is going to roll first in the game'''

        pl1 = input(f"{self.player1} press Enter to roll the dice or x to quit the game ")

        # Looks for 'x' to close the game
        x_to_exit(pl1)

        p1_roll = dice_roll()
        print(f"{self.player1} rolled : {p1_roll}")

        pl2 = input(f"{self.player2} press Enter to roll the dice or x to quit the game ")

        # Looks for 'x' to close the game
        x_to_exit(pl2)

        p2_roll = dice_roll()
        print(f"{self.player2} rolled : {p2_roll}")

        if p1_roll > p2_roll:
            print("-"*20)
            print(f"{self.player1} rolls first")
            print("-"*20)
            self.player_first_roll = 1

        elif p2_roll > p1_roll:
            print("-"*20)
            print(f"{self.player2} rolls first")
            print("-"*20)
            self.player_first_roll = 2

        else:
            print("-"*10)
            print("Roll again")
            print("-"*10)

            self.first_roll()


    def pl_pos_check(self, roll, pos, player):
        '''Check if player has reached the finish line'''
        if pos[0] < 100:
            print(f"{player}'s position is : {pos[0]}\n")
            check = board(pos, player)

            if check is not None:
                pos[0] = check[0]
            return pos

        # If position exceeds 100 then player stays at the same position
        elif pos[0] > 100:
            pos[0] -= roll
            print(f"{player}'s position remains : {pos[0]}\n")
            return pos

        # If position is 100 - Congradulates the winner and asks if a new game should be started
        print(f"{player}, you WIN!!! Congrats\nDo you want to start a new game?")
        self.new_game()


    def game_roll(self, curr_player, other_player, curr_pos, other_pos):
        '''Rolling the dice in the game'''

        input_ = input(f"{'-'*50}\n{curr_player} press Enter to roll the dice ")

        # Checks if 'x' is typed to close the game
        x_to_exit(input_)

        roll = dice_roll()

        print(f'{curr_player} rolled : {roll}')
        curr_pos[0] += roll

        curr_pos = self.pl_pos_check(roll, curr_pos, curr_player)

        # Resets player position if stabbing is turned 'On'
        if self.attacks is True and curr_pos == other_pos:
            print(f"Sorry {other_player}, {curr_player} stabbed you from behind!"
                    " You're back to position 0!")
            other_pos[0] = 0

        if roll == 6:
            self.game_roll(
                curr_player=curr_player, other_player=other_player,
                curr_pos=curr_pos, other_pos=other_pos
            )

        else:
            self.game_roll(curr_player=other_player, other_player=curr_player,
                            curr_pos=other_pos, other_pos=curr_pos
            )


    def new_game(self):
        '''Rematch dialog'''

        rematch = input("Do you want to play another game?\n" \
            "Type Yes to start a new game and No to quit game: ")

        # Restart the game if 'yes' was typed
        if rematch.lower() in ["yes", "y", "1"]:
            self.__init__()

        # Announce the winner and quit!
        elif rematch.lower() in ["no", "n", "0", "x"]:

            if self.p1_pos[0] > self.p2_pos[0]:
                print(f"Congrats to {self.player1} for the win!")

            elif self.p2_pos[0] > self.p1_pos[0]:
                print(f"Congrats to {self.player2} for the win!")

            else:
                print("It's a draw!")

            print("Goodbye!")
            sys.exit()

        else:
            print("You must Enter Yes or No!")
            self.new_game()


def x_to_exit(inp):
    '''Checks if it needs to exit the game'''
    if inp != 'x':
        return
    print('Game closed')
    sys.exit()


def dice_roll():
    '''Rolls the Dice'''
    return random.randint(1,6)


def stabs():
    '''Stabbing dialog'''

    stabbing = input("Do you want stabbing to be enabled?\nType 'Yes' or 'No'" \
            " or type 'Info' for more info on 'stabbing' and 'x' to exit the game\n\n")

    # If 'Yes' was typed - stabbing is turned On
    if stabbing.lower() in ("yes", "y", "1"):
        print("Stabbing is On")

    # If 'No' was typed - stabbing is turned Off
    elif stabbing.lower() in ("no", "n", "0"):
        SnakesAndLadders.attacks = False
        print("Stabbing is Off")

    # If 'Info' was typed - Info text is displayed
    elif stabbing.lower() == "info":
        print("-"*70)
        print("Stabbing is when Player 'A' reaches the same position as the Player 'B'.")
        print("This results in Player 'B' resetting their position back to 0!")
        print("-"*70)
        stabs()

    # If 'x' was typed - the game closes
    elif stabbing.lower() == "x":
        sys.exit()

    # If anything else was typed - show the options and restart the question
    else:
        print("You must enter: 'Yes', 'No', 'Info' or 'x'")
        stabs()


def board(pos, player):
    '''Snakes and Ladders logic'''

    if pos[0] in LADDERS:
        print(f"{player}, you encountered a ladder! " \
            f"Congrats!\nYour position changes from {pos[0]} to {LADDERS[pos[0]]}")
        pos[0] = LADDERS[pos[0]]

        print(f"{player}'s position is : {pos[0]}\n")
        return pos

    if pos[0] in SNAKES:
        print(f"{player}, you encountered a snake! "\
            f"Sorry! Your position changes from {pos[0]} to {SNAKES[pos[0]]}")
        pos[0] = SNAKES[pos[0]]

        print(f"{player}'s position is : {pos[0]}\n")
        return pos


if __name__ == "__main__":
    game = SnakesAndLadders()
