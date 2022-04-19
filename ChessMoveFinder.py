import random




def findRandomMove(validMoves):
    return validMoves[random.randomint(0, len(validMoves) -1)]
    