import error_handling
from datatypes import Move, Vec2
from chess_board import ChessBoard
import pieces

# Movement input, example input: 3,3,4,4 - move piece in space 3,3 to space 4,4 if possible
def move_from_string(string):
    string_inputs = [inp for inp in string.split(",")]

    int_inputs = [-1, -1, -1, -1]

    # TODO: Convert to equation abs(num - 8) = new_num
    for inp in range(len(string_inputs)):
        if string_inputs[inp] == "a" or string_inputs[inp] == "A" or string_inputs[inp] == "8":
            int_inputs[inp] = 0
        elif string_inputs[inp] == "b" or string_inputs[inp] == "B" or string_inputs[inp] == "7":
            int_inputs[inp] = 1
        elif string_inputs[inp] == "c" or string_inputs[inp] == "C" or string_inputs[inp] == "6":
            int_inputs[inp] = 2
        elif string_inputs[inp] == "d" or string_inputs[inp] == "D" or string_inputs[inp] == "5":
            int_inputs[inp] = 3
        elif string_inputs[inp] == "e" or string_inputs[inp] == "E" or string_inputs[inp] == "4":
            int_inputs[inp] = 4
        elif string_inputs[inp] == "f" or string_inputs[inp] == "F" or string_inputs[inp] == "3":
            int_inputs[inp] = 5
        elif string_inputs[inp] == "g" or string_inputs[inp] == "G" or string_inputs[inp] == "2":
            int_inputs[inp] = 6
        elif string_inputs[inp] == "h" or string_inputs[inp] == "H" or string_inputs[inp] == "1":
            int_inputs[inp] = 7
        else:
            int_inputs[inp] = int(string_inputs[inp])

    cur_x, cur_y, new_x, new_y = int_inputs

    return Move(Vec2(int(cur_x), int(cur_y)), Vec2(int(new_x), int(new_y)))

def algebraic_move(move):
    algebraic_print_list = [-1, -1, -1, -1]
    algebraic_print_list[0] = move.old.x
    algebraic_print_list[1] = move.old.y

    algebraic_print_list[2] = move.new.x
    algebraic_print_list[3] = move.new.y

    if algebraic_print_list[0] == 0:
        algebraic_print_list[0] = "A"
    elif algebraic_print_list[0] == 1:
        algebraic_print_list[0] = "B"
    elif algebraic_print_list[0] == 2:
        algebraic_print_list[0] = "C"
    elif algebraic_print_list[0] == 3:
        algebraic_print_list[0] = "D"
    elif algebraic_print_list[0] == 4:
        algebraic_print_list[0] = "E"
    elif algebraic_print_list[0] == 5:
        algebraic_print_list[0] = "F"
    elif algebraic_print_list[0] == 6:
        algebraic_print_list[0] = "G"
    elif algebraic_print_list[0] == 7:
        algebraic_print_list[0] = "H"

    if algebraic_print_list[2] == 0:
        algebraic_print_list[2] = "A"
    elif algebraic_print_list[2] == 1:
        algebraic_print_list[2] = "B"
    elif algebraic_print_list[2] == 2:
        algebraic_print_list[2] = "C"
    elif algebraic_print_list[2] == 3:
        algebraic_print_list[2] = "D"
    elif algebraic_print_list[2] == 4:
        algebraic_print_list[2] = "E"
    elif algebraic_print_list[2] == 5:
        algebraic_print_list[2] = "F"
    elif algebraic_print_list[2] == 6:
        algebraic_print_list[2] = "G"
    elif algebraic_print_list[2] == 7:
        algebraic_print_list[2] = "H"

    algebraic_print_list[1] = abs(algebraic_print_list[1] - 8)
    algebraic_print_list[3] = abs(algebraic_print_list[3] - 8)

    algebraic_print = f"{algebraic_print_list[0]}{algebraic_print_list[1]} -> {algebraic_print_list[2]}{algebraic_print_list[3]}"

    return algebraic_print

# Game Process
class ChessGame:
    def __init__(self, setup_pieces=False):
        self.board = ChessBoard()
        self.highness = None
        self.p1_king = None
        self.p2_king = None
        self.player_turn = 1
        self.other_player_turn = 2
        self.turn_counter = 0
        self.move_history = []
        self.player_1_color = "yellow"
        self.player_2_color = "magenta"
        if setup_pieces:
            self.setup_pieces()

    def end_game(self):
        print("Game Over")
        print(f"Player {self.other_player_turn} wins!")
        exit()

    def run(self):
        # Game Process Logic
        while True:
            if self.is_checkmate():
                print("Checkmate")
                self.end_game()
            self.board.display()
            move = input(f"Player {self.player_turn}, enter move: ")
            try:
                move = move_from_string(move)
                self.try_player_move(move, self.player_turn)
                self.move_history.append(move)
                self.board.get_piece(move.new).move_counter += 1
                self.next_player_turn()

            # Error Handling
            except ValueError:
                print("Invalid Input")

            except error_handling.ChessException as chess_exception:
                print(chess_exception)

    # After a successful turn, switch players
    def next_player_turn(self):
        self.turn_counter += 1
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.other_player_turn = 2 if self.player_turn == 2 else 1

    # Piece placement
    def setup_pieces(self):
        # Top team
        # for num in range(0, 8):
        #     self.board.set_piece(Vec2(num, 1), pieces.Pawn(team=2, color="magenta"))
        self.board.set_piece(Vec2(4, 1), pieces.Rook(team=2, color="magenta"))
        # self.board.set_piece(Vec2(7, 0), pieces.Rook(team=2, color="magenta"))
        # self.board.set_piece(Vec2(1, 0), pieces.Knight(team=2, color="magenta"))
        # self.board.set_piece(Vec2(6, 0), pieces.Knight(team=2, color="magenta"))
        # self.board.set_piece(Vec2(2, 0), pieces.Bishop(team=2, color="magenta"))
        # self.board.set_piece(Vec2(5, 0), pieces.Bishop(team=2, color="magenta"))
        self.p2_king = self.board.set_piece(Vec2(3, 0), pieces.King(team=2, color="magenta"))
        # self.board.set_piece(Vec2(4, 0), pieces.Queen(team=2, color="magenta"))

        # Bottom Team
        # for num in range(0, 8):
        #     self.board.set_piece(Vec2(num, 6), pieces.Pawn(team=1, color="yellow"))
        # self.board.set_piece(Vec2(0, 7), pieces.Rook(team=1, color="yellow"))
        # self.board.set_piece(Vec2(7, 7), pieces.Rook(team=1, color="yellow"))
        # self.board.set_piece(Vec2(1, 7), pieces.Knight(team=1, color="yellow"))
        # self.board.set_piece(Vec2(6, 7), pieces.Knight(team=1, color="yellow"))
        self.board.set_piece(Vec2(4, 6), pieces.Bishop(team=1, color="yellow"))
        # self.board.set_piece(Vec2(5, 7), pieces.Bishop(team=1, color="yellow"))
        self.p1_king = self.board.set_piece(Vec2(4, 7), pieces.King(team=1, color="yellow"))
        # self.board.set_piece(Vec2(3, 7), pieces.Queen(team=1, color="yellow"))

        # cool stuff
        self.board.print_all_moves_for_piece(Vec2(4, 7))

    def is_checkmate(self) -> bool:

        self.highness = self.p1_king if self.player_turn == 1 else self.p2_king
        king_pos = (self.board.get_piece_pos(self.highness))

        # Is King in check?
        king_is_in_danger = not self.board.is_space_safe(king_pos, self.highness.team)

        # Can the King move to free himself?
        king_cannot_move = not self.board.can_piece_move(self.highness, king_pos)

        # See if a piece may free the King
        king_cannot_be_saved = not self.can_friendlies_uncheck_king()

        if king_is_in_danger:
            print("Check")
        if king_is_in_danger and king_cannot_move and not king_cannot_be_saved:
            print("Your King requires help from a friendly piece")
        return king_is_in_danger and king_cannot_move and king_cannot_be_saved

    # Murder checker
    def can_friendlies_uncheck_king(self) -> bool:

        friendlies = self.board.get_all_pieces_on_team(self.highness.team)

        checkers = self.board.get_all_pieces_checking_king(self.highness.team, self.board.get_piece_space(self.highness))

        if len(checkers) > 1:
            return False
        elif len(checkers) == 0:
            return True
        else:
            checker = checkers[0]
            if friendlies:
                for friendly in friendlies:
                    move_kill = Move(self.board.get_piece_pos(friendly), self.board.get_piece_pos(checker))
                    if friendly.can_move(move_kill, self.board) or self.can_friendlies_block_checker(friendlies, checker):
                        print(f"Checker may be captured or blocked")
                        if friendly.can_move(move_kill, self.board) and self.can_friendlies_block_checker(friendlies, checker):
                            print(f"Checker may be captured via {move_kill}, and blocked via {self.can_friendlies_block_checker(friendlies, checker)}")
                        return True
            else:
                return False

    def can_friendlies_block_checker(self, friendlies, checker) -> bool:
        checker_pos = self.board.get_piece_pos(checker)
        checking_path = self.board.get_attacker_spaces_for_checkmate(checker, checker_pos)
        if len(checking_path) > 0:
            for friendly in friendlies:
                friendly_pos = self.board.get_piece_pos(friendly)
                for pos in checking_path:
                    move = Move(friendly_pos, pos)
                    if friendly.can_move(move, self.board):
                        if not self.board.will_king_check(move, self.highness.team, self.board.get_piece_pos(self.highness)):
                            if friendly.name != "King":
                                print(f"Checker may be blocked via {move}")
                                return True
        else:
            print("No check path (Knight?)")
            return False

    # For while loop in chess_game.py
    def try_player_move(self, move, player_team):
        cur, new = move.old, move.new

        # Bounds check
        if not self.board.in_board(cur) or not self.board.in_board(new):
            raise error_handling.OutOfBounds()

        piece = self.board.get_piece(cur)

        # Selected empty space
        if piece is None:
            raise error_handling.NoPieceInSpace()

        # Wrong team check
        if piece.team != player_team:
            raise error_handling.ThatsNotUrFuckinTeam()

        # Move puts own King in check
        king_pos = self.board.get_piece_pos(self.board.get_king(player_team))

        # This allows Kings to free themselves
        if piece.name == "King":
            piece.is_castling_move(move, self.board)

            if self.board.will_king_check(move, player_team, move.new):
                raise error_handling.CheckingKing()
            elif not self.board.is_space_safe(king_pos, piece.team) and piece.is_castling:
                raise error_handling.CastlingWhileChecked()
            elif not self.board.is_castle_path_clear(move, player_team) and piece.is_castling:
                raise error_handling.CastlePathBlocked()

        # This prevents other pieces from endangering the King
        else:
            if self.board.will_king_check(move, player_team, king_pos):
                raise error_handling.CheckingKing()

        if piece.can_move(move, self.board):
            piece.do_move(move, self.board)
            print(algebraic_move(move))
            if piece.name == "Pawn" and piece.team == 1:
                if move.new.y == 0:
                    self.pawn_promotion(move.new)
            elif piece.name == "Pawn" and piece.team == 2:
                if move.new.y == 7:
                    self.pawn_promotion(move.new)
        else:
            raise error_handling.IllegalMove()

    def pawn_promotion(self, pos):
        print("Promotion! - Bishop, Knight, Rook, or Queen?")
        promotion_choice = input()
        color = self.player_1_color if self.player_turn == 1 else self.player_2_color

        pawn = self.board.get_piece(pos)
        if promotion_choice == "Queen":
            self.board.spaces[pos.y][pos.x] = pieces.Queen(team=pawn.team)

        if promotion_choice == "Rook":
            self.board.spaces[pos.y][pos.x] = pieces.Rook(team=pawn.team)

        if promotion_choice == "Knight":
            self.board.spaces[pos.y][pos.x] = pieces.Knight(team=pawn.team)

        if promotion_choice == "Bishop":
            self.board.spaces[pos.y][pos.x] = pieces.Bishop(team=pawn.team)

    def get_previous_move_piece(self):
        previous_move_piece = self.board.get_piece(self.move_history[self.turn_counter - 1])

        return previous_move_piece
