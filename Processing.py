import PySimpleGUI as telinha


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
    
def Step(state,move):
    # layoutChildDisplay = [[telinha.Text("Child Display")]]
    # childWindow = telinha.Window("Child Display", layoutChildDisplay, margins=(70,100))
    
    actualBoard = Game()
    actualBoard.gameBoard = list(state)

    while True:
        
        play = int(move)
        if actualBoard.IsValid(play):
            actualBoard.Assing(play)
            
            board = actualBoard.gameBoard[:]
            InitNode = NodeGame(board)
            if actualBoard.Evaluate(actualBoard.Value()) == 0:
                Minimax(InitNode, True)
                best = 0
                index = 0
                counter = 0
                for children in InitNode.children:
                    
                    if children.getValue() >= best:
                        best = children.getValue()
                        counter = index
                    index +=1
                        
                actualBoard.gameBoard = InitNode.children[counter].gameBoard
                return InitNode,actualBoard,actualBoard.Evaluate(actualBoard.Value())
                    
            else:
                return InitNode,actualBoard,actualBoard.Evaluate(actualBoard.Value())   #terminou alguma coisa 
        else:
            currentState = Game()
            currentState.gameBoard = list(state)
            return NodeGame(state),currentState,0  #pop pop pop pop pop pop pop por pop pop pop pop
    
# def AfterGame(board, window):
#     if telinha.PopupYesNo(TurnToString(board.Value()),title="Game Over") == "Yes":
#         board.Reset()
#         for i in range (9):
#             window[f"{i}"].update(" ")
#         return True
#     else:
#         return False

# def DrawGame(game):
#     layoutSTART = [[telinha.Text('Welcome to Tic Tac Toe. '), telinha.Text("Press in your play: ")],
#             [telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="0"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="1"), telinha.Button(" ",size=(widthBUTTON ,heightBUTTON),key="2")],
#             [telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="3"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="4"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON ),key="5")],
#             [telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="6"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="7"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON ),key="8")]]

#     StartWindow = telinha.Window("Tic Tac Toe", layoutSTART,margins=(70,100))
#     while True:
#         element = gameStart()
#         for elements in element:
#             StartWindow[elements].update("X")
            
# def DrawMenu():
#     layout = [
#             [telinha.Text(text='PET Computação',
#                    font=('Arial Bold', 25),
#                    size=20,
#                    expand_x=True,
#                    justification='center')],
#             [telinha.Text(text='Jogo da Velha\n',
#                    font=('Arial Bold', 18),
#                    size=20,
#                    expand_x=True,
#                    justification='center')],
#             [telinha.Button('Começar', size=(15,1)), telinha.Exit('Sair', size=(15,1))],
#             [telinha.Text(text='Vitórias: 0',
#                    font=('Arial Bold', 10),
#                    size=15,
#                    expand_x=True,
#                    justification='center',
#                    key='v'),
#             telinha.Text(text='Empates: 0',
#                    font=('Arial Bold', 10),
#                    size=15,
#                    expand_x=True,
#                    justification='center',
#                    key='e'),
#             telinha.Text(text='Derrotas: 0',
#                    font=('Arial Bold', 10),
#                    size=15,
#                    expand_x=True,
#                    justification='center',
#                    key='d'),
#             ]
#             ]
    
#     window = telinha.Window('PET Computação', layout, element_justification='c', margins=(70,140))

#     while True:
#         event, values = window.read()
#         if event in (telinha.WIN_CLOSED, 'Sair'):
#             exit()
#         elif event == 'Começar':
#             window.close()
#             DrawGame(Game())
#             break 
            
# ### main
# ###
# ### drawMenu()
# ### while True:
# ###     drawGame()