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
        self.setup_pieces()
        self.player_turn = 1
        self.highness = None

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
        # self.board.set_piece(Vec2(7, 0), pieces.Rook(team=2, color="magenta"))
        # self.board.set_piece(Vec2(1, 0), pieces.Knight(team=2, color="magenta"))
        # self.board.set_piece(Vec2(6, 0), pieces.Knight(team=2, color="magenta"))
        # self.board.set_piece(Vec2(2, 0), pieces.Bishop(team=2, color="magenta"))
        # self.board.set_piece(Vec2(5, 0), pieces.Bishop(team=2, color="magenta"))
        # self.board.set_piece(Vec2(3, 0), pieces.King(team=2, color="magenta"))
        self.board.set_piece(Vec2(4, 4), pieces.Queen(team=2, color="magenta"))
        self.board.set_piece(Vec2(6, 6), pieces.Queen(team=2, color="magenta"))

        # Bottom Team
        # for num in range(0, 8):
        #     self.board.set_piece(Vec2(num, 6), pieces.Pawn(team=1, color="yellow"))
        # self.board.set_piece(Vec2(0, 7), pieces.Rook(team=1, color="yellow"))
        # self.board.set_piece(Vec2(7, 7), pieces.Rook(team=1, color="yellow"))
        # self.board.set_piece(Vec2(1, 7), pieces.Knight(team=1, color="yellow"))
        # self.board.set_piece(Vec2(6, 7), pieces.Knight(team=1, color="yellow"))
        # self.board.set_piece(Vec2(2, 7), pieces.Bishop(team=1, color="yellow"))
        # self.board.set_piece(Vec2(5, 7), pieces.Bishop(team=1, color="yellow"))
        self.highness = self.board.set_piece(Vec2(5, 5), pieces.King(team=1, color="yellow"))
        # self.board.set_piece(Vec2(3, 7), pieces.Queen(team=1, color="yellow"))

    # 1: In check
    # 2: Can't move out of check
    # 3: Can't murder check
    # 4: Friendly can't jump in way
    # 5: Friendly can't murder check
    def is_checkmate(self) -> bool:
        return True