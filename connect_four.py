# connect_four.py
# Yingqi Ding
# The game Connect Four.

import copy
import random

class Board:   
    def __init__(self, width, height):
        self.width = width
        self.height = height
        #boardStatus[column][row]
        self.boardState = [[-1] * self.height for index in range(self.width)]
        
    def getWidth(self):
        return self.width
        
    def getHeight(self):
        return self.height
    
    def testLegal(self, move):
        if move in range(self.width):
            if self.boardState[move][0] == -1:
                return True
        return False
    
    def play(self, playerN, move):
        if self.testLegal(move):
            row = 0
            while ((row+1 < self.height)\
                   and (self.boardState[move][row + 1] == -1)):
                row += 1
            self.boardState[move][row] = playerN
            return True, move, row
        return False, None, None
    
    def playerWin(self, player, col, row):
        if self.boardState[col][row] != player:
            return False
        
        horizontal = 1
        nextCol = col - 1
        while nextCol >= 0\
              and self.boardState[nextCol][row] == player:
            nextCol -= 1
            horizontal += 1
        nextCol = col + 1
        while nextCol < self.width\
              and self.boardState[nextCol][row] == player:
            nextCol += 1
            horizontal += 1
        if horizontal >= 4:
            return True
        
        vertical = 1
        nextRow = row + 1
        while nextRow < self.height\
              and self.boardState[col][nextRow] == player:
            nextRow += 1
            vertical += 1
        if vertical >= 4:
            return True
        
        diagonal = 1
        nextCol, nextRow = col-1, row-1
        while nextCol >= 0\
              and nextRow >= 0\
              and self.boardState[nextCol][nextRow] == player:
            nextCol -= 1
            nextRow -= 1
            diagonal += 1
        nextCol, nextRow = col+1, row+1
        while nextCol < self.width\
              and nextRow < self.height\
              and self.boardState[nextCol][nextRow] == player:
            nextCol += 1
            nextRow += 1
            diagonal += 1
        if diagonal >= 4:
            return True
        
        viceDiagonal = 1
        nextCol, nextRow = col-1, row+1
        while nextCol >= 0\
              and nextRow < self.height\
              and self.boardState[nextCol][nextRow] == player:
            nextCol -= 1
            nextRow += 1
            viceDiagonal += 1
        nextCol, nextRow = col+1, row-1
        while nextCol < self.width and nextRow >= 0 and self.boardState[nextCol][nextRow] == player:
            nextCol += 1
            nextRow -= 1
            viceDiagonal += 1
        if viceDiagonal >= 4:
            return True
        return False
    
    def full(self):
        for col in range(self.width):
            if self.boardState[col][0] == -1:
                return False
        return True
    
    def showBoard(self):
        status = [" ", "x", "o"]
        for row in range(self.width):
            for col in range(self.height):
                i = self.boardState[col][row] + 1
                print(status[i], end = "")
            print()
        for n in range(self.width):
            print(n, end = "")
        print()

class Player:
    def __init__(self, playerType, playerN):
        if playerType == "human":
            self.type = "human"
        if playerType == "AI":
            self.type = "AI"
        if playerType == "random":
            self.type = "random"
        self.num = playerN
    
    def getMove(self, board):
        if self.type == "human":
            board.showBoard()
            move = int(input("Please enter your next move."))
        
        if self.type == "AI":
            legalMoves = []
            scores = []
            for move in range(board.width):
                if board.testLegal(move):
                    legalMoves.append(move)
                    scores.append(0)
            for move in legalMoves:
                newBoard = copy.deepcopy(board)
                success, col, row = newBoard.play(self.num, move)
                if newBoard.playerWin(self.num, col, row):
                    scores[legalMoves.index(move)] = 9999
                else:
                    for trial in range(1000):
                        testGame = GameState(copy.deepcopy(newBoard),"random", "random", 1 - self.num)
                        scores[legalMoves.index(move)] += ((-1) ** self.num) * testGame.playOut()
            bestScore = -9999
            for score in scores:
                if score > bestScore:
                    bestScore = score
            bestScoreIndices = []
            for i in range(len(scores)):
                if scores[i] == bestScore:
                    bestScoreIndices.append(i)
            bestScoreIndex = random.choice(bestScoreIndices)
            move = legalMoves[bestScoreIndex]
            
        if self.type == "random":
            legalMoves = []
            for move in range(board.width):
                if board.testLegal(move):
                    legalMoves.append(move)
            move = random.choice(legalMoves)
        
        return move

class GameState:
    def __init__(self, board, player0Type, player1Type, currentPlayer = 0):
        self.board = board
        self.player0 = Player(player0Type, 0)
        self.player1 = Player(player1Type, 1)
        self.currentPlayer = currentPlayer
        
    def takeTurn(self):
        if self.currentPlayer == 0:
            nextMove = self.player0.getMove(self.board)
        if self.currentPlayer == 1:
            nextMove = self.player1.getMove(self.board)
        success, col, row = self.board.play(self.currentPlayer, nextMove)
        
        if not success:
            print("Please make a legal move.")
            return None
        if self.board.playerWin(self.currentPlayer, col, row):
            if self.currentPlayer == 0:
                return 1
            if self.currentPlayer == 1:
                return -1
        if self.board.full():
            return 0
        
        self.currentPlayer = 1 - self.currentPlayer
        return None
    
    def playOut(self):
        result = None
        while (result == None):
            result = self.takeTurn()
        return result

def main():
    print("Welcome! In Connect Four, two players can drop pieces from the top\n\
into a vertically suspended grid. The pieces fall and occupy the lowest\n\
available spaces in the grid. The player who first connects four pieces\n\
in the horizontal, vertical, or diagonal line will win!") 
    print("First player plays x and second player plays o.")
    size = int(input("You can choose the size of the board(integers): "))
    newBoard = Board(size, size)
    randomNum = random.random()
    if randomNum < 0.5:
        print ("You move first!")
        newGame = GameState(newBoard, "human", "AI") 
        result = newGame.playOut()
        if result == 1:
            newBoard.showBoard()
            print("You win!")
        if result == -1:
            newBoard.showBoard()
            print("AI wins!")
        if result == 0:
            newBoard.showBoard()
            print("It's a tie...")
    else: 
        print ("You go second.")
        newGame = GameState(newBoard, "AI", "human")
        result = newGame.playOut()
        if result == 1:
            newBoard.showBoard()
            print("AI wins!")
        if result == -1:
            newBoard.showBoard()
            print("You win!")
        if result == 0:
            newBoard.showBoard()
            print("It's a tie...")

if __name__ == "__main__":
    main()
