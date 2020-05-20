from termcolor import colored
import datatypes
import moves

class King:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "King"
        self.has_moved = has_moved

    def __str__(self):
        return colored("K", self.color)

    def can_move(self, move, board):
        return moves.can_kingly_movement(move, board) or moves.can_castle(move, board)

    def do_move(self, move, board):
        if moves.can_castle(move, board):
            board.castle(move)
        else:
            board.move(move)

class Queen:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Queen"
        self.has_moved = has_moved

    def __str__(self):
        return colored("Q", self.color)

    def can_move(self, move, board):
        return moves.can_move_diagonally(move, board) or moves.can_move_xy(move, board)

    def do_move(self, move, board):
        board.move(move)

class Bishop:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Bishop"
        self.has_moved = has_moved

    def __str__(self):
        return colored("B", self.color)

    def can_move(self, move, board):
        return moves.can_move_diagonally(move, board)

    def do_move(self, move, board):
        board.move(move)


class Rook:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Rook"
        self.has_moved = has_moved

    def __str__(self):
        return colored("R", self.color)

    def can_move(self, move, board):
        return moves.can_move_xy(move, board)

    def do_move(self, move, board):
        board.move(move)


class Knight:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Knight"
        self.has_moved = has_moved

    def __str__(self):
        return colored("H", self.color)

    def can_move(self, move, board):
        return moves.can_horsey_jump(move, board)

    def do_move(self, move, board):
        board.move(move)


class Pawn:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Pawn"
        self.has_moved = has_moved
        self.forward = (datatypes.Vec2(0, -1) if team == 1 else datatypes.Vec2(0, 1))
        self.left = datatypes.Vec2(-self.forward.y, self.forward.x)

    def __str__(self):
        return colored("P", self.color)

    def can_move(self, move, board):
        return moves.can_pawn_move(self, move, board)

    def do_move(self, move, board):
        board.move(move)
