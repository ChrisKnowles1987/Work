
import random
import ChessEngine






CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "P": 1}




def scoreBoard(gs):
    
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


#NegaMax algorithm

def findBestMove(gs, validMoves):
    
    global nextMove, moveCounter
    nextMove = None
    moveCounter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1) 
    print(str(moveCounter) + " moves evaluated")
    #-CHECKMATE = alpha and CHECKMATE = beta to initialise with the lowest max and highest min
    
    return nextMove

#NegaMax with Alpha-beta pruning
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, moveCounter
    moveCounter += 1
    #turnMultiplier = 1 if gs.whiteToMove else -1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #move ordering - checks captures attacks (add later)
    
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth -1, -beta, -alpha, -turnMultiplier) #swap alpha and bata and add negative to make min the max and max the min
        
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha = maxScore
        if alpha >= beta:
            break
        
    return maxScore



#NegaMax test
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth -1, -turnMultiplier)
        
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        
    return maxScore


#min max algorithm

def findBestMoveMinMax(gs, validMoves):
    
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    
    global nextMove
    if depth == 0:
        return scoreMaterial(gs)
    
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