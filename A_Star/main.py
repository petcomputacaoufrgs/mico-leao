from interface import interface
from algorithm import Algorithm

if __name__ == '__main__':
    x = True
    while x:
        UI = interface(5, 5,['#283b5b', 'red', "green", "blue", "yellow"])
        ret = UI.map_creator()
        if(ret == None):
            exit()
        maze, start, end = ret
        path = Algorithm.astar(maze, start, end)
        print(path)
        x = UI.map_viewer(path)