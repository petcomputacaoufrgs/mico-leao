import PySimpleGUI as sg

def Result(position,gameIc, player):
    if player == False:
        gameIc.gameBoard[position] = "O"

    else:
        gameIc.gameBoard[position] = "X"
    return gameIc

def Terminal(gameBoard):

        for i in range(3):
            if gameBoard[(i*3)] == gameBoard[(i*3)+1] == gameBoard[(i*3)+2] != " ":
                return True
            
        for i in range(3):
            if gameBoard[i] == gameBoard[i+3] == gameBoard[i+6] != " ":
                return True
        if gameBoard[0] == gameBoard[4] == gameBoard[8] != " ":
            return True
        elif gameBoard[2] == gameBoard[4] == gameBoard[6] != " ":
            return True
        elif " " not in gameBoard:
            return True
        else:
            return False 
        
class Game:
    def __init__(self):
        self.gameBoard = list(" "*9)
    def Assing (self, position):
        self.gameBoard[position] = "X"
        return 
    def show(self):
        for i in range(3):
            print(f"|{self.gameBoard[i*3]}|{self.gameBoard[(i*3)+1]}|{self.gameBoard[(i*3)+2]}|")
        pass
    def Evaluate(self,value):
        if value == 1:
            print("You Lose")
        elif value == -1:
            print("You Win")
        elif value == 0:
            print("Draw")
        else:
            return 0 
    def Value(self):
        for i in range(3):
            if self.gameBoard[(i*3)] == self.gameBoard[(i*3)+1] == self.gameBoard[(i*3)+2] == "O":
                return 1
            
        for i in range(3):
            if self.gameBoard[i] == self.gameBoard[i+3] == self.gameBoard[i+6] == "O":
                return 1
        if self.gameBoard[0] == self.gameBoard[4] == self.gameBoard[8] == "O":
            return 1
        elif self.gameBoard[2] == self.gameBoard[4] == self.gameBoard[6] == "O":
            return 1
        
        for i in range(3):
            if self.gameBoard[(i*3)] == self.gameBoard[(i*3)+1] == self.gameBoard[(i*3)+2] == "X":
                return -1
            
        for i in range(3):
            if self.gameBoard[i] == self.gameBoard[i+3] == self.gameBoard[i+6] == "X":
                return -1
        if self.gameBoard[0] == self.gameBoard[4] == self.gameBoard[8] == "X":
            return -1
        elif self.gameBoard[2] == self.gameBoard[4] == self.gameBoard[6] == "X":
            return -1
        elif " " not in self.gameBoard:
            return 0
        else:
            return None 
    def IsValid(self,position):
        if position < 0 or position > 8:
            return False
        if self.gameBoard[int(position)] == " ":
            return True
        else:
            return False     
    def teste(self):
        self.gameBoard = ["X","X","X",""," "," "," "," "," "]
        self.Evaluate(self.Value())
        self.gameBoard = ["O","O","O",""," "," "," "," "," "]
        self.Evaluate(self.Value())
        self.gameBoard = ["X"," "," ","X"," "," ","X"," "," "]
        self.Evaluate(self.Value())
        self.gameBoard = ["O"," "," ","O"," "," ","O"," "," "]
        self.Evaluate(self.Value())
        self.gameBoard = ["X"," "," "," ","X"," "," "," ","X"]
        self.Evaluate(self.Value())
        self.gameBoard = ["O"," "," "," ","O"," "," "," ","O"]
        self.Evaluate(self.Value())
        self.gameBoard = [" "," ","X"," ","X"," ","X"," "," "]
        self.Evaluate(self.Value())
        self.gameBoard = [" "," ","O"," ","O"," ","O"," "," "]
        self.Evaluate(self.Value())
        self.gameBoard = ["X","X","O","O","O","X","X","O","O"]
        self.Evaluate(self.Value())
    
    def Reset(self):
        self.gameBoard = list(" "*9)
        

class NodeGame:
    def __init__(self,gameBoard):
        self.gameBoard = gameBoard
        self.children = []
        self.value = 0
    
    def Possible(self):
        number = 0
        possible = []
        for game in self.gameBoard:
            if game == " ":
                possible.append(number)
            number +=1
            
        return possible
    def generateChildren(self, gameboard):
        copy = NodeGame(gameboard)
        copy.gameBoard = gameboard
        self.children.append(copy)
        copy.gameBoard = self.gameBoard
        return copy
    def count(self):
        return self.gameBoard.count("X")
    def Value(self):
        for i in range(3):
            if self.gameBoard[(i*3)] == self.gameBoard[(i*3)+1] == self.gameBoard[(i*3)+2] == "O":
                return 1
            
        for i in range(3):
            if self.gameBoard[i] == self.gameBoard[i+3] == self.gameBoard[i+6] == "O":
                return 1
        if self.gameBoard[0] == self.gameBoard[4] == self.gameBoard[8] == "O":
            return 1
        elif self.gameBoard[2] == self.gameBoard[4] == self.gameBoard[6] == "O":
            return 1
        
        for i in range(3):
            if self.gameBoard[(i*3)] == self.gameBoard[(i*3)+1] == self.gameBoard[(i*3)+2] == "X":
                return -1
            
        for i in range(3):
            if self.gameBoard[i] == self.gameBoard[i+3] == self.gameBoard[i+6] == "X":
                return -1
        if self.gameBoard[0] == self.gameBoard[4] == self.gameBoard[8] == "X":
            return -1
        elif self.gameBoard[2] == self.gameBoard[4] == self.gameBoard[6] == "X":
            return -1
        elif " " not in self.gameBoard:
            return 0
        else:
            return None
    def show(self):
        for i in range(3):
            print(f"|{self.gameBoard[i*3]}|{self.gameBoard[(i*3)+1]}|{self.gameBoard[(i*3)+2]}|")
        pass
    def setValue(self,value):
        self.value = value
        return 
    def getValue(self):

        return self.value
    
def Minimax(game, IsMaximizingPlayer):
    score = game.Value()
    if score == 1:
        return score
    elif score == -1:
        return score
    elif score == 0:
        return score
    
    if IsMaximizingPlayer:
        
        value = -1000
        for action in game.Possible():
            board = game.gameBoard[:]
            copy = NodeGame(board)
            Result(int(action),copy, False)
            value = max(value,Minimax(copy, False))
            game.children.append(copy)
            game.setValue(value)
        return value
    else:
        
        value = 1000
        for action in game.Possible():
            board = game.gameBoard[:]
            copy = NodeGame(board)
            Result(int(action),copy, True)
            value = min(value,Minimax(copy, True))
            game.children.append(copy)
            game.setValue(value)
        return value

def TurnToString(value):
    if value == -1:
        return "You Win \n Try Again?"
    elif value == 1:
        return "You Lose \n Try Again?"
    elif value == 0:
        return "Draw \n Try Again?"
    
def AfterGame(board, window):
    if sg.PopupYesNo(TurnToString(board.Value()),title="Game Over") == "Yes":
        board.Reset()
        for i in range (9):
            window[f"{i}"].update(" ")
        return True
    else:
        return False