from termcolor import colored
import datatypes
import moves

class Piece:
    def __init__(self, team, name, symbol):
        self.color = "yellow" if team == 1 else "magenta"
        self.team = team
        self.name = name
        self.has_moved = False
        self.move_counter = 0
        self.symbol = symbol

    def __str__(self):
        return colored(self.symbol, self.color)

    def can_move(self, move, board):
        raise Exception("Unimplemented")

    def do_move(self, move, board):
        raise Exception("Unimplemented")

class King(Piece):
    def __init__(self, team, is_castling=False):
        super().__init__(team, name="King", symbol="K")
        self.is_castling = is_castling

    def can_move(self, move, board):
        return moves.can_kingly_movement(move, board) or moves.can_castle(move, board)

    def is_castling_move(self, move, board):
        self.is_castling = moves.is_castling(move, board)

    def do_move(self, move, board):
        if moves.can_castle(move, board):
            board.castle(move)
        else:
            board.move(move)

class Queen(Piece):
    def __init__(self, team):
        super().__init__(team, name="Queen", symbol="Q")

    def can_move(self, move, board):
        return moves.can_move_diagonally(move, board) or moves.can_move_xy(move, board)

    def do_move(self, move, board):
        board.move(move)

class Bishop(Piece):
    def __init__(self, team):
        super().__init__(team, name="Bishop", symbol="B")

    def can_move(self, move, board):
        return moves.can_move_diagonally(move, board)

    def do_move(self, move, board):
        board.move(move)


class Rook(Piece):
    def __init__(self, team):
        super().__init__(team=team, name="Rook", symbol="R")

    def can_move(self, move, board):
        return moves.can_move_xy(move, board)

    def do_move(self, move, board):
        board.move(move)


class Knight(Piece):
    def __init__(self, team):
        super().__init__(team=team, name="Knight", symbol="H")

    def can_move(self, move, board):
        return moves.can_horsey_jump(move, board)

    def do_move(self, move, board):
        board.move(move)


class Pawn(Piece):
    def __init__(self, team):
        super().__init__(team, name="Pawn", symbol="P")
        self.forward = (datatypes.Vec2(0, -1) if team == 1 else datatypes.Vec2(0, 1))
        self.left = datatypes.Vec2(-self.forward.y, self.forward.x)

    def can_move(self, move, board):
        return moves.can_pawn_move(self, move, board)

    def do_move(self, move, board):
        board.move(move)
