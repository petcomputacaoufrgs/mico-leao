from interface import interface
from algorithm import Algorithm

if __name__ == '__main__':
    while True:
        UI = interface(5, 5, ['#283b5b', 'red', "green", "blue", "yellow"])
        maze, start, end = UI.map_creator()
        path = Algorithm.astar(maze, start, end)
        UI.map_viewer(path)