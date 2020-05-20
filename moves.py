# Piece move logic

# Pawn
def can_step_forward(piece, move, board):
    is_normal_move = move.new == (move.old + piece.forward)
    print(is_normal_move)
    print(move.old + piece.forward)
    print(move)
    is_double_step = not piece.has_moved and move.new == move.old + piece.forward * 2
    is_legal_move = is_normal_move or is_double_step

    return is_legal_move and board.is_unoccupied(move.new)

def can_step_diagonal(piece, move, board):
    is_diagonal_move = (move.new == move.old + piece.forward + piece.left or
                        move.new == move.old + piece.forward - piece.left)

    return is_diagonal_move and board.is_dest_occupied_by_enemy(move)

def can_pawn_move(piece, move, board):
    return (can_step_forward(piece, move, board) or
            can_step_diagonal(piece, move, board))
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
def can_kingly_movement(move, board):
    return (abs(move.new.y - move.old.y) <= 1 and abs(move.new.x - move.old.x) <= 1) and board.is_dest_empty_or_enemy(move)

def can_castle(move, board):

    if not board.is_path_clear(move):
        return False

    if board.get_piece(move.old).has_moved:
        return False

    if board.get_piece(move.old).team == 1:
        if move.new.x == move.old.x + 2:
            if board.spaces[7][7].has_moved is False:
                return True

        elif move.new.x == move.old.x - 2:
            if board.spaces[0][7].has_moved is False:
                return True

    else:
        if move.new.x == move.old.x + 2:
            if board.spaces[7][0].has_moved is False:
                return True

        elif move.new.x == move.old.x - 2:
            if board.spaces[0][0].has_moved is False:
                return True

    return False
