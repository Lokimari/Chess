from termcolor import colored

class King:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "King"
        self.has_moved = has_moved

    def __str__(self):
        return colored("K", self.color)

    def can_move(self, move):
        return abs(move.new.y - move.old.y) <= 1 and abs(move.new.x - move.old.x) <= 1


class Queen:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Queen"
        self.has_moved = has_moved

    def __str__(self):
        return colored("Q", self.color)

    def can_move(self, move):
        return (move.new.x == move.old.x or move.new.y == move.old.y or
                (move.old.x - move.old.y == move.new.x - move.new.y) or
                (move.old.x + move.old.y == move.new.x + move.new.y))


class Bishop:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Bishop"
        self.has_moved = has_moved

    def __str__(self):
        return colored("B", self.color)

    def can_move(self, move):
        return ((move.old.x - move.old.y == move.new.x - move.new.y) or
                (move.old.x + move.old.y == move.new.x + move.new.y))


class Rook:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Rook"
        self.has_moved = has_moved

    def __str__(self):
        return colored("R", self.color)

    def can_move(self, move):
        return move.new.x == move.old.x or move.new.y == move.old.y


class Knight:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Knight"
        self.has_moved = has_moved

    def __str__(self):
        return colored("H", self.color)

    def can_move(self, move):
        return (((abs(move.new.x - move.old.x) == 2) and abs(move.old.y - move.new.y) == 1) or
                ((abs(move.new.x - move.old.x) == 1) and abs(move.old.y - move.new.y) == 2))


class Pawn:
    def __init__(self, team, color="white", has_moved=False):
        self.color = color
        self.team = team
        self.name = "Pawn"
        self.has_moved = has_moved

    def __str__(self):
        return colored("P", self.color)

    def can_move(self, move):
        if self.has_moved:
            return (((move.new.x - move.old.x == -1) and self.team == 1) or
                    ((move.new.x - move.old.x == 1) and self.team == 2))
        else:
            return (((move.new.x - move.old.x == -2 or move.new.x - move.old.x == -1) and self.team == 1) or
                    ((move.new.x - move.old.x == 2 or move.new.x - move.old.x == 1) and self.team == 2))
