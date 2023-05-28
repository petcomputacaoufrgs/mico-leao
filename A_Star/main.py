import PySimpleGUI as sg
from interface import interface, size

if __name__ == '__main__':
    sizex, sizey, path = size()
    if sizex == -1 and path is None:
        exit()

    while True:
        UI = interface(sizey, sizex, ['grey', 'black', "green", "blue", "yellow", "#283b5b", "red"], path)
        maze, start, end = UI.map_creator()
        UI.map_viewer(maze, start, end)
        UI.close()