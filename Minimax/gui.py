from PySide6 import QtCore, QtWidgets, QtGui
import minimax
import graphviz

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
        self.closeExtraWindow()     
        self.deleteCurrentLayout() 
        self.curWindow = GameMenu(self)
        self.setCurrentLayout()
        
    ### Game started    
    def startGame(self):        
        self.deleteCurrentLayout()          # Previous layout must be deleted to change to another layout
        self.curWindow = GameWindow(self)
        self.setCurrentLayout()
    
    def endScreen(self, score):
        
        self.deleteCurrentLayout()
        self.curWindow = GameEnd(self, score)
        self.setCurrentLayout()
    
    ### Change Main Window layout
    def setCurrentLayout(self):
        self.curLayout = self.curWindow.getLayout()
        self.setLayout(self.curLayout)
    
    def deleteCurrentLayout(self): 
        QtWidgets.QWidget().setLayout(self.curLayout)
       
    ### Close main window                      
    def closeWindow(self):
        self.close()
        
    def closeEvent(self, event):
        for window in QtWidgets.QApplication.topLevelWidgets():
            window.close()
            
    def closeExtraWindow(self):
        for window in QtWidgets.QApplication.topLevelWidgets():     
            if window.windowTitle() == "Árvore de Decisão":
                window.close()

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

class GameEnd(QtWidgets.QWidget):
    def __init__(self, parent, score):
        super().__init__()
        
        self.setParent(parent)
        self.layout = QtWidgets.QVBoxLayout()
        winMessage = " "
        match score:
            
            case 0:
                winMessage = "Empate! :/"    
            case 1:
                winMessage = "Você perdeu! :("
            case -1:
                winMessage = "Você ganhou! :)"
        
        self.mainTitle = QtWidgets.QLabel(winMessage, parent, alignment=QtCore.Qt.AlignCenter)
        self.startButton = QtWidgets.QPushButton("Jogar de novo", parent)      
        self.quitButton = QtWidgets.QPushButton("Sair", parent)
        
        self.mainTitle.setFont(QtGui.QFont('Times', 30))
        
        self.startButton.clicked.connect(parent.launch)
        self.quitButton.clicked.connect(parent.closeWindow)    
        
        self.layout.addWidget(self.mainTitle)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.quitButton)
        
        
    def getLayout(self):
        return self.layout
        
      
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
        
        self.tree = TreeWindow()
        self.tree.show()
        
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
        self.logic.registerPlayerMove(index)

        self.updateBoard()
        
    ### Update each button on the board
    def updateBoard(self):
        for button in self.buttons:
            index = self.buttons.get(button)
            button.setText(self.logic.gameState.gameBoard[index])
        
        self.tree.updateTreeImage()
        
        score = self.logic.gameState.evaluateBoard()
        
        if score != None:
            self.parentWidget().endScreen(score)
     
class TreeWindow(QtWidgets.QWidget):
    
        
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 600, 600)
        
        self.setWindowTitle("Árvore de Decisão")
        
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        self.view = QtWidgets.QGraphicsView(self)
        
        
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view.setScene(self.scene)

        # Create a QGraphicsPixmapItem to hold the image
        self.image_item = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        self.updateTreeImage()

        # Enable dragging of the view
        self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        
        # Set the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        

    def updateTreeImage(self):
        pixmap = QtGui.QPixmap("tree.png")
        self.image_item.setPixmap(pixmap)
        self.view.fitInView(self.image_item, QtCore.Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        zoom_factor = 1.15 

        if event.angleDelta().y() > 0:
            # Zoom in
            self.view.scale(zoom_factor, zoom_factor)
        else:
            # Zoom out
            self.view.scale(1 / zoom_factor, 1 / zoom_factor)
            
        event.accept()
        
        
        
### Class coordinates game logic
class GameLogic:
    
    def __init__(self):
        
        ### Board class from minimax.py
        self.gameState = minimax.Board()
        ### AI class from minimax.py
        self.ai = minimax.AIPlayer(self.gameState.PLAYER2)
        
        self.treeGraph = DecisionTreeGraph()
    
    ### Will register move if its a valid move           
    def registerPlayerMove(self, index): 
         
        if self.gameState.isValidMove(index): 
            
            self.gameState.registerMove(index, self.gameState.PLAYER1)
            
            if self.ai.gameTree is not None:
                self.ai.updateTreeRoot(self.gameState)
                self.treeGraph.drawTreeNode(self.ai.gameTree)
            
            self.getAIMove()
                   
    def getAIMove(self):
        self.gameState = self.ai.makePlay(self.gameState)
        self.treeGraph.drawTreeNode(self.ai.gameTree)
        self.treeGraph.graph.render("tree", view=False)

class DecisionTreeGraph(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.graph = graphviz.Digraph('G', filename='hello.gv')
        
        self.graph.attr('node', shape='box', style='filled', color='lightgrey')

        self.graph.format = "png"
        self.graph.render("tree", view=False)
    
    def spaceToTab(self, board):
        
        result = board.copy()    
        for i in range(9):
            if result[i] == " ":
                result[i] = "   "
        return result
        
    def drawTreeNode(self, curNode):
        
        current_board = self.spaceToTab(curNode.gameBoard.gameBoard)
             
        for child in curNode.children:
            
            child_board = self.spaceToTab(child.gameBoard.gameBoard)
            self.graph.edge("""
{} || {} || {}
=========
{} || {} || {}
=========
{} || {} || {}
            """.format(*current_board), """
{} || {} || {}
=========
{} || {} || {}
=========
{} || {} || {}
            """.format(*child_board)) 
            
    

        
    