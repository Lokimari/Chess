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

# Allow piece color for cmd
init()


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.setup_pieces()
        self.player_turn = 1

    def run(self):
        while True:
            self.board.display()
            move = input(f"Player {self.player_turn}, enter move: ")
            try:
                move = move_from_string(move)
                self.board.move(move, self.player_turn)
                self.next_player_turn()
            except AttributeError:
                print("Empty space selected.")
            except ValueError:
                print("Invalid Input")
            except NoPieceInSpace:
                print("No Piece in Space!")
            except IllegalMove:
                print("Illegal move!")
            except OutOfBounds:
                print("Out of Bounds!")
            except ThatsNotUrFuckinTeam:
                print("Wrong team, dingus!")

    def next_player_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1

    def setup_pieces(self):
        # self.board.spaces[3][3] = Queen(team=1)
        # self.board.spaces[2][3] = Bishop(team=1)
        # self.board.spaces[7][7] = Rook(team=1)
        # self.board.spaces[3][4] = Knight(team=1)
        self.board.spaces[6][0] = Pawn(team=1, color="yellow")
        self.board.spaces[1][0] = Pawn(team=2, color="magenta")
        # self.board.spaces[4][4] = King(team=1, color="yellow")
        # self.board.spaces[6][6] = King(team=2, color="magenta")


class NoPieceInSpace(Exception):
    pass


class IllegalMove(Exception):
    pass


class OutOfBounds(Exception):
    pass


class ThatsNotUrFuckinTeam(Exception):
    pass


class ChessBoard:
    def __init__(self):
        self.spaces = []
        self.build()

    def build(self):
        for x in range(0, 8):
            self.spaces.append([None for space in range(0, 8)])

    def display(self):
        # row_num = 8
        row_num = 0
        board_string = "    0 1 2 3 4 5 6 7"
        for row in self.spaces:
            board_string += "\n" + str(row_num) + " [ "
            row_num += 1
            # row_num -= 1
            for val in row:
                if val is None:
                    board_string += "_ "
                else:
                    board_string += str(val) + " "
            board_string += "]"

        print(board_string)

    def move(self, move, player_team):
        cur = move.old
        new = move.new

        if not self.in_board(cur) or not self.in_board(new):
            raise OutOfBounds()

        piece = self.spaces[cur.x][cur.y]
        if not piece.team == player_team:
            raise ThatsNotUrFuckinTeam()

        if piece is None:
            raise NoPieceInSpace()
        else:
            if piece.can_move(move):
                print("Moving...")
                print(move)
                self.spaces[new.x][new.y] = piece
                self.spaces[cur.x][cur.y] = None
                # To-do: Change piece's has_moved property to True
            else:
                raise IllegalMove()

    def in_board(self, pos):
        return not (pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7)


class Move:
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __str__(self):
        return str(self.old) + " -> " + str(self.new)


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"


class King:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "King"
        self.has_moved = has_moved

    def __str__(self):
        return colored("K", self.color)

    def can_move(self, move):
        return abs(move.new.y - move.old.y) <= 1 and abs(move.new.x - move.old.x) <= 1


class Queen:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Queen"
        self.has_moved = has_moved

    def __str__(self):
        return colored("Q", self.color)

    def can_move(self, move):
        return (move.new.x == move.old.x or move.new.y == move.old.y or
                (move.old.x - move.old.y == move.new.x - move.new.y) or
                (move.old.x + move.old.y == move.new.x + move.new.y))


class Bishop:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Bishop"
        self.has_moved = has_moved

    def __str__(self):
        return colored("B", self.color)

    def can_move(self, move):
        return ((move.old.x - move.old.y == move.new.x - move.new.y) or
                (move.old.x + move.old.y == move.new.x + move.new.y))


class Rook:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Rook"
        self.has_moved = has_moved

    def __str__(self):
        return colored("R", self.color)

    def can_move(self, move):
        return move.new.x == move.old.x or move.new.y == move.old.y


class Knight:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Knight"
        self.has_moved = has_moved

    def __str__(self):
        return colored("H", self.color)

    def can_move(self, move):
        return (((abs(move.new.x - move.old.x) == 2) and abs(move.old.y - move.new.y) == 1) or
                ((abs(move.new.x - move.old.x) == 1) and abs(move.old.y - move.new.y) == 2))


class Pawn:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Pawn"
        self.has_moved = has_moved

    def __str__(self):
        return colored("P", self.color)

    def can_move(self, move):
        return (((((move.new.x - move.old.x == -1) and self.team == 1) or
                  ((move.new.x - move.old.x == -1) and self.team == 2)) if self.has_moved == True else False) or
               (((((move.new.x - move.old.x == -2 or move.new.x - move.old.x == -1) and self.team == 1) or
                  ((move.new.x - move.old.x ==  2 or move.new.x - move.old.x ==  1) and self.team == 2)) if self.has_moved == False else False, self.has_moved)))


# Example input: 3,3,4,4 - move piece in space 3,3 to space 4,4 if possible
def move_from_string(string):
    inputs = [int(num) for num in string.split(",")]
    cur_x, cur_y, new_x, new_y = inputs
    return Move(Vec2(cur_x, cur_y), Vec2(new_x, new_y))


def main():
    game = ChessGame()
    game.run()


if __name__ == "__main__":
    main()
