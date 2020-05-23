import error_handling
from datatypes import Move, Vec2
from chess_board import ChessBoard
import pieces

# Movement input, example input: 3,3,4,4 - move piece in space 3,3 to space 4,4 if possible
def move_from_string(string):
    inputs = [int(num) for num in string.split(",")]
    cur_x, cur_y, new_x, new_y = inputs
    return Move(Vec2(cur_x, cur_y), Vec2(new_x, new_y))

# Game Process
class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.highness = None
        self.setup_pieces()
        self.player_turn = 1

    def run(self):
        # Game Process Logic
        while True:
            if self.is_checkmate():
                print("Checkmate test")
            self.board.display()
            move = input(f"Player {self.player_turn}, enter move: ")
            try:
                move = move_from_string(move)
                self.board.try_player_move(move, self.player_turn)
                self.next_player_turn()

            # Error Handling
            except ValueError:
                print("Invalid Input")

            except error_handling.ChessException as chess_exception:
                print(chess_exception)

    # After a successful turn, switch players
    def next_player_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1

    # Piece placement
    def setup_pieces(self):
        # Top team
        # for num in range(0, 1):
        #     self.board.set_piece(Vec2(num, 1), pieces.Pawn(team=2, color="magenta"))
        # self.board.set_piece(Vec2(0, 0), pieces.Rook(team=2, color="magenta"))
        # self.board.set_piece(Vec2(5, 0), pieces.Rook(team=2, color="magenta")) # test rook
        # self.board.set_piece(Vec2(7, 0), pieces.Rook(team=2, color="magenta"))
        # self.board.set_piece(Vec2(1, 0), pieces.Knight(team=2, color="magenta"))
        # self.board.set_piece(Vec2(6, 0), pieces.Knight(team=2, color="magenta"))
        # self.board.set_piece(Vec2(2, 0), pieces.Bishop(team=2, color="magenta"))
        # self.board.set_piece(Vec2(5, 0), pieces.Bishop(team=2, color="magenta"))
        # self.board.set_piece(Vec2(3, 0), pieces.King(team=2, color="magenta"))
        self.board.set_piece(Vec2(7, 3), pieces.Queen(team=2, color="magenta")) # pieces are in test positions
        self.board.set_piece(Vec2(7, 2), pieces.Rook(team=2, color="magenta"))
        self.board.set_piece(Vec2(1, 4), pieces.Rook(team=2, color="magenta")) # having this line, but not the next bricks everything
        #self.board.set_piece(Vec2(7, 4), pieces.Rook(team=2, color="magenta"))

        # Bottom Team
        # for num in range(0, 8):
        #     self.board.set_piece(Vec2(num, 6), pieces.Pawn(team=1, color="yellow"))
        # self.board.set_piece(Vec2(0, 7), pieces.Rook(team=1, color="yellow"))
        self.board.set_piece(Vec2(6, 1), pieces.Knight(team=1, color="yellow")) # test Knight
        # self.board.set_piece(Vec2(7, 7), pieces.Rook(team=1, color="yellow"))
        # self.board.set_piece(Vec2(1, 7), pieces.Knight(team=1, color="yellow"))
        # self.board.set_piece(Vec2(6, 7), pieces.Knight(team=1, color="yellow"))
        # self.board.set_piece(Vec2(2, 7), pieces.Bishop(team=1, color="yellow"))
        # self.board.set_piece(Vec2(5, 7), pieces.Bishop(team=1, color="yellow"))
        self.highness = self.board.set_piece(Vec2(3, 3), pieces.King(team=1, color="yellow"))

        # self.board.set_piece(Vec2(3, 7), pieces.Queen(team=1, color="yellow"))

    # 1: In check
    # 1.1: is_space_safe is False
    # 2: Can't move out of check
    # 2.1: make can_king_move func that loops through all board spaces, checks if king can move to it (safe place :))
    # 3: Can't murder check
    # 3.1: Acquire Attackers, get all friendlies(king too) - determine if they can attack the Attackers and also uncheck
    # 3.2: ideas: implement get_all_pieces_on_team or have one big ass for loop
    # 4: Friendly can't jump in way :[ - fuck 4 for now
    def is_checkmate(self) -> bool:

        king_pos = (self.board.get_piece_space(self.highness))

        # Is King in check?
        king_is_in_danger = not self.board.is_space_safe(king_pos, self.highness.team)

        # Can the King move to free himself?
        king_cannot_move = not self.board.can_piece_move(self.highness, king_pos)

        # See if a piece may free the King
        king_cannot_be_saved = not self.can_friendlies_uncheck_king()

        return king_is_in_danger and king_cannot_move and king_cannot_be_saved

    def can_friendlies_uncheck_king(self) -> bool:
        friendlies = self.board.get_all_pieces_on_team(self.highness.team)

        checkers = self.board.get_all_pieces_checking_king(self.highness.team, self.board.get_piece_space(self.highness))

        if len(checkers) > 1:
            return False
        elif len(checkers) == 0:
            return True
        else:
            checker = checkers[0]
            for friendly in friendlies:
                move_kill = Move(self.board.get_piece_pos(friendly), self.board.get_piece_pos(checker))
                if friendly.can_move(move_kill, self.board) and self.can_friendlies_block_checker(friendly, checker):
                    print("Checker may be captures")
                    return True

    def can_friendlies_block_checker(self, friendly, checker) -> bool:
        checker_pos = self.board.get_piece_pos(checker)
        checker_path = self.board.get_piece_path(checker, checker_pos)
        print(checker_path)
        return True  # placeholder

# To-do: implement friendly jumping into attacker path to save king (only applicable if there is 1 attacker)
