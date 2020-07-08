# Error Handling

# Base Chess Exception
class ChessException(Exception):
    def __init__(self, message):
        super(ChessException, self).__init__(message)

# Other exceptions
class IllegalMove(ChessException):
    def __init__(self, message="That's an illegal move!"):
        super(IllegalMove, self).__init__(message)

class OutOfBounds(ChessException):
    def __init__(self, message="That move is out of bounds!"):
        super(OutOfBounds, self).__init__(message)

class ThatsNotUrFuckinTeam(ChessException):
    def __init__(self, message="Wrong team selected!"):
        super(ThatsNotUrFuckinTeam, self).__init__(message)

class Blockage(ChessException):
    def __init__(self, message="Path blocked!"):
        super(Blockage, self).__init__(message)

class NoPieceInSpace(ChessException):
    def __init__(self, message="No piece in space"):
        super(NoPieceInSpace, self).__init__(message)

class CheckingKing(ChessException):
    def __init__(self, message="King would be placed in check"):
        super(CheckingKing, self).__init__(message)

class CastlingWhileChecked(ChessException):
    def __init__(self, message="King is in check, may not castle"):
        super(CastlingWhileChecked, self).__init__(message)

class CastlePathBlocked(ChessException):
    def __init__(self, message="The castle path is endangered!"):
        super(CastlePathBlocked, self).__init__(message)
