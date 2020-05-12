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
        # Top team
        for num in range(0,8):
            self.board.spaces[1][num] = Pawn(team=2, color="magenta")
        self.board.spaces[0][0] = Rook(team=2, color="magenta")
        self.board.spaces[0][7] = Rook(team=2, color="magenta")
        self.board.spaces[0][1] = Knight(team=2, color="magenta")
        self.board.spaces[0][6] = Knight(team=2, color="magenta")
        self.board.spaces[0][2] = Bishop(team=2, color="magenta")
        self.board.spaces[0][5] = Bishop(team=2, color="magenta")
        self.board.spaces[0][3] = King(team=2, color="magenta")
        self.board.spaces[0][4] = Queen(team=2, color="magenta")

        # Bottom Team
        for num in range(0,8):
            self.board.spaces[6][num] = Pawn(team=1, color="yellow")
        self.board.spaces[7][0] = Rook(team=1, color="yellow")
        self.board.spaces[7][7] = Rook(team=1, color="yellow")
        self.board.spaces[7][1] = Knight(team=1, color="yellow")
        self.board.spaces[7][6] = Knight(team=1, color="yellow")
        self.board.spaces[7][2] = Bishop(team=1, color="yellow")
        self.board.spaces[7][5] = Bishop(team=1, color="yellow")
        self.board.spaces[7][3] = King(team=1, color="yellow")
        self.board.spaces[7][4] = Queen(team=1, color="yellow")

# Error Handling
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

    # Board printing with variable x/y labels
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

    # Takes Vec2 of current space and destination space, checks each, moves, and sets piece attr "has_moved" = True
    def move(self, move, player_team):
        # vars
        cur = move.old
        new = move.new
        piece = self.spaces[cur.x][cur.y]
        dest = self.spaces[new.x][new.y]

        # Movement logic

        # Preliminary error checks
        if not self.in_board(cur) or not self.in_board(new):
            raise OutOfBounds()


        if not piece.team == player_team:
            raise ThatsNotUrFuckinTeam()

        if piece is None:
            raise NoPieceInSpace()
        else:
            # Movement - To-do: get rid of redundancy here
            if piece.can_move(move):
                if dest is None:
                    print("Moving...")
                    print(move)
                    setattr(self.spaces[cur.x][cur.y], 'has_moved', True)  # So pawns can't do wacky stuff
                    # The actual movement
                    self.spaces[new.x][new.y] = piece
                    self.spaces[cur.x][cur.y] = None
                elif dest is not None and getattr(dest, "team") is player_team:
                    print("You arleady have a piece there")
                else:
                    print("Moving...")
                    print(move)
                    print(str(getattr(dest, "name") + " taken"))
                    setattr(self.spaces[cur.x][cur.y], 'has_moved', True)  # So pawns can't do wacky stuff
                    # The actual movement
                    self.spaces[new.x][new.y] = piece
                    self.spaces[cur.x][cur.y] = None
            else:
                raise IllegalMove()

    # Checking bounds
    def in_board(self, pos):
        return not (pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7)

# Move History (unfinished)
class Move:
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __str__(self):
        return str(self.old) + " -> " + str(self.new)

# For neatly storing coordinates as class objects
class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

# ####################################################Pieces############################################################
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
                  ((move.new.x - move.old.x ==  2 or move.new.x - move.old.x ==  1) and self.team == 2)) if self.has_moved == False else False)))

########################################################################################################################

# Movement input, example input: 3,3,4,4 - move piece in space 3,3 to space 4,4 if possible
def move_from_string(string):
    inputs = [int(num) for num in string.split(",")]
    cur_x, cur_y, new_x, new_y = inputs
    return Move(Vec2(cur_x, cur_y), Vec2(new_x, new_y))


def main():
    game = ChessGame()
    game.run()


if __name__ == "__main__":
    main()
