from chess_board import ChessBoard
from datatypes import Vec2
# Piece move logic

# Pawn
def can_an_passant(piece, move, board: ChessBoard):
    left_neighbor = board.get_piece(Vec2(move.old.x - 1, move.old.y))
    right_neighbor = board.get_piece(Vec2(move.old.x + 1, move.old.y))

    if piece.team == 1:
        if move.old.y == 3:
            if left_neighbor is not None:
                if left_neighbor.name == "Pawn" and left_neighbor.move_counter == 1 and left_neighbor.team != piece.team:
                    board.spaces[move.old.y][move.old.x - 1] = None
                    print("An-passant!")
                    return True
            elif right_neighbor is not None:
                if right_neighbor.name == "Pawn" and right_neighbor.move_counter == 1 and right_neighbor.team != piece.team:
                    board.spaces[move.old.y][move.old.x - 1] = None
                    print("An-passant!")
                    return True

    elif piece.team == 2:
        if move.old.y == 4:
            if left_neighbor is not None:
                if left_neighbor.name == "Pawn" and left_neighbor.move_counter == 1 and left_neighbor.team != piece.team:
                    board.spaces[move.old.y][move.old.x - 1] = None
                    print("An-passant!")
                    return True
            elif right_neighbor is not None:
                if right_neighbor.name == "Pawn" and right_neighbor.move_counter == 1 and right_neighbor.team != piece.team:
                    board.spaces[move.old.y][move.old.x - 1] = None
                    print("An-passant!")
                    return True
    return False

def can_step_forward(piece, move, board: ChessBoard):
    is_normal_move = move.new == (move.old + piece.forward)
    is_double_step = not piece.has_moved and move.new == move.old + piece.forward * 2
    is_legal_move = is_normal_move or is_double_step

    return is_legal_move and board.is_unoccupied(move.new)

def can_step_diagonal(piece, move, board):
    is_diagonal_move = (move.new == move.old + piece.forward + piece.left or
                        move.new == move.old + piece.forward - piece.left)

    return is_diagonal_move and board.is_dest_occupied_by_enemy(move)

def can_pawn_move(piece, move, board):
    return (can_step_forward(piece, move, board) or
            can_step_diagonal(piece, move, board) or
            can_an_passant(piece, move, board))
# End Pawn

def can_move_diagonally(move, board):
    return (move.is_diagonal() and
            board.is_path_clear(move) and
            board.is_dest_empty_or_enemy(move))

def can_move_xy(move, board):
    return (move.is_xy() and
            board.is_path_clear(move) and
            board.is_dest_empty_or_enemy(move))

def can_horsey_jump(move, board):
    can_horse_jump = (((abs(move.new.x - move.old.x) == 2) and abs(move.old.y - move.new.y) == 1) or
                      ((abs(move.new.x - move.old.x) == 1) and abs(move.old.y - move.new.y) == 2))
    return can_horse_jump and board.is_dest_empty_or_enemy(move)

# King Movement
def can_kingly_movement(move, board: ChessBoard):
    return ((abs(move.new.y - move.old.y) <= 1 and abs(move.new.x - move.old.x) <= 1)
            and board.is_dest_empty_or_enemy(move))

def can_castle(move, board: ChessBoard):
    king = board.get_piece(move.old)

    king.is_castling_move(move, board)

    if king.is_castling:

        if not board.is_path_clear(move):
            return False

        if king.has_moved:
            return False

        if king.team == 1:
            if move.new == Vec2(6, 7):
                if board.get_piece(Vec2(7, 7)) is not None:
                    if board.get_piece(Vec2(7, 7)).has_moved is False:
                        return True

            elif move.new == Vec2(2, 7):
                if board.get_piece(Vec2(0, 7)) is not None:
                    if board.get_piece(Vec2(0, 7)).has_moved is False:
                        return True

        else:
            if move.new == Vec2(6, 0):
                if board.get_piece(Vec2(7, 0)) is not None:
                    if board.get_piece(Vec2(7, 0)).has_moved is False:
                        return True

            elif move.new == Vec2(2, 0):
                if board.get_piece(Vec2(0, 0)) is not None:
                    if board.get_piece(Vec2(0, 0)).has_moved is False:
                        return True

        # if board.is_space_safe(move.old, king.team):
        #     return False

        return False

    return False

def is_castling(move, board: ChessBoard):
    king = board.get_piece(move.old)

    if king.team == 1:
        if move.new == Vec2(6, 7) or move.new == Vec2(2, 7):
            return True

    else:
        if move.new == Vec2(6, 0) or move.new == Vec2(2, 0):
            return True

    return False
