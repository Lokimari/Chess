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

    def run(self):
        # Game Process Logic
        while True:
            self.board.display()
            move = input(f"Player {self.player_turn}, enter move: ")
            try:
                move = move_from_string(move)
                self.board.move(move, self.player_turn)
                self.next_player_turn()

            # Error Handling
            except AttributeError:
                print("Empty space selected")
            except ValueError:
                print("Invalid Input")
            except error_handling.NoPieceInSpace:
                print("No Piece in Space!")
            except error_handling.IllegalMove:
                print("Illegal move!")
            except error_handling.OutOfBounds:
                print("Out of Bounds!")
            except error_handling.ThatsNotUrFuckinTeam:
                print("Wrong team, dingus!")
            except error_handling.FriendlySpaceOccupied:
                print("You already have a piece there")
            except error_handling.Blockage:
                print("Path blocked")

    # After a successful turn, switch players
    def next_player_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1

    # Piece placement
    def setup_pieces(self):
        # Top team
        for num in range(0, 8):
            self.board.spaces[1][num] = pieces.Pawn(team=2, color="magenta")
        self.board.spaces[0][0] = pieces.Rook(team=2, color="magenta")
        self.board.spaces[0][7] = pieces.Rook(team=2, color="magenta")
        # self.board.spaces[0][1] = pieces.Knight(team=2, color="magenta")
        # self.board.spaces[0][6] = pieces.Knight(team=2, color="magenta")
        # self.board.spaces[0][2] = pieces.Bishop(team=2, color="magenta")
        # self.board.spaces[0][5] = pieces.Bishop(team=2, color="magenta")
        self.board.spaces[0][3] = pieces.King(team=2, color="magenta")
        self.board.spaces[0][4] = pieces.Queen(team=2, color="magenta")

        # Bottom Team
        for num in range(0, 8):
            self.board.spaces[6][num] = pieces.Pawn(team=1, color="yellow")
        self.board.spaces[7][0] = pieces.Rook(team=1, color="yellow")
        self.board.spaces[7][7] = pieces.Rook(team=1, color="yellow")
        # self.board.spaces[7][1] = pieces.Knight(team=1, color="yellow")
        # self.board.spaces[7][6] = pieces.Knight(team=1, color="yellow")
        # self.board.spaces[7][2] = pieces.Bishop(team=1, color="yellow")
        # self.board.spaces[7][5] = pieces.Bishop(team=1, color="yellow")
        self.board.spaces[7][4] = pieces.King(team=1, color="yellow")
        self.board.spaces[7][3] = pieces.Queen(team=1, color="yellow")