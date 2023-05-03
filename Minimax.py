# Description: This program is a Tic Tac Toe game that uses the Minimax algorithm to play against the user.
import PySimpleGUI as sg
from Stuff import *
sg.theme('DarkAmber') 
width = 15
layout = [  [sg.Text('Welcome to Tic Tac Toe. '), sg.Text("Press in your play: ")],
            [sg.Button(" ",size=(width,width),key="0"), sg.Button(" ",size=(width,width),key="1"), sg.Button(" ",size=(width,width),key="2")],
            [sg.Button(" ",size=(width,width),key="3"), sg.Button(" ",size=(width,width),key="4"), sg.Button(" ",size=(width,width),key="5")],
            [sg.Button(" ",size=(width,width),key="6"), sg.Button(" ",size=(width,width),key="7"), sg.Button(" ",size=(width,width),key="8")]]

def main():
    window = sg.Window("Tic Tac Toe", layout)
    actualBoard = Game()
    while True:
        
        event,values = window.read()
       
        if sg.WINDOW_CLOSED == event:
            exit()
        
        play = int(event[0])
        if actualBoard.IsValid(int(play)):
            actualBoard.Assing(int(play))
            
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
                caller = 0
                for cells in actualBoard.gameBoard:
                    window[str(caller)].update(cells)
                    caller+=1
                    
            else:
                if AfterGame(actualBoard, window) == False:
                    exit()
        else:
            sg.popup("Invalid Play")
            
  
if __name__ == "__main__":
    main()
