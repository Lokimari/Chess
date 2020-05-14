# To-do:
# add piece blockage logic
# castling
# add Check and Checkmate logic
# add fork notification

# y = mx + b
# b = y - mx
# intXs = range(minX + 1, maxX) = range(3,5) = [3,4]
# ints = [Vec2(x, m*x + b) for x in intXs] = [Vec2(3,1*3+0), Vec2(4,1*4+0)] = [Vec2(3,3), Vec2(4,4)]
# move = Move(Vec2(2,2), Vec2(5,5))
# print(move.get_diagonal_spaces())

# Coloration
from colorama import init
from chess_game import ChessGame
from chess_game import Move
from chess_game import Vec2
init()  # Necessary for command prompt coloration


def main():
    # move = Move(Vec2(-5, 0), Vec2(-2, 3))
    # print([str(x) for x in move.get_spaces_inbetween()])
    game = ChessGame()
    game.run()


if __name__ == "__main__":
    main()
