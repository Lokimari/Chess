import error_handling
from datatypes import Move

# Game Environment


class ChessBoard:
    def __init__(self):
        self.spaces = []
        self.build()

    # Create an 8x8 of None-type
    def build(self):
        for x in range(0, 8):
            self.spaces.append([None for space in range(0, 8)])

    # Board printing with variable x/y labels
    def display(self):
        # row_num = 8
        row_num = 0
        board_string = "    0 1 2 3 4 5 6 7"
        for row in self.spaces:
            board_string += "\n" + str(row_num) + " [ "
            row_num += 1
            # row_num -= 1
            for val in row:
                if val is None:
                    board_string += "_ "
                else:
                    board_string += str(val) + " "
            board_string += "]"

        print(board_string)

    # Takes Vec2 of current space and destination space, checks each, moves, and sets piece attr "has_moved" = True
    def move(self, move, player_team):
        # vars
        cur = move.old
        new = move.new

        # Movement Logic

        # Preliminary error checks
        if not self.in_board(cur) or not self.in_board(new):
            raise error_handling.OutOfBounds()

        piece = self.spaces[cur.x][cur.y]
        destination = self.spaces[new.x][new.y]

        if not piece.team == player_team:
            raise error_handling.ThatsNotUrFuckinTeam()

        # Start of Movement Logic
        if piece.name == "Knight":
            if piece.can_move(move):
                self.movement(move)
            else:
                raise error_handling.IllegalMove()
        else:
            if not self.check_blockage(move):
                if piece.can_move(move):
                    if destination is None:
                        self.movement(move)
                    elif getattr(destination, "team") is player_team:
                        raise error_handling.FriendlySpaceOccupied()
                    else:
                        print(str(getattr(destination, "name") + " taken"))
                        self.movement(move)
                else:
                    raise error_handling.IllegalMove()
            else:
                raise error_handling.Blockage()

    # Movement
    def movement(self, move):
        cur = move.old
        new = move.new
        piece = self.spaces[cur.x][cur.y]

        print("Moving...")
        print(move)
        setattr(self.spaces[cur.x][cur.y], 'has_moved', True)  # So pawns can't do wacky stuff
        # The actual movement
        self.spaces[new.x][new.y] = piece
        self.spaces[cur.x][cur.y] = None
        # End of Movement Logic

    def check_blockage(self, move: Move):
        spaces_inbetween = move.get_spaces_inbetween()

        for space in spaces_inbetween:
            if self.spaces[space.x][space.y] is not None:
                return True

        return False

    # Prelim bounds check
    def in_board(self, pos):
        return not (pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7)
