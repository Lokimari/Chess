#  Homework #15: Chess (Part 1)
# Create a `Board` class. This class should have 1 property, `spaces`, that is an 8x8 list of lists initialized to None.
# In addition, this class should have a method named `display` that prints out something similar to the following example.
# And, to clarify, `display` should be printing each cell in `spaces` - do not hard code it. You're going to have to explicitly handle converting None into a string.
#
# Example:
#     a b c d e f g h
# 8 [ _ _ _ _ _ _ _ _ ]
# 7 [ _ _ _ _ _ _ _ _ ]
# 6 [ _ _ _ _ _ _ _ _ ]
# 5 [ _ _ _ _ _ _ _ _ ]
# 4 [ _ _ _ _ _ _ _ _ ]
# 3 [ _ _ _ _ _ _ _ _ ]
# 2 [ _ _ _ _ _ _ _ _ ]
# 1 [ _ _ _ _ _ _ _ _ ]
#
# then
# Create a `main` function that...
# 1. Creates a Board
# 2. (in an infinite loop) displays the board, prompts the user for input, saves the user's input to a variable, and then prints the user's input back to them

# Homework #15: Chess Movement (Part 2)
# 1. Create a `King` piece that implements `__str__`. Then, create a method,
# `King#can_move(cur_x, cur_y, new_x, new_y)`
# that returns true if the king is allowed to move from their current position to the new position.
# For example, `king.can_move(5, 5, 6, 5)` (moving 1 space to the right) should return true, but `king.can_move(5, 5, 7, 5)` (moving 2 spaces to the right) should return false.
#
# 2. Create a method, `Board#move(old_x, old_y, new_x, new_y)`, that when called either...
# (1) prints that there is no piece in position (old_x, old_y) to move,
# (2) prints that a move is illegal based on the results of calling `can_move`, or
# (3) moves the piece from the original position to the new position and prints something along the lines of 'moved piece from old_x, old_y to new_x, new_y'
#
# 3. (extra credit) give the king a `name` property, so that you can print a nicer message (e.g. 'moved piece.name from old_x, old_y to new_x, new_y')
#
# Notes:
# * The user input is not being used at this point. Test your program by manually placing a king on the board and moving it. For example...
# chess_board.spaces[3][3] = King()
# chess_board.display()
# chess_board.move(3, 3, 4, 3) # should move piece and print nice message
# chess_board.display()
# chess_board.move(3, 3, 7, 3) # should not move piece and print illegal move
# chess_board.display() # should not have changed positions
#
# * Feel free to implement more pieces; but, do not implement pawns yet since they have team-dependent movement.
# * All chess coordinates are based on list indices (index-es) at this point. Using a chess-based coordinate system (e.g. "a6", "e5") is its own feature and will come at a later point in time.

# there's 4 things that need to happen for pawns:
# 1. orientation
# 2. team / owner
# 3. has_moved / last_moved_turn (for the first move and eventually en passants)
# 4. most likely passing board at the end of can_move as an optional argument
#
# we'll build up to the pawns after establishing  ChessGame (i.e. a chess match). that way we have the piece orientation and teams worked out
# to keep slowly building things up, here's 2 suggestions:
#
# 1) Add a color property to every piece that defaults to "white". Using the colored function from termcolor in conjunction with colorama (both external libraries)
# you should be able to create colored pieces (e.g. King(color="magenta"). Here's a basic sample using these libraries:
# from colorama import init
# from termcolor import colored
#
# # Makes it so that colored text gets properly escaped in Windows.
# init()
#
# print(colored("Boop", "cyan"))
#
#
# 2) Create a Vec2 class that has x and y properties. Use it to simplify the program (e.g. old_x and old_y is really old = Vec2(x, y); old.x; old.y

from colorama import init
from termcolor import colored

class ChessBoard:
    def __init__(self):
        self.spaces = []
        self.build()

    def build(self):
        for x in range(0,8):
            self.spaces.append([None for space in range(0, 8)])

    def display(self):
        # row_num = 8
        row_num = 1
        board_string = "    1 2 3 4 5 6 7 8"
        for row in self.spaces:
            board_string += "\n" + str(row_num) + " [ "
            row_num += 1
            # row_num -= 1
            for val in row:
                if val is None:
                    board_string += "_ "
                else: board_string += str(val) + " "
            board_string += "]"

        print(board_string)

    def move(self, cur, new):

        if not self.in_board(cur) or not self.in_board(new):
            print("Out of bounds")
            return

        piece = self.spaces[cur.x][cur.y]

        if piece is None:
            print("No piece in space")
        else:
            if piece.can_move(cur, new):
                print("Moving...")
                self.spaces[new.x][new.y] = piece
                self.spaces[cur.x][cur.y] = None
            else:
                print("ILLEGAL")


    def in_board(self, pos):
        print(pos)
        return not (pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7)

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x)+ "," + str(self.y) + ")"

class King:
    def __init__(self):
        self.name = "King"
        self.color = "white"
    def __str__(self):
        return colored("K", self.color)

    def can_move(self, cur, new):
        return abs(new.y - cur.y) <= 1 and abs(new.x - cur.x) <= 1

class Queen:
    def __init__(self):
        self.name = "Queen"
        self.color = "white"
    def __str__(self):
        return colored("Q", self.color)

    def can_move(self, cur, new):
        return (new.x == cur.x or new.y == cur.y or
               (cur.x - cur.y == new.x - new.y) or
               (cur.x + cur.y == new.x + new.y))

class Bishop:
    def __init__(self):
        self.name = "Bishop"
        self.color = "white"
    def __str__(self):
        return colored("B", self.color)

    def can_move(self, cur, new):
        return ((cur.x - cur.y == new.x - new.y) or
                (cur.x + cur.y == new.x + new.y))

class Rook:
    def __init__(self):
        self.name = "Rook"
        self.color = "white"
    def __str__(self):
        return colored("R", self.color)

    def can_move(self, cur, new):
        return new.x == cur.x or new.y == cur.y

class Knight:
    def __init__(self):
        self.name = "Knight"
        self.color = "white"
    def __str__(self):
        return colored("H", self.color)

    def can_move(self, cur, new):
        return (((abs(new.x - cur.x) == 2) and abs(cur.y - new.y) == 1) or
                ((abs(new.x - cur.x) == 1) and abs(cur.y - new.y) == 2))

# Example input: 3,3,4,4 - move piece in space 3,3 to space 4,4 if possible
def move_from_string(string):
    inputs = [int(num) - 1 for num in string.split(",")]
    cur_x, cur_y, new_x, new_y = inputs
    return [Vec2(cur_x, cur_y), Vec2(new_x, new_y)]


def main():
    the_king = King()
    a_bishop = Bishop()
    a_rook = Rook()
    a_pony = Knight()
    queenie = Queen()
    chess_board = ChessBoard()
    chess_board.spaces[3][3] = queenie
    chess_board.spaces[2][3] = a_bishop
    chess_board.spaces[7][7] = the_king
    chess_board.spaces[3][4] = a_rook
    chess_board.spaces[4][4] = a_pony

    while True:
        chess_board.display()
        move = input("Enter move: ")
        try:
            cur, new = move_from_string(move)
            chess_board.move(cur, new)
        except ValueError:
            print("Invalid Input")

if __name__ == "__main__":
    main()
