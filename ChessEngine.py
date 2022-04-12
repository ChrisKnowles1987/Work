"""
class file for storing information aboutt the current state of the game, generating valid moves at teh current state and traking the movelog
"""
from math import pi
from operator import truediv
from ChessMain import DIMENSION
from ChessMain import drawgameState


class Gamestate():
    def __init__(self):
        #8x8 list of lists with piece annotations (b/w = colour, P,R,N,B,Q,K = Pawn, Rook, Knight, Bishop, Queen, King, '--' = empty square)
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        self.moveFunctions ={"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation =(0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        
        
        
    #execute the move.  Will not cover special moves like promotion, castling and en-passant
    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #update king positions
        if move.pieceMoved == "wK" :
            self.whiteKingLocation = (move.endRow ,move.endCol)
        elif move.pieceMoved == "bK" :
            self.blackKingLocation = (move.endRow ,move.endCol)
            
        
    #undo last move with keypress

    def undoMove (self):
        if len(self.moveLog) != 0:
            move =self.moveLog.pop()
            self.board[move.startRow][move.startCol] =  move.pieceMoved
            self.board[move.endRow][move.endCol] =  move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #update king positions
        if move.pieceMoved == "wK" :
            self.whiteKingLocation = (move.startRow ,move.startCol)
        elif move.pieceMoved == "bK" :
            self.blackKingLocation = (move.startRow ,move.startCol)
            
    #All moves considering checks

    def getValidMoves(self):
        
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
            
        if self.inCheck:
            if len(self.checks) == 1:   # with 1 attacker we have the choice to block or move king
                moves = self.getAllPossibleMoves()
                check = self.checks[0] # gets the info of the attacking piece
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  #squares that can block the check
                
                #for Knight checks the Knight must be captured or we move the king
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else: #calculate the squares between the king and attacker 
                    for i in range (1 ,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)  #check[2] and check [3] are the directions (row, col) that the check is coming from
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # we have calculated all squares between the king and its attacker
                            break
                # remove moves which dont block the check or move the king out of check
                for i in range(len(moves)-1, -1, -1): # go backwards through moves to avoid skipping anything when moves are added or removed     
                    if moves[i].pieceMoved[1] != "K": #if the move is not the king we have to check that it blocks the check line
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: # more than one attacker means we have to move the king
                self.getKingMoves(kingRow, kingCol, moves)
        else: #not in check so all moves are valid
            moves = self.getAllPossibleMoves()

        return moves

    #All moves without cosndierign checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves
                    
    #define moves     
    def getPawnMoves(self, r, c ,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection =(self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        #white pawn moves
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1 , 0):
                    moves.append(Move((r,c),(r-1,c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c), self.board))
                    
            #captures
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    if not piecePinned or pinDirection == (-1 , -1):
                        moves.append(Move((r,c),(r-1,c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    if not piecePinned or pinDirection == (-1 , 1):
                        moves.append(Move((r,c),(r-1,c+1), self.board))
        #back pawn moves
        else:
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection == (1 , 0):
                    moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c), self.board))
                    
            #captures
            if c-1 >=0:
                if self.board[r+1][c-1][0] == "w":
                    if not piecePinned or pinDirection == (1 , -1):
                     moves.append(Move((r,c),(r+1,c-1), self.board))
            if c+1 <=7:
                if self.board[r+1][c+1][0] == "w":
                    if not piecePinned or pinDirection == (1 , 1):
                        moves.append(Move((r,c),(r+1,c+1), self.board))
            #add pawn promotions
            
                        

    def getRookMoves(self, r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection =(self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q": # cannot remove piece from pin list until we have calculated bishop moves as the queen uses getRookMoves and getBishopMoves
                    self.pins.remove(self.pins[i])
                    break
        
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break #friendly piece is only option left so we break
                    else:
                        break # move is of board so we break

    def getKnightMoves(self, r,c,moves):
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        KnightMoves = ((-2, 1), (-2, -1), (2, 1), (2, -1), (-1, -2), (-1, 2), (1, 2), (1, -2))
        allyColor = "w" if self.whiteToMove else "b"
        for m in KnightMoves:
            endRow = r +m[0]
            endCol = c +m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  #checks if square is either enemy piece or free
                        moves.append(Move((r, c), (endRow, endCol), self.board))    

    def getBishopMoves(self, r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection =(self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break #friendly piece is only option left so we break
                    else:
                        break # move is of board so we break

    def getQueenMoves(self, r,c,moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r,c,moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  #checks if square is either enemy piece or free
                    #move king and check to see if the move would put the king in check
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:  
                     moves.append(Move((r, c), (endRow, endCol), self.board))
                    #put the king back
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColour = "b"
            allyColour = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColour = "w"
            allyColour = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        #scan outward from the King for pins and checks in every direction (Knights handled seperately)
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  
        #0 to 3 are up down left right , 4 to 7 are diagonals, 4 and 5 are white pawn captures, 6 and 7 are black pawn captures
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1 ,8): # max 7 moves possible from one end of board to the other
                endRow = startRow +d[0] * i
                endCol = startCol +d[1] * i
                if 0 <= endRow < 8 and 0 < endCol < 8:  # check the position is on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColour and endPiece[1] != "K":
                        if possiblePin == (): #first ally piece encountered in this direction
                            possiblePin = (endRow, endCol, d[0], d[1]) #grab locations of pinned piece and the squares which would block the pin
                        else:
                            break # if there is allready a pinned piece in this direction then no other piece can be pinned
                    elif endPiece[0] == enemyColour:
                        type = endPiece[1]
                        #need to check two conditions:  what the piece is and what direction is being checked,   
                        # Rooks from same col / row  
                        # Bishops from diagonals  
                        # Queens from any direction, 
                        # Pawns from diagonal and one square    
                        #king and once square will be added here as a condition to stop kings moving into check
                        if (0 <= j <= 3 and type == "R") or \
                            (4 <= j <= 7 and type == "B") or \
                            (i == 1 and type == "P" and ((enemyColour == "w" and  6 <= j <=7) or (enemyColour == "b" and 4 <= j <= 5 ))) or \
                            (type == "Q") or \
                            (i == 1 and type == "K"):
                            if possiblePin == (): # if there is no ally piece blocking the attack line
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1])) # grab square of attacking piece and all the squares to block the check
                                break
                            else: # ally piece blockign and so there is a pin
                                pins.append(possiblePin)
                                break
                        else: #enemy piece not able to check the king
                            break
                else: #looking off the board
                    break
                
        #Knight checks just look for Knight moves from the kings position
        knightMoves  = ((-2, 1), (-2, -1), (2, 1), (2, -1), (-1, -2), (-1, 2), (1, 2), (1, -2))
        for m in knightMoves:
            endRow = startRow + m [0]
            endCol = startCol + m [1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColour and endPiece[1] == "N":   #if the piece is an enemy Knight
                    inCheck =True
                    checks.append((endRow, endCol, m[0], m[1]))
                    
        return inCheck, pins, checks
                        
                        
class Move():
    #rows and cols to ranks and files
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8": 0}
    rowsToRanks = {v : k for k, v in ranksToRows.items()}
    
    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h": 7}
    colsToFiles = {v : k for k, v in filesToCols.items()}

    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        
        self.pieceMoved =board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow *1000 + self.startCol * 100 + self.endRow *10 + self.endCol
            
            
    #overriding the equals method because of the move class conflicting with mouse clicks
    
    def __eq__(self,other):
        if isinstance (other, Move):
            return self.moveID == other.moveID
        return False
                
            
        #Basic notation   add proper notation later with captures and piece moves and removing pawn name + castling
    def getChessNotation(self):
            return self.getRankfile(self.startRow ,self.startCol) + self.getRankfile(self.endRow, self.endCol)
            
    def getRankfile(self, r, c):
            return self.colsToFiles[c] + self.rowsToRanks[r]
            
        