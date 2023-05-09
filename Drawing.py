import PySimpleGUI as telinha
from Processing import *
widthBUTTON = 30
heightBUTTON = 15

def AfterGame(board, window):
    if telinha.PopupYesNo(TurnToString(board.Value()),title="Game Over") == "Yes":
        board.Reset()
        for i in range (9):
            window[f"{i}"].update(" ")
        return True
    else:
        return False

def DrawGame(game):
    layoutSTART = [[telinha.Text('Welcome to Tic Tac Toe. '), telinha.Text("Press in your play: ")],
            [telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="0"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="1"), telinha.Button(" ",size=(widthBUTTON ,heightBUTTON),key="2")],
            [telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="3"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="4"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON ),key="5")],
            [telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="6"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON),key="7"), telinha.Button(" ",size=(widthBUTTON,heightBUTTON ),key="8")]]

    StartWindow = telinha.Window("Tic Tac Toe", layoutSTART,margins=(70,100))
    boardState = list(" ")*9


    child_layout = [[telinha.Text("child",key="text")]]
    child_window = telinha.Window("child display", child_layout, location=(40,40))
    

    while True:
        event, value = StartWindow.read() 
        eventchild,valuechild = child_window.read(timeout=0)
        child_window["text"].update("""{} | {} | {}
         ---+---+---
          {} | {} | {}
         ---+---+---
          {} | {} | {}""".format(*boardState))
        if event in (telinha.WIN_CLOSED, 'Sair'):
            exit()
    
        gameNode, endFlag = Step(boardState,event)
        boardState = gameNode.gameBoard
        for itens in range(9):
            StartWindow[str(itens)].update(boardState[itens])
        gameStatus = Game()
        gameStatus.gameBoard = boardState
        if endFlag != 0:
            if AfterGame(gameStatus, StartWindow) == True:
                boardState = gameStatus.gameBoard
            else:
                exit()
              
def StartGame():
    layout = [
            [telinha.Text(text='PET Computação',
                   font=('Arial Bold', 25),
                   size=20,
                   expand_x=True,
                   justification='center')],
            [telinha.Text(text='Jogo da Velha\n',
                   font=('Arial Bold', 18),
                   size=20,
                   expand_x=True,
                   justification='center')],
            [telinha.Button('Começar', size=(15,1)), telinha.Exit('Sair', size=(15,1))],
            [telinha.Text(text='Vitórias: 0',
                   font=('Arial Bold', 10),
                   size=15,
                   expand_x=True,
                   justification='center',
                   key='v'),
            telinha.Text(text='Empates: 0',
                   font=('Arial Bold', 10),
                   size=15,
                   expand_x=True,
                   justification='center',
                   key='e'),
            telinha.Text(text='Derrotas: 0',
                   font=('Arial Bold', 10),
                   size=15,
                   expand_x=True,
                   justification='center',
                   key='d'),
            ]
            ]
    
    window = telinha.Window('PET Computação', layout, element_justification='c', margins=(70,140))

    while True:
        event, values = window.read()
        if event in (telinha.WIN_CLOSED, 'Sair'):
            exit()
        elif event == 'Começar':
            window.close()
            DrawGame(Game())
            break 
            