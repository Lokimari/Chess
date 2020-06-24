import unittest

from chess_game import ChessGame
from chess_board import ChessBoard
from datatypes import Vec2, Move
from pieces import Pawn, King, Knight
from error_handling import IllegalMove

def setup_full_board(chess_game):
    pass

class ChessGameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.player_turn = 1
        self.chess_game = ChessGame()
        self.chess_board = ChessBoard()
        self.chess_game.player_turn = self.player_turn
        self.start_space = Vec2(5, 5)
        self.pawn = Pawn(team=self.player_turn)

    def test_creating_a_chess_game_works_fuck(self):
        self.assertIsInstance(self.chess_game, ChessGame)

    def test_pawn_can_move_one_space_forward(self):
        # Arrange
        end_space = self.start_space + Vec2(0, -1)
        move = Move(self.start_space, end_space)

        self.chess_game.board.set_piece(self.start_space, self.pawn)

        # Act
        self.chess_game.try_player_move(move, self.player_turn)

        # Assert
        self.assertEqual(self.chess_game.board.get_piece(end_space), self.pawn)

    def test_pawn_cannot_move_backwards(self):
        # Arrange
        end_space = self.start_space + Vec2(0, 1)
        move = Move(self.start_space, end_space)

        self.chess_game.board.set_piece(self.start_space, self.pawn)

        # Act & Assert
        self.assertRaises(IllegalMove, self.chess_game.try_player_move, move, self.player_turn)

    def test_king_is_on_board(self):
        # Arrange
        king = King(team=self.player_turn)

        self.chess_game.board.set_piece(self.start_space, king)

        # Act & Assert
        self.assertTrue(self.chess_game.board.get_king(self.player_turn))

    def test_border_portal(self):
        # Arrange
        knight = Knight(team=2)

        knight_starting_space = Vec2(0, 1)
        knight_destination_space = Vec2(1, 3)

        self.chess_game.board.set_piece(knight_starting_space, knight)
        # Act & Assert
        self.assertTrue(knight.can_move((Move(knight_starting_space, knight_destination_space)), self.chess_board))
