# To-do:
# castling
# add Check and Checkmate logic
# add fork notification

# Coloration
from colorama import init
from chess_game import ChessGame
init()  # Necessary for command prompt coloration


def main():

    game = ChessGame()
    game.run()


if __name__ == "__main__":
    main()
