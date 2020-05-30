# To-do:
# add Check and Checkmate logic - needs test cases to confirm functionality
# add fork notification

# Coloration
from colorama import init
from chess_game import ChessGame
init()  # Necessary for command prompt coloration


def main():

    game = ChessGame(setup_pieces=True)
    game.run()


if __name__ == "__main__":
    main()
