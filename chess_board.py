import error_handling
from datatypes import Move, Vec2
from typing import List
import copy


# Game Environment
class ChessBoard:
    def __init__(self):
        self.spaces = self.build()

    # Create an 8x8 of None-type
    def build(self):
        spaces = []
        for x in range(0, 8):
            spaces.append([None for x in range(0, 8)])
        return spaces

    # Board printing with variable x/y labels, x-axis will be changed to letters in the future
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

    # Piece movement
    def move(self, move, should_update_piece=True):
        piece = self.get_piece(move.old)
        self.spaces[move.new.y][move.new.x] = piece
        self.spaces[move.old.y][move.old.x] = None
        if should_update_piece:
            piece.has_moved = True

    # General piece movement check
    #######################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
    def is_dest_empty_or_enemy(self, move):
        return self.is_unoccupied(move.new) or self.get_piece(move.old).team != self.get_piece(move.new).team

    # Pawn diagonal take check
    def is_dest_occupied_by_enemy(self, move):
        if self.is_unoccupied(move.new):
            return False
        else:
            return self.get_piece(move.old).team != self.get_piece(move.new).team

    # Pawn forward check
    def is_unoccupied(self, pos):
        return self.get_piece(pos) is None

    # Get object at x/y position
    def get_piece(self, pos):
        return self.spaces[pos.y][pos.x]

    # Used in board initialization
    def set_piece(self, pos, piece):
        self.spaces[pos.y][pos.x] = piece
        return piece

    # Bounds check
    def in_board(self, pos):
        return not (pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7)

    # Castling
    def castle(self, move):
        # Utilizing normalization to determine King or Queen side castling
        new_king_pos = move.old + move.direction() * 2
        new_rook_pos = new_king_pos - move.direction()

        # Fetching the rook via Kingly movement
        rook_x = 7 if new_rook_pos.x > move.old.x else 0

        # Moves to do
        king_move = Move(move.old, new_king_pos)
        rook_move = Move(Vec2(rook_x, new_rook_pos.y), new_rook_pos)

        # The actual castling
        self.move(king_move)
        self.move(rook_move)

    # Checking blockage in path
    def is_path_clear(self, move: Move):
        # Using move's normalization to determine direction ((-1 to 1), (-1 to 1))
        spaces_in_between = move.get_spaces_in_between()
        # print([str(x) for x in spaces_in_between])

        # Checking intermediate spaces via normalized Vec2
        for space in spaces_in_between:
            if not self.is_unoccupied(space):
                # Blocked
                return False

        # Not blocked
        return True

        # Castling path checking
    def is_castle_path_clear(self, move: Move, player_team):
        spaces_in_between = move.get_spaces_in_between()

        for space in spaces_in_between:
            if not self.is_space_safe(space, player_team):
                return False

        return True

    def will_king_check(self, move, player_team, king_pos):
        old_spaces = self.spaces
        copied_spaces = copy.deepcopy(self.spaces)
        self.spaces = copied_spaces

        self.move(move, False)

        is_safe = self.is_space_safe(king_pos, player_team)
        self.spaces = old_spaces

        return not is_safe

    # Checking if King is moving out of check (Does not account for taking a spot to remove check)
    def is_space_safe(self, pos: Vec2, for_team: int) -> bool:
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                piece = self.get_piece(Vec2(x, y))
                if piece and piece.team != for_team:
                    if piece.can_move(Move(Vec2(x, y), pos), self):
                        # print(f"{piece} can take {pos}")
                        return False
        return True

    def print_all_moves_for_piece(self, pos):
        a_board = ChessBoard()
        piece = self.get_piece(pos)

        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                if piece.can_move(Move(pos, Vec2(x, y)), self):
                    a_board.spaces[y][x] = "x"

        print(a_board.display())

    # Find a piece
    def get_piece_space(self, piece_to_find) -> Vec2:
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                if self.get_piece(Vec2(x, y)) == piece_to_find:
                    return Vec2(x, y)

    # Seeing if a piece can move / avoid itself being captured / check for checkmate
    def can_piece_move(self, piece, piece_pos):
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                if piece.can_move((Move(piece_pos, Vec2(x, y))), self):
                    return True
        return False

    # Gets a piece's position
    def get_piece_pos(self, piece) -> Vec2:
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                if self.spaces[y][x] == piece:
                    return Vec2(x, y)

    def get_all_pieces_on_team(self, player_team):
        friendly_list = []
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                attacker = self.get_piece(Vec2(x, y))
                if attacker is not None and attacker.team == player_team:
                    friendly_list.append(attacker)
        return friendly_list

    # Return list of pieces checking King
    def get_all_pieces_checking_king(self, player_team, king_pos) -> List:
        hit_list = []
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                attacker = self.get_piece(Vec2(x, y))
                if attacker is not None and attacker.team != player_team:
                    if attacker.can_move((Move(Vec2(x, y), king_pos)), self):
                        hit_list.append(attacker)
        return hit_list

    # Get List of Vec2 of all board positions an enemy can go to
    def get_attacker_spaces_for_checkmate(self, attacker_piece, attacker_pos) -> List[Vec2]:
        move_list = []
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                if attacker_piece.can_move(Move(attacker_pos, Vec2(x, y)), self):
                    move_list.append(Vec2(x, y))
        return move_list

    def get_king(self, player_team):
        for y in range(len(self.spaces)):
            for x in range(len(self.spaces)):
                piece = self.get_piece(Vec2(x, y))
                if piece and piece.name == "King" and piece.team == player_team:
                    return piece
