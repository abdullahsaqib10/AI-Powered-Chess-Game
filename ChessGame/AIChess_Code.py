import copy
import random

allRows = [8    ,   7,  6,   5,   4,      3,      2,      1]
allCols = ['a',     'b',     'c',    'd',    'e',    'f',    'g',    'h']

whitePieces = ['wp',    'wR',   'wN',   'wB',   'wK',   'wQ']
blackPieces = ['bB',    'bK',   'bQ',   'bp',   'bR',   'bN']

#define a piece class
class ChessPiece:
    def __init__(self,   name,   color, row, col, symbol, value, attackingValue):
        self.name =name
        self.color =color
        self.row = row
        self.col = col
        self.symbol = symbol
        self.value = value
        self.attackingValue = attackingValue
    
    def evaluate(self, boardState, aiColor):
        #Calculating for black (AI)
        #Material value of the board
        matVal = 0
        for i in range(8):
            for j in range(8):
                if boardState[i][j].color == 'black':
                    matVal = matVal + boardState[i][j].value
        
        #Attacking value of the board
        attVal = 0
        for i in range(8):
            for j in range(8):
                if boardState[i][j].color == 'black':
                    moves = getAllLegalMoves(boardState, i, j)
                    for move in moves:
                        if boardState[move[0]][move[1]].color == 'white':
                            attVal = attVal + boardState[move[0]][move[1]].value
        
        #King safety
        kingSafety = 0
        bKRow, bKCol = getKingPos(boardState, 'black')
        playerMoves = getAllPossibleMoves(boardState, 'white')
        for move in playerMoves:
            if move[2] == bKRow and move[3] == bKCol:
                kingSafety = kingSafety - 1
        
        blackVal = matVal + attVal + kingSafety

        #Calculating for white (player)
        #Material value of the board
        matVal = 0
        for i in range(8):
            for j in range(8):
                if boardState[i][j].color == 'white':
                    matVal = matVal + boardState[i][j].value
        
        #Attacking value of the board
        attVal = 0
        for i in range(8):
            for j in range(8):
                if boardState[i][j].color == 'white':
                    moves = getAllLegalMoves(boardState, i, j)
                    for move in moves:
                        if boardState[move[0]][move[1]].color == 'black':
                            attVal = attVal + boardState[move[0]][move[1]].value
        
        #King safety
        kingSafety = 0
        wKRow, wKCol = getKingPos(boardState, 'white')
        aiMoves = getAllPossibleMoves(boardState, 'black')
        for move in aiMoves:
            if move[2] == wKRow and move[3] == wKCol:
                kingSafety = kingSafety - 1

        whiteVal = matVal + attVal + kingSafety

        if aiColor == 'black':
            return blackVal - whiteVal
        else:
            return whiteVal - blackVal


    def minimax(self, boardState, depth, alpha, beta, maximizing, userColor, aiColor):
        if depth == 0:
            return self.evaluate(boardState, aiColor), None

        if maximizing == True:
            maxEval = float('-inf')
            allMoves = getAllPossibleMoves(boardState, aiColor)
            allMoves2 = []
            bestMove = None

            kRow, kCol = getKingPos(boardState, aiColor)
            if aiColor == 'white':
                if boardState[kRow][kCol].isWhiteInCheck(boardState, kRow, kCol) == True:
                    for move in allMoves:
                        tempBoardState = copy.deepcopy(boardState)
                        row1 = move[0]
                        col1 = move[1]
                        row2 = move[2]
                        col2 = move[3]
                        movePiece(tempBoardState, row1, col1, row2, col2)
                        kRow, kCol = getKingPos(tempBoardState, aiColor)
                        if tempBoardState[kRow][kCol].isWhiteInCheck(tempBoardState, kRow, kCol) == False:
                            allMoves2.append(move)
                            # bestMove = move
                            # return maxEval, bestMove
                else:
                    allMoves2 = allMoves
            else:
                if boardState[kRow][kCol].isBlackInCheck(boardState, kRow, kCol) == True:
                    for move in allMoves:
                        tempBoardState = copy.deepcopy(boardState)
                        row1 = move[0]
                        col1 = move[1]
                        row2 = move[2]
                        col2 = move[3]
                        movePiece(tempBoardState, row1, col1, row2, col2)
                        kRow, kCol = getKingPos(tempBoardState, aiColor)
                        if tempBoardState[kRow][kCol].isBlackInCheck(tempBoardState, kRow, kCol) == False:
                            allMoves2.append(move)
                            # bestMove = move
                            # return maxEval, bestMove
                else:
                    allMoves2 = allMoves
                

            for move in allMoves2:
                tempBoardState = copy.deepcopy(boardState)
                row1 = move[0]
                col1 = move[1]
                row2 = move[2]
                col2 = move[3]
                movePiece(tempBoardState, row1, col1, row2, col2)
                kRow, kCol = getKingPos(tempBoardState, aiColor)
                if aiColor == 'white':
                    if tempBoardState[kRow][kCol].isWhiteInCheck(tempBoardState, kRow, kCol) == False:
                        eval = self.minimax(tempBoardState, depth - 1, alpha, beta, False, userColor, aiColor)[0]
                        if eval > maxEval:
                            maxEval = eval
                            bestMove = move
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                else:
                    if tempBoardState[kRow][kCol].isBlackInCheck(tempBoardState, kRow, kCol) == False:
                        eval = self.minimax(tempBoardState, depth - 1, alpha, beta, False, userColor, aiColor)[0]
                        if eval > maxEval:
                            maxEval = eval
                            bestMove = move
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break

            
            return maxEval, bestMove
        else:
            minVal = float('inf')
            allMoves = getAllPossibleMoves(boardState, userColor)

            for move in allMoves:
                tempBoardState = copy.deepcopy(boardState)
                row1 = move[0]
                col1 = move[1]
                row2 = move[2]
                col2 = move[3]
                movePiece(tempBoardState, row1, col1, row2, col2)
                eval = self.minimax(tempBoardState, depth - 1, alpha, beta, True, userColor, aiColor)[0]
                if eval < minVal:
                    minVal = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            return minVal, None


class Pawn(ChessPiece):
    def __init__(self,  name,    color, row, col, symbol, value, attackingValue):
        super().__init__(name, color, row, col, symbol, value, attackingValue)

    def move(self, boardState, row, col, toRow, toCol):
        if self.color == 'white':
            if row == 6:
                if (toRow == 4 or toRow == 5) and toCol == col:
                    if boardState[toRow][toCol].name == '' and boardState[row - 1][toCol].name == '':
                        return True
                if toRow == row - 1 and (toCol == col - 1 or toCol == col + 1):
                    if boardState[toRow][toCol].name in blackPieces: #Taking a piece
                        return True
            else:
                if toRow == row - 1 and toCol == col:
                    if boardState[toRow][toCol].name == '':
                        return True
                if toRow == row - 1 and (toCol == col - 1 or toCol == col + 1):
                    if boardState[toRow][toCol].name in blackPieces: #Taking a piece
                        return True
        if self.color == 'black':
            if row == 1:
                if (toRow == 3 or toRow == 2) and toCol == col:
                    if boardState[toRow][toCol].name == '' and boardState[row + 1][toCol].name == '':
                        return True
                if toRow == row + 1 and (toCol == col - 1 or toCol == col + 1):
                    if boardState[toRow][toCol].name in whitePieces: #Taking a piece
                        return True
            else:
                if toRow == row + 1 and toCol == col:
                    if boardState[toRow][toCol].name == '':
                        return True
                if toRow == row + 1 and (toCol == col - 1 or toCol == col + 1):
                    if boardState[toRow][toCol].name in whitePieces: #Taking a piece
                        return True
        
        return False

class Rook(ChessPiece):
    def __init__(self,  name,    color, row, col, symbol, value, attackingValue):
        super().__init__(name, color, row, col, symbol, value, attackingValue)
    
    def move(self, boardState, row, col, toRow, toCol):
        if row == toRow:
            if col < toCol:
                st = col + 1
                fin = toCol
            else:
                st = toCol + 1
                fin = col
            for i in range(st, fin):
                if boardState[row][i].name != '':
                    return False
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        elif col == toCol:
            if row < toRow:
                st = row + 1
                fin = toRow
            else:
                st = toRow + 1
                fin = row
            for i in range(st, fin):
                if boardState[i][col].name != '':
                    return False
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        else:
            return False

class Knight(ChessPiece):
    def __init__(self,  name,    color, row, col, symbol, value, attackingValue):
        super().__init__(name, color, row, col, symbol, value, attackingValue)
    
    def move(self, boardState, row, col, toRow, toCol):
        if (toRow == row + 2 and ((toCol == col + 1) or (toCol == col - 1))) or (toRow == row - 2 and ((toCol == col + 1 or toCol == col - 1))): 
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        
        if (toCol == col + 2 and ((toRow == row + 1) or (toRow == row - 1))) or (toCol == col - 2 and ((toRow == row + 1) or (toRow == row - 1))): 
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        
        return False

class Bishop(ChessPiece):
    def __init__(self,  name,    color, row, col, symbol, value, attackingValue):
        super().__init__(name, color, row, col, symbol, value, attackingValue)
    
    def move(self, boardState, row, col, toRow, toCol):
        if abs(toRow - row) == abs(toCol - col):
            if toRow > row and toCol > col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row + i][col + i].name != '':
                        return False
            elif toRow > row and toCol < col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row + i][col - i].name != '':
                        return False
            elif toRow < row and toCol > col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row - i][col + i].name != '':
                        return False
            elif toRow < row and toCol < col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row - i][col - i].name != '':
                        return False
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        else:
            return False

class Queen(ChessPiece):
    def __init__(self,  name,    color, row, col, symbol, value, attackingValue):
        super().__init__(name, color, row, col, symbol, value, attackingValue)

    def move(self, boardState, row, col, toRow, toCol):
        if abs(toRow - row) == abs(toCol - col):
            if toRow > row and toCol > col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row + i][col + i].name != '':
                        return False
            elif toRow > row and toCol < col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row + i][col - i].name != '':
                        return False
            elif toRow < row and toCol > col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row - i][col + i].name != '':
                        return False
            elif toRow < row and toCol < col:
                for i in range(1, abs(toRow - row)):
                    if boardState[row - i][col - i].name != '':
                        return False
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        elif row == toRow:
            if col < toCol:
                st = col + 1
                fin = toCol
            else:
                st = toCol + 1
                fin = col
            for i in range(st, fin):
                if boardState[row][i].name != '':
                    return False
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        elif col == toCol:
            if row < toRow:
                st = row + 1
                fin = toRow
            else:
                st = toRow + 1
                fin = row
            for i in range(st, fin):
                if boardState[i][col].name != '':
                    return False
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        else:
            return False

class King(ChessPiece):
    def __init__(self,  name,    color, row, col, symbol, value, attackingValue):
        super().__init__(name, color, row, col, symbol, value, attackingValue)

    def move(self, boardState, row, col, toRow, toCol):
        if abs(row - toRow) <= 1 and abs(col - toCol) <= 1:
            if boardState[row][col].color == 'white':
                if boardState[toRow][toCol].name in whitePieces: #Cannot take own piece
                    return False
            if boardState[row][col].color == 'black':
                if boardState[toRow][toCol].name in blackPieces: #Cannot take own piece
                    return False
            return True
        else:
            return False
    
    def isWhiteInCheck(self, boardState, row, col):
        for i in range(8):
            for j in range(8):
                if boardState[i][j].name in blackPieces:
                    if boardState[i][j].move(boardState, i, j, row, col) == True:
                        return True
        return False

    def isBlackInCheck(self, boardState, row, col):
        for i in range(8):
            for j in range(8):
                if boardState[i][j].name in whitePieces:
                    if boardState[i][j].move(boardState, i, j, row, col) == True:
                        return True
        return False

    def isBlackInCheckMate(self, boardState, row, col):
        #Check if king is in check or not
        if boardState[row][col].isBlackInCheck(boardState, row, col) == False:
            return False

        #Check if king can get out of check by moving
        kingMoves = getAllLegalMoves(boardState, row, col)
        for move in kingMoves:
            tempBoardState = copy.deepcopy(boardState)
            toRow = move[0]
            toCol = move[1]
            movePiece(tempBoardState, row, col, toRow, toCol)
            if tempBoardState[toRow][toCol].isBlackInCheck(tempBoardState, toRow, toCol) == False:
                return False
        
        #Check if any other piece can null the check
        for i in range(8):
            for j in range(8):
                if boardState[i][j].name in blackPieces and boardState[i][j].name != 'bK':
                    pieceMoves = getAllLegalMoves(boardState, i, j)
                    for move in pieceMoves:
                        tempBoardState = copy.deepcopy(boardState)
                        movePiece(tempBoardState, i, j, move[0], move[1])
                        if tempBoardState[row][col].isBlackInCheck(tempBoardState, row, col) == False:
                            return False
        return True
    

    def isWhiteInCheckMate(self, boardState, row, col):
        #Check if king is in check or not
        if boardState[row][col].isWhiteInCheck(boardState, row, col) == False:
            return False

        #Check if king can get out of check by moving
        kingMoves = getAllLegalMoves(boardState, row, col)
        for move in kingMoves:
            tempBoardState = copy.deepcopy(boardState)
            toRow = move[0]
            toCol = move[1]
            movePiece(tempBoardState, row, col, toRow, toCol)
            if tempBoardState[toRow][toCol].isWhiteInCheck(tempBoardState, toRow, toCol) == False:
                return False
        
        #Check if any other piece can null the check
        for i in range(8):
            for j in range(8):
                if boardState[i][j].name in whitePieces and boardState[i][j].name != 'wK':
                    pieceMoves = getAllLegalMoves(boardState, i, j)
                    for move in pieceMoves:
                        tempBoardState = copy.deepcopy(boardState)
                        movePiece(tempBoardState, i, j, move[0], move[1])
                        if tempBoardState[row][col].isWhiteInCheck(tempBoardState, row, col) == False:
                            return False
        return True
        
        

#Get all legal moves a piece on a certain position can make
def getAllLegalMoves(boardState, row, col):
    legalMoves = []
    for i in range(8):
        for j in range(8):
            if boardState[row][col].move(boardState, row, col, i, j) == True:
                if boardState[row][col].name == 'wK':
                    if boardState[row][col].isWhiteInCheck(boardState, i, j) == False:
                        legalMoves.append([i, j])
                elif boardState[row][col].name == 'bK':
                    if boardState[row][col].isBlackInCheck(boardState, i, j) == False:
                        legalMoves.append([i, j])
                else:
                    legalMoves.append([i, j])
    return legalMoves


#Get all possible moves given a board state and the color
def getAllPossibleMoves(boardState, color):
    allPossibleMoves = []
    for i in range(8):
        for j in range(8):
            if boardState[i][j].color == color:
                for k in range(8):
                    for l in range(8):
                        if boardState[i][j].move(boardState, i, j, k, l) == True:
                            if boardState[i][j].name == 'wK':
                                if boardState[i][j].isWhiteInCheck(boardState, k, l) == False:
                                    row1 = i
                                    col1 = j
                                    row2 = k
                                    col2 = l
                                    allPossibleMoves.append([row1, col1, row2, col2])
                            elif boardState[i][j].name == 'bK':
                                if boardState[i][j].isBlackInCheck(boardState, k, l) == False:
                                    row1 = i
                                    col1 = j
                                    row2 = k
                                    col2 = l
                                    allPossibleMoves.append([row1, col1, row2, col2])
                            else:
                                row1 = i
                                col1 = j
                                row2 = k
                                col2 = l
                                allPossibleMoves.append([row1, col1, row2, col2])
                            

    return allPossibleMoves


#Get a random move
def randomMove(boardState, color):
    allPossibleMoves = getAllPossibleMoves(boardState, color)
    randMove = random.choice(allPossibleMoves)
    return randMove
        
    
#Get kings position
def getKingPos(boardState, color):
    row = 0
    col = 0
    if color == 'white':
        for i in range(8):
            for j in range(8):
                if boardState[i][j].name == 'wK':
                    row = i
                    col = j
                    break
    else:
        for i in range(8):
            for j in range(8):
                if boardState[i][j].name == 'bK':
                    row = i
                    col = j
                    break
    
    return row, col


# Function to draw the board
def draw_board(boardState):
    print("    -------------------------")
    for row in range(8):
        print(allRows[row], " |", end = '')
        for col in range(8):
            if boardState[row][col].symbol != '':
                print(boardState[row][col].symbol, end = ' |')
            else:
                print('  ', end = '|')
        print()
    #Write alphabets a to h under each column
    print(end = '   ')
    for col in range(0, 8):
        print(" ", allCols[col], end = '')
    print("    \n-------------------------")

#Move piece on the board
def movePiece(boardState, row, col, toRow, toCol):
    temp = boardState[row][col]
    boardState[row][col] = ChessPiece('', '', -1, -1, '', 0, 0)
    boardState[toRow][toCol] = temp

#Returns result board after applying a move
def boardAfterMove(boardState, row, col, toRow, toCol):
    movePiece(boardState, row, col, toRow, toCol)
    return boardState


#Check if white is in stalemate or not
def checkWhiteStalemate(boardState):
    #Check if any piece can move legally or not
    for i in range(8):
        for j in range(8):
            if boardState[i][j].name in whitePieces and boardState[i][j].name != 'wK':
                pieceMoves = getAllLegalMoves(boardState, i, j)
                if len(pieceMoves) != 0:
                    return False
            
    #Check the king (if it is in check then return false)
    wKRow, wKCol = getKingPos(boardState, 'white')
    if boardState[wKRow][wKCol].isWhiteInCheck(boardState, wKRow, wKCol) == True:
        return False
    
    #Check if the legal moves of the king puts it in check or not
    kingMoves = getAllLegalMoves(boardState, wKRow, wKCol)
    for move in kingMoves:
        tempBoardState = copy.deepcopy(boardState)
        toRow = move[0]
        toCol = move[1]
        movePiece(tempBoardState, wKRow, wKCol, toRow, toCol)
        if tempBoardState[toRow][toCol].isWhiteInCheck(tempBoardState, toRow, toCol) == False:
            return False
    
    return True
        
#Check if black is in stalemate or not
def checkBlackStalemate(boardState):
    #Check if any piece can move legally or not
    for i in range(8):
        for j in range(8):
            if boardState[i][j].name in blackPieces and boardState[i][j].name != 'bK':
                pieceMoves = getAllLegalMoves(boardState, i, j)
                if len(pieceMoves) != 0:
                    return False
            
    #Check the king (if it is in check then return false)
    bKRow, bKCol = getKingPos(boardState, 'black')
    if boardState[bKRow][bKCol].isBlackInCheck(boardState, bKRow, bKCol) == True:
        return False
    
    #Check if the legal moves of the king puts it in check or not
    kingMoves = getAllLegalMoves(boardState, bKRow, bKCol)
    for move in kingMoves:
        tempBoardState = copy.deepcopy(boardState)
        toRow = move[0]
        toCol = move[1]
        movePiece(tempBoardState, bKRow, bKCol, toRow, toCol)
        if tempBoardState[toRow][toCol].isBlackInCheck(tempBoardState, toRow, toCol) == False:
            return False
    
    return True

#Promote white pawn
def promoteWhitePawn(boardState, row, col, aiColor):
    if aiColor == 'white':
        promotion = random.choice(['R','N','B','Q'])
    else:
        promotion = ''
        while promotion not in ['R','N','B','Q']:
            promotion = input("What do you want for your pawn to be promoted to?(R,N,B,Q): ")

    if promotion == 'R':
        boardState[row][col] = Rook('wR', 'white', row, col, '♖', 5, 0)
    elif promotion == 'N':
        boardState[row][col] = Knight('wN', 'white', row, col, '♘', 3, 0)
    elif promotion == 'B':
        boardState[row][col] = Bishop('wB', 'white', row, col, '♗', 3, 0)
    else:
        boardState[row][col] = Queen('wQ', 'white', row, col, '♕', 9, 0)


#Promote black pawn
def promoteBlackPawn(boardState, row, col, aiColor):
    if aiColor == 'black':
        promotion = random.choice(['R','N','B','Q'])
    else:
        promotion = ''
        while promotion not in ['R','N','B','Q']:
            promotion = input("What do you want for your pawn to be promoted to?(R,N,B,Q): ")

    if promotion == 'R':
        boardState[row][col] = Rook('bR', 'black', row, col, '♜', 5, 0)
    elif promotion == 'N':
        boardState[row][col] = Knight('bN', 'black', row, col, '♞', 3, 0)
    elif promotion == 'B':
        boardState[row][col] = Bishop('bB', 'black', row, col, '♝', 3, 0)
    else:
        boardState[row][col] = Queen('bQ', 'black', row, col, '♛', 9, 0)


#Function for user input
def userInput():
    row, col, toRow, toCol = '', '', '', ''
    indexes = [0,1,2,3,4,5,6,7]
    rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    while row not in indexes or col not in indexes or toRow not in indexes or toCol not in indexes:
        row =  input("Enter row: ")
        if row not in rows:
            continue
        row = int(row)
        col = input("Enter col: ")

        toRow =  input("Enter destination row: ")
        if toRow not in rows:
            continue
        toRow = int(toRow)
        toCol = input("Enter destination col: ")



        for i in range(len(allRows)):
            if row == allRows[i]:
                row = i
                break
        for i in range(len(allRows)):
            if toRow == allRows[i]:
                toRow = i
                break

        for i in range(len(allCols)):
            if col == allCols[i]:
                col = i
                break
        for i in range(len(allCols)):
            if toCol == allCols[i]:
                toCol = i
                break
    
    return row, col, toRow, toCol





bp1 = Pawn('bp', 'black', 1, 0, '♟', 1, 0)
bp2 = Pawn('bp', 'black', 1, 1, '♟', 1, 0)
bp3 = Pawn('bp', 'black', 1, 2, '♟', 1, 0)
bp4 = Pawn('bp', 'black', 1, 3, '♟', 1, 0)
bp5 = Pawn('bp', 'black', 1, 4, '♟', 1, 0)
bp6 = Pawn('bp', 'black', 1, 5, '♟', 1, 0)
bp7 = Pawn('bp', 'black', 1, 6, '♟', 1, 0)
bp8 = Pawn('bp', 'black', 1, 7, '♟', 1, 0)

bR1 = Rook('bR', 'black', 0, 0, '♜', 5, 0)
bR2 = Rook('bR', 'black', 0, 7, '♜', 5, 0)
bN1 = Knight('bN', 'black', 0, 1, '♞', 3, 0)
bN2 = Knight('bN', 'black', 0, 6, '♞', 3, 0)
bB1 = Bishop('bB', 'black', 0, 2, '♝', 3, 0)
bB2 = Bishop('bB', 'black', 0, 5, '♝', 3, 0)
bQ = Queen('bQ', 'black', 0, 3, '♛', 9, 0)
bK = King('bK', 'black', 0, 4, '♚', 100, 0)

wp1 = Pawn('wp', 'white', 6, 0, '♙', 1, 0)
wp2 = Pawn('wp', 'white', 6, 1, '♙', 1, 0)
wp3 = Pawn('wp', 'white', 6, 2, '♙', 1, 0)
wp4 = Pawn('wp', 'white', 6, 3, '♙', 1, 0)
wp5 = Pawn('wp', 'white', 6, 4, '♙', 1, 0)
wp6 = Pawn('wp', 'white', 6, 5, '♙', 1, 0)
wp7 = Pawn('wp', 'white', 6, 6, '♙', 1, 0)
wp8 = Pawn('wp', 'white', 6, 7, '♙', 1, 0)

wR1 = Rook('wR', 'white', 7, 0, '♖', 5, 0)
wR2 = Rook('wR', 'white', 7, 7, '♖', 5, 0)
wN1 = Knight('wN', 'white', 7, 1, '♘', 3, 0)
wN2 = Knight('wN', 'white', 7, 6, '♘', 3, 0)
wB1 = Bishop('wB', 'white', 7, 2, '♗', 3, 0)
wB2 = Bishop('wB', 'white', 7, 5, '♗', 3, 0)
wQ = Queen('wQ', 'white', 7, 3, '♕', 9, 0)
wK = King('wK', 'white', 7, 4, '♔', 100, 0)

empty = ChessPiece('', '', -1, -1, '', 0, 0)


#Initial State of board
boardState = [
    [bR1,bN1,bB1,bQ,bK,bB2,bN2,bR2],
    [bp1,bp2,bp3,bp4,bp5,bp6,bp7,bp8],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [empty,empty,empty,empty,empty,empty,empty,empty],
    [wp1,wp2,wp3,wp4,wp5,wp6,wp7,wp8],
    [wR1,wN1,wB1,wQ,wK,wB2,wN2,wR2]
]


# #Initial State of board
# boardState = [
#     [empty,bR1,empty,bK,empty,bB2,bN2,bR2],
#     [bp1,bp2,empty,empty,bp3,bp4,empty,bp5],
#     [empty,empty,bp6,bp7,empty,empty,bp8,empty],
#     [empty,empty,bN1,empty,wp5,bQ,empty,empty],
#     [wp1,empty,empty,empty,empty,wB1,empty,empty],
#     [empty,empty,wN1,wp4,empty,empty,wp7,wN2],
#     [empty,wp2,wp3,empty,empty,wp6,empty,wp8],
#     [wR1,empty,empty,wQ,empty,wK,empty,wR2]
# ]







turns = 2
whiteHistory = []
blackHistory = []

userColor = ''
clrs = ['white', 'black']
while userColor not in clrs:
    userColor = input("Enter the color you want to play as (white/black): ")


if userColor == "white":
    aiColor = "black"
else:
    aiColor = "white"

# Draw the initial board state
draw_board(boardState)

while turns > 0:

    
    if turns % 2 == 0:
        print("White's turn")

        #Check if the game is a draw (stalemate)
        if checkWhiteStalemate(boardState) == True:
            print("Stalemate! The game is a draw!")
            break

        if userColor == "white":
            row, col, toRow, toCol = userInput()
        else:
            AiMove = boardState[0][0].minimax(boardState, 3, float('-inf'), float('inf'), True, userColor, aiColor)[1]
            if AiMove == None:
                AiMove = randomMove(boardState, aiColor)
            row = AiMove[0]
            col = AiMove[1]
            toRow = AiMove[2]
            toCol = AiMove[3]
        
    else:
        print("Black's turn")

        if checkBlackStalemate(boardState) == True:
            print("Stalemate! The game is a draw!")
            break

        if userColor == "black":
            row, col, toRow, toCol = userInput()
        else:
            AiMove = boardState[0][0].minimax(boardState, 3, float('-inf'), float('inf'), True, userColor, aiColor)[1]
            if AiMove == None:
                AiMove = randomMove(boardState, aiColor)
            row = AiMove[0]
            col = AiMove[1]
            toRow = AiMove[2]
            toCol = AiMove[3]
        

    

    

    #White moves
    if boardState[row][col].name in whitePieces and turns % 2 == 0:
        if boardState[row][col].move(boardState, row, col, toRow, toCol) == False: #when the piece is not allowed to move to that position
            print("Invalid move")
        else:
            tempBoardState = copy.deepcopy(boardState)
            movePiece(tempBoardState, row, col, toRow, toCol)
            wKRow, wKCol = getKingPos(tempBoardState, 'white')
            if tempBoardState[wKRow][wKCol].isWhiteInCheck(tempBoardState, wKRow, wKCol) == True: #when the king is in check
                print("You are in check. You must move your king out of check")
            else:
                movePiece(boardState, row, col, toRow, toCol)

                dispRow1 = 8 - row
                dispRow2 = 8 - toRow
                dispCol1, dispCol2 = '', ''
                for x in range(8):
                    if col == x:
                        dispCol1 = allCols[x]
                        break
                for x in range(8):
                    if toCol == x:
                        dispCol2 = allCols[x]
                        break
                
                print("White has moved " , boardState[toRow][toCol].symbol, " from ",  dispRow1, dispCol1, "to", dispRow2, dispCol2)


                #Check for pawn promotion
                if boardState[toRow][toCol].name == 'wp' and toRow == 0:
                    draw_board(boardState)
                    promoteWhitePawn(boardState, toRow, toCol, aiColor)

                draw_board(boardState)
                turns += 1
                whiteHistory.append([row, col, toRow, toCol])

                #print("All possible moves for white: :", getAllPossibleMoves(boardState, 'white'))

    #Black moves
    if boardState[row][col].name in blackPieces and turns % 2 == 1:
        if boardState[row][col].move(boardState, row, col, toRow, toCol) == False: #When the piece is not able to move to the destination
            print("Invalid move")
        else:
            tempBoardState = copy.deepcopy(boardState)
            movePiece(tempBoardState, row, col, toRow, toCol)
            bKRow, bKCol = getKingPos(tempBoardState, 'black')
            if tempBoardState[bKRow][bKCol].isBlackInCheck(tempBoardState, bKRow, bKCol) == True: #When the king is in check
                print("You are in check. You must move your king out of check")
            else:
                movePiece(boardState, row, col, toRow, toCol)

                dispRow1 = 8 - row
                dispRow2 = 8 - toRow
                dispCol1, dispCol2 = '', ''
                for x in range(8):
                    if col == x:
                        dispCol1 = allCols[x]
                        break
                for x in range(8):
                    if toCol == x:
                        dispCol2 = allCols[x]
                        break
                
                print("Black has moved " , boardState[toRow][toCol].symbol, " from ", dispRow1, dispCol1, " to ", dispRow2, dispCol2)

                #Check for pawn promotion
                if boardState[toRow][toCol].name == 'bp' and toRow == 7:
                    draw_board(boardState)
                    promoteBlackPawn(boardState, toRow, toCol, aiColor)

                draw_board(boardState)
                turns += 1

                blackHistory.append([row, col, toRow, toCol])

                #print("black evaluation: ", boardState[toRow][toCol].evaluate(boardState))
                #print("All possible moves for black: :", getAllPossibleMoves(boardState, 'black'))
    
    #Checking for check (white)
    wKRow, wKCol = getKingPos(boardState, 'white')
    if boardState[wKRow][wKCol].isWhiteInCheck(boardState, wKRow, wKCol) == True: #when the king is in check
        print("WHITE IS IN CHECK!")
    
    #Checking for check (black)
    bKRow, bKCol = getKingPos(boardState, 'black')
    if boardState[bKRow][bKCol].isBlackInCheck(boardState, bKRow, bKCol) == True: #when the king is in check
        print("BLACK IS IN CHECK!")

    # Check if white's king is in check mate
    wKRow, wKCol = getKingPos(boardState, 'white')
    if boardState[wKRow][wKCol].isWhiteInCheckMate(boardState, wKRow, wKCol) == True:
        print("Checkmate! Black wins!")
        break

    # Check if black's king is in check mate
    bKRow, bKCol = getKingPos(boardState, 'black')
    if boardState[bKRow][bKCol].isBlackInCheckMate(boardState, bKRow, bKCol) == True:
        print("Checkmate! White wins!")
        break

#White player(USER) History
print("White player history: ", whiteHistory)

#Black player (AI) History
print("Black player history: ", blackHistory)
