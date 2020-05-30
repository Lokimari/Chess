import unittest

from chess_game import ChessGame
from datatypes import Vec2, Move
from pieces import Pawn, King
from error_handling import IllegalMove

class TestTurns(unittest.TestCase):
    def setUp(self) -> None:
        self.player_turn = 1
        self.chess_game = ChessGame()
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
