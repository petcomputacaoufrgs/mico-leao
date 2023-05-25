'''
Controla estado do jogo
'''
class Board:
    PLAYER_WINS = 1
    AI_WINS = 1
    TIE = 1
    PLAYER1 = 1
    PLAYER1_SYMBOL = 'X'
    PLAYER2 = 2
    PLAYER2_SYMBOL = 'O'

    def __init__(self):
        self.gameBoard = list(" "*9)
    
    def copy(self):
        copyBoard = Board()
        copyBoard.gameBoard = self.gameBoard.copy()
        return copyBoard

    def __eq__(self, __value: object) -> bool:
        return self.gameBoard == __value.gameBoard
    
    def registerMove(self, position, player):
        if player == Board.PLAYER1:
            self.gameBoard[int(position)] = 'X'
        else:
            self.gameBoard[int(position)] = 'O'
    
    def __repr__(self):
        for i in range(3):
            print(f"|{self.gameBoard[i*3]}|{self.gameBoard[(i*3)+1]}|{self.gameBoard[(i*3)+2]}|")
         
    def evaluateBoard(self):
        
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
         
    def isValidMove(self,position):
        if position < 0 or position > 8:
            return False
        if self.gameBoard[int(position)] == " ":
            return True
        else:
            return False
    
    def clear(self):
        self.gameBoard = list(" "*9)

    # Retorna jogador oponente
    @staticmethod
    def getOpponent(player):
        if player == Board.PLAYER1:
            return Board.PLAYER2
        else:
            return Board.PLAYER1

'''
Jogador IA, que gera a árvore de jogadas uma única vez e atualiza
a raiz desta baseado no estado atual, escolhendo a próxima jogada a partir
dos melhores filhos
'''
class AIPlayer:

    def __init__(self, player) -> None:
        self.gameTree = None
        self.player = player
        self.cur_depth = 0 if player == Board.PLAYER1 else 1

    # Gera árvore minimax a partir de tabuleiro
    def generateGameTree(self, initialBoard : Board):
        self.gameTree = MinimaxNode(initialBoard, self.player)
        self.gameTree.minimax(True, self.cur_depth)

    # Atualiza a raiz da árvores
    def updateTreeRoot(self, newBoard):
        for child in self.gameTree.children:
            if child.gameBoard == newBoard:
                self.gameTree = child
                break

    # Faz jogada e retorna tabuleiro
    def makePlay(self, board : Board):
        if self.gameTree is None:
            self.generateGameTree(board)
        
        best_move = None
        best_value = -1000
        for child in self.gameTree.children:
            if child.score > best_value:
                best_move = child
                best_value = child.score
        
        if best_move is not None:
            self.updateTreeRoot(best_move.gameBoard)
        
        return self.gameTree.gameBoard


class MinimaxNode:
    def __init__(self, gameBoard : Board, player) -> None:
        self.gameBoard = gameBoard
        self.score = None
        self.children = []
        self.player = player

    # Gera jogadas possíveis
    def generateChildren(self):
        for p in range(9):
            if self.gameBoard.isValidMove(p):
                newBoard = self.gameBoard.copy()
                newBoard.registerMove(p, self.player)
                newNode = MinimaxNode(newBoard, Board.getOpponent(self.player))
                self.children.append(newNode)

    # Gera árvore minimax a partir deste nodo e obtém o valor da raiz
    def minimax(self, isMax, depth=0, maxDepth=9):
        self.score = self.gameBoard.evaluateBoard()
        
        if self.score is not None:
            return self.score

        if depth == maxDepth:
            return self.score

        self.generateChildren()
  
        if isMax:
            best_value = -1000

            for child in self.children:
                new_value = child.minimax(not isMax, depth+1, maxDepth)
                 
                if new_value > best_value:
                    best_value = new_value

        else:
            best_value = 1000

            for child in self.children:
                new_value = child.minimax(not isMax, depth+1, maxDepth)
                if new_value < best_value:
                    best_value = new_value

        self.score = best_value
        return best_value


