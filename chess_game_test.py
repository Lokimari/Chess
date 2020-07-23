import unittest

from chess_game import ChessGame
from datatypes import Vec2, Move
from pieces import Piece, Pawn, Knight, King, Rook, Bishop, Queen
from error_handling import IllegalMove

def setup_full_board(chess_game):
    pass


# IMPORTANT
# Initializing Vec2 positions is done by indexes, but Move()s are done inversely with y coordinates
# Move(Vec2(0, 2), Vec2(0, 4)) will move a starting team1 pawn forward twice
#     0 1 2 3 4 5 6 7
#     A B C D E F G H
# 8 [ _ _ _ _ _ _ _ _ ]
# 7 [ _ _ _ _ _ _ _ _ ]
# 6 [ _ _ _ _ _ _ _ _ ]
# 5 [ _ _ _ _ _ _ _ _ ]
# 4 [ _ _ _ _ _ _ _ _ ]
# 3 [ _ _ _ _ _ _ _ _ ]
# 2 [ _ _ _ _ _ _ _ _ ]
# 1 [ _ _ _ _ _ _ _ _ ]

class ChessGameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.player_turn = 1
        self.chess_game = ChessGame()
        self.chess_board = self.chess_game.board
        self.chess_game.player_turn = self.player_turn
        self.start_space = Vec2(5, 5)
        self.king = King(team=self.player_turn)
        self.knight = Knight(team=self.player_turn)
        self.pawn = Pawn(team=self.player_turn)
        self.enemy_pawn = Pawn(team=2)
        self.p1_pawn = Pawn(team=1)

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
        self.chess_game.board.set_piece(self.start_space, self.king)

        # Act & Assert
        self.assertTrue(self.chess_game.board.get_king(self.player_turn))

    def test_knight_border_portal(self):
        # Arrange
        knight = Knight(team=1)

        knight_starting_space = Vec2(1, 0)
        knight_destination_space = Vec2(0, 2)

        knight_move = Move(knight_starting_space, knight_destination_space)

        self.chess_game.board.set_piece(knight_starting_space, knight)

        # Act & Assert
        self.assertTrue(knight.can_move(knight_move, self.chess_board))

    def test_get_king(self):
        # Arrange
        king_start_pos = Vec2(4, 0)
        self.chess_game.board.set_piece(king_start_pos, self.king)

        # Act
        the_king = self.chess_board.get_king(self.player_turn)

        # Assert
        self.assertEqual(self.king, the_king)

    def test_get_king_returns_none_if_no_king(self):
        # Arrange
        # No arrangement

        # Act
        the_king = self.chess_board.get_king(self.player_turn)

        # Assert
        self.assertIsNone(the_king)

    def test_can_king_free_himself_if_checked(self):
        # Arrange
        king_start_pos = Vec2(4,7)
        self.chess_game.board.set_piece(king_start_pos, self.king)
        self.chess_game.board.set_piece(Vec2(5, 6), self.enemy_pawn)

        # Act
        king_move = self.king.can_move(Move(king_start_pos, Vec2(3, 7)), self.chess_board)

        # Assert
        self.assertTrue(king_move)

    def test_king_cannot_endanger_himself(self):
        # Arrange
        king_start_pos = Vec2(4, 7)
        self.chess_game.board.set_piece(king_start_pos, self.king)
        self.chess_game.board.set_piece(Vec2(5, 5), self.enemy_pawn)

        # Act
        king_move = self.king.can_move(Move(king_start_pos, Vec2(4, 2)), self.chess_board)

        # Assert
        self.assertFalse(king_move)

    def test_pawn_may_double_jump(self):
        # Arrange
        pawn_start_pos = Vec2(5, 5)

        # Act
        pawn_move = self.pawn.can_move(Move(pawn_start_pos, Vec2(5, 3)), self.chess_board)

        # Assert
        self.assertTrue(pawn_move)

    def test_pawn_may_not_double_jump_after_moving(self):
        # Arrange
        pawn_start_pos = Vec2(0, 6)

        # Act
        self.chess_board.move(Move(pawn_start_pos, Vec2(0, 3)))
        pawn_move_to_test = self.p1_pawn.can_move(Move(pawn_start_pos, Vec2(5, 3)), self.chess_board)

        # Assert
        self.assertFalse(pawn_move_to_test)

    def test_horse_may_jump(self):
        # Arrange
        knight_start_pos = Vec2(5, 5)
        self.chess_game.board.set_piece(knight_start_pos, self.knight)
        self.chess_game.board.set_piece(Vec2(5, 4), self.pawn)
        self.chess_game.board.set_piece(Vec2(4, 4), self.king)

        # Act
        knight_jump = self.knight.can_move(Move(knight_start_pos, Vec2(3, 4)), self.chess_board)

        # Assert
        self.assertTrue(knight_jump)

    def test_king_may_castle_left(self):
        # Arrange
        king_start_pos = Vec2(4, 7)
        rook_start_pos = Vec2(0, 7)
        self.chess_game.board.set_piece(king_start_pos, self.king)
        self.chess_game.board.set_piece(rook_start_pos, Rook(team=self.player_turn))

        # Act
        castle_move = self.king.can_move(Move(king_start_pos, Vec2(2, 7)), self.chess_board)

        # Assert
        self.assertTrue(castle_move)

    def test_king_may_castle_right(self):
        # Arrange
        king_start_pos = Vec2(4, 7)
        rook_start_pos = Vec2(7, 7)
        self.chess_game.board.set_piece(king_start_pos, self.king)
        self.chess_game.board.set_piece(rook_start_pos, Rook(team=self.player_turn))

        # Act
        castle_move = self.king.can_move(Move(king_start_pos, Vec2(6, 7)), self.chess_board)

        # Assert
        self.assertTrue(castle_move)

    def test_king_cannot_over_move_For_castle_left(self):
        # Arrange
        king_start_pos = Vec2(4, 7)
        rook_start_pos = Vec2(0, 7)
        self.chess_game.board.set_piece(king_start_pos, self.king)
        self.chess_game.board.set_piece(rook_start_pos, Rook(team=self.player_turn))

        # Act
        castle_move = self.king.can_move(Move(king_start_pos, Vec2(1, 7)), self.chess_board)

        # Assert
        self.assertFalse(castle_move)

    def test_king_cannot_over_move_For_castle_right(self):
        # Arrange
        king_start_pos = Vec2(4, 7)
        rook_start_pos = Vec2(7, 7)
        self.chess_game.board.set_piece(king_start_pos, self.king)
        self.chess_game.board.set_piece(rook_start_pos, Rook(team=self.player_turn))

        # Act
        castle_move = self.king.can_move(Move(king_start_pos, Vec2(7, 7)), self.chess_board)

        # Assert
        self.assertFalse(castle_move)

    def test_piece_may_not_move_out_of_bounds(self):
        # Arrange
        knight_end_pos = Vec2(-2, -1)

        # Act
        is_knight_moving_inbound = self.chess_board.in_board(knight_end_pos)

        # Assert
        self.assertFalse(is_knight_moving_inbound)
