import PySimpleGUI as sg
from interface import interface, size

if __name__ == '__main__':
    sizex, sizey = size()

    while True:
        UI = interface(sizey, sizex, ['grey', 'black', "green", "blue", "yellow", "#283b5b", "red"])
        maze, start, end = UI.map_creator()
        UI.map_viewer(maze, start, end)
        UI.close()