import error_handling
from datatypes import Move, Vec2
from chess_board import ChessBoard
import pieces

move_string_dict = {
    'A': 0, '8': 0,
    'B': 1, '7': 1,
    'C': 2, '6': 2,
    'D': 3, '5': 3,
    'E': 4, '4': 4,
    'F': 5, '3': 5,
    'G': 6, '2': 6,
    'H': 7, '1': 7,
}

def move_from_string(string):
    cur_x, cur_y, new_x, new_y =[int(move_string_dict[x.upper()]) for x in string]
    return Move(Vec2(cur_x, cur_y), Vec2(new_x, new_y))


algebraic_print_dict = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H"
}

def algebraic_move(move):
    print_list = [-1, -1, -1, -1]
    print_list[0] = algebraic_print_dict[move.old.x]
    print_list[2] = algebraic_print_dict[move.new.x]

    print_list[1] = abs(move.old.y - 8)
    print_list[3] = abs(move.new.y - 8)

    return f"{print_list[0]}{print_list[1]} -> {print_list[2]}{print_list[3]}"

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
        for num in range(0, 8):
            self.board.set_piece(Vec2(num, 1), pieces.Pawn(team=2))
        self.board.set_piece(Vec2(0, 0), pieces.Rook(team=2))
        self.board.set_piece(Vec2(7, 0), pieces.Rook(team=2))
        self.board.set_piece(Vec2(1, 0), pieces.Knight(team=2))
        self.board.set_piece(Vec2(6, 0), pieces.Knight(team=2))
        self.board.set_piece(Vec2(2, 0), pieces.Bishop(team=2))
        self.board.set_piece(Vec2(5, 0), pieces.Bishop(team=2))
        self.p2_king = self.board.set_piece(Vec2(3, 0), pieces.King(team=2))
        self.board.set_piece(Vec2(4, 0), pieces.Queen(team=2))

        # Bottom Team
        for num in range(0, 8):
            self.board.set_piece(Vec2(num, 6), pieces.Pawn(team=1))
        self.board.set_piece(Vec2(0, 7), pieces.Rook(team=1))
        self.board.set_piece(Vec2(7, 7), pieces.Rook(team=1))
        self.board.set_piece(Vec2(1, 7), pieces.Knight(team=1))
        self.board.set_piece(Vec2(6, 7), pieces.Knight(team=1))
        self.board.set_piece(Vec2(2, 7), pieces.Bishop(team=1))
        self.board.set_piece(Vec2(5, 7), pieces.Bishop(team=1))
        self.p1_king = self.board.set_piece(Vec2(4, 7), pieces.King(team=1))
        self.board.set_piece(Vec2(3, 7), pieces.Queen(team=1))

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
