import error_handling
from datatypes import Move, Vec2

# Game Environment
class ChessBoard:
    def __init__(self):
        self.spaces = []
        self.build()

    def is_dest_empty_or_enemy(self, move):
        return self.is_unoccupied(move.new) or self.get_piece(move.old).team != self.get_piece(move.new).team

    def is_dest_occupied_by_enemy(self, move):
        if self.is_unoccupied(move.new):
            return False
        else:
            return self.get_piece(move.old).team != self.get_piece(move.new).team

    def is_unoccupied(self, pos):
        return self.get_piece(pos) is None

    # Create an 8x8 of None-type
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
    def move(self, move):
        piece = self.get_piece(move.old)
        self.spaces[move.new.y][move.new.x] = piece
        self.spaces[move.old.y][move.old.x] = None
        piece.has_moved = True

    def get_piece(self, pos):
        return self.spaces[pos.y][pos.x]

    def set_piece(self, pos, piece):
        self.spaces[pos.y][pos.x] = piece

    def try_player_move(self, move, player_team):
        cur, new = move.old, move.new

        if not self.in_board(cur) or not self.in_board(new):
            raise error_handling.OutOfBounds()

        piece = self.get_piece(cur)

        if piece is None:
            raise error_handling.NoPieceInSpace()
        if piece.team != player_team:
            raise error_handling.ThatsNotUrFuckinTeam()

        if piece.can_move(move, self):
            piece.do_move(move, self)
        else:
            raise error_handling.IllegalMove()

    def castle(self, move):
        # King is moving towards the rook
        new_king_pos = move.old + move.direction() * 2
        new_rook_pos = new_king_pos - move.direction()

        rook_x = 7 if new_rook_pos.x > move.old.x else 0

        king_move = Move(move.old, new_king_pos)
        rook_move = Move(Vec2(rook_x, new_rook_pos.y), new_rook_pos)

        self.move(king_move)
        self.move(rook_move)

    # Using datatypes.py Move method to normalize move
    def is_path_clear(self, move: Move):
        spaces_in_between = move.get_spaces_in_between()

        # Checking intermediate spaces via normalized Vec2
        for space in spaces_in_between:
            if not self.is_unoccupied(space):
                # Blocked
                return False

        # Not blocked
        return True

    # Prelim bounds check
    def in_board(self, pos):
        return not (pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7)
