from PySide6 import QtCore, QtWidgets, QtGui
import minimax

### Main window class, coordinates other classes
class MainWindow(QtWidgets.QWidget): 
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Jogo da Velha")
        
        ### Current window and current layout
        self.curWindow = None
        self.curLayout = None
    
    @QtCore.Slot()
    
    ### Menu of the game
    def launch(self):
        self.deleteCurrentLayout() 
        self.curWindow = GameMenu(self)
        self.setCurrentLayout()
        
    ### Game started    
    def startGame(self):
        self.deleteCurrentLayout()          # Previous layout must be deleted to change to another layout
        self.curWindow = GameWindow(self)
        self.setCurrentLayout()
    
    ### Change Main Window layout
    def setCurrentLayout(self):
        self.curLayout = self.curWindow.getLayout()
        self.setLayout(self.curLayout)
    
    ### TODO: find better way to delete current layout
    """  Couldnt find another way to delete layout
    Before entering this function, the parent of current layout is the main window
    Apparently to change current layout to another layout every object inside layout must be deleted (i think?)
    However, layout is not iterable, so a for loop wouldnt work
    Basically here the current layout parent is set to a temporary object, so when the temporary object gets
    deleted, there wont be any references to the widgets inside current layout and they all will be deleted""" 
      
    def deleteCurrentLayout(self): 
        QtWidgets.QWidget().setLayout(self.curLayout)
       
    ### Close main window                      
    def closeWindow(self):
        self.close() 

### Coordinates menu of the game      
class GameMenu(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        
        ### Menu layout
        self.layout = QtWidgets.QVBoxLayout(parent)
        
        ### Menu buttons
        self.mainTitle = QtWidgets.QLabel("Jogo da Velha", parent, alignment=QtCore.Qt.AlignCenter)
        self.subTitle = QtWidgets.QLabel("PET Computação", parent, alignment=QtCore.Qt.AlignCenter)
        self.startButton = QtWidgets.QPushButton("Começar", parent)
        self.quitButton = QtWidgets.QPushButton("Sair", parent)
        
        self.mainTitle.setFont(QtGui.QFont('Times', 30))
        self.subTitle.setFont(QtGui.QFont('Times', 15))
        
        self.startButton.clicked.connect(parent.startGame)
        self.quitButton.clicked.connect(parent.closeWindow)
        
        
        self.layout.addWidget(self.mainTitle)
        self.layout.addWidget(self.subTitle)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.quitButton)
    
    ### returns menu layout ready to go   
    def getLayout(self):
        return self.layout

# class EndWindow(QtWidgets.QWidget):
#     def __init__(self, parent):
#         super().__init__()

#         self.endItOrNot = False
        
#     @staticmethod
#     def askDecision():
        

    
     
      
### Coordinates game window
class GameWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.setParent(parent)
        ### Everythig related to the implementation of the game is here
        self.logic = GameLogic()
        
        ### Dictionary to map each QPushButton to an index (from 0 to 8, since the game board is a list with 9 elements)
        self.buttons = {}
        
        ### Game layout
        self.layout = QtWidgets.QGridLayout(parent)
        
        ### Setting up the buttons
        for row in range(3):
            for column in range(3):
                
                button = QtWidgets.QPushButton(" ", parent)
                button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                button.setFont(QtGui.QFont('Times', 30))
                
                button.clicked.connect(self.getPlayerMove) 
                index = row*3 + column
                self.layout.addWidget(button, row, column)
                
                ### Mapping each button with its respective index
                self.buttons[button] = index
    
    @QtCore.Slot()
    
    ### Return layout ready to go    
    def getLayout(self):
        return self.layout
    
    ### Reads the player move
    def getPlayerMove(self):
        
        ### Get the button which called this function
        button = self.sender()
        
        ### Search for its index (which will be its position on the board)
        index = self.buttons.get(button)
        
        ### Checking if move is valid
        self.logic.registerPlayerMove(button, index)

        self.updateBoard()
        
    ### Update each button on the board
    def updateBoard(self):
        for button in self.buttons:
            index = self.buttons.get(button)
            button.setText(self.logic.gameState.gameBoard[index])
        
        score = self.logic.gameState.evaluateBoard()
        
        if score != None:
            self.parentWidget().launch()
        
### Class coordinates game logic (from minimax.py)
class GameLogic:
    
    def __init__(self):
        
        ### Board class from minimax.py
        self.gameState = minimax.Board()
        ### AI class from minimax.py
        self.ai = minimax.AIPlayer(self.gameState.PLAYER2)
    
    ### Will register move if its a valid move           
    def registerPlayerMove(self, button, index): 
         
        if self.gameState.isValidMove(index): 
            
            self.gameState.registerMove(index, self.gameState.PLAYER1)
            
            if self.ai.gameTree is not None:
                self.ai.updateTreeRoot(self.gameState)
            
            self.getAIMove()
                   
    def getAIMove(self):
        self.gameState = self.ai.makePlay(self.gameState)
