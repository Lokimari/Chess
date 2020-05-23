# To-do:
# add Check and Checkmate logic - allow friendlies to jump in the way of attacker to save king
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
