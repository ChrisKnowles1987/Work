
import random
import ChessEngine






CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "P": 1}

def scoreMaterial(board):
    gs = ChessEngine.Gamestate()
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
    print (score)
    return score


def scoreBoard(gs):
    gs = ChessEngine.Gamestate()
    #positive score is good for white, negative score is good for black so we need to set the worst score based on perspective
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
    return score

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) -1)]

def findBestMoveMinMax(gs, validMoves):
    gs = ChessEngine.Gamestate()
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    gs = ChessEngine.Gamestate()
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE #set to lowest possible score for white to find a better move and iterate over this to fidn the best move
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, not whiteToMove )
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
        
    else:
        minScore = CHECKMATE #set to lowest possible score for black to find a better move and iterate over this to fidn the best move
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, not whiteToMove)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore