import PySimpleGUI as sg
import os
from os import walk, listdir
from math import floor, ceil
from images import PETLOGO, NOPATH
from algorithm import Algorithm as alg

def load(name: str) -> tuple[int, int, int, tuple[int, int], tuple[int, int], list[list[int]]] or None:
        place = name.rfind(".")
        name = name + ".astr" if place == -1 else name[:place] + ".astr"
        try:
            with open(name, "rb") as file:
                diagonal = bool.from_bytes(file.read(1), "big")
                height = int.from_bytes(file.read(2), "big")
                width = int.from_bytes(file.read(2), "big")
                start = (int.from_bytes(file.read(2), "big"), int.from_bytes(file.read(2), "big"))
                end = (int.from_bytes(file.read(2), "big"), int.from_bytes(file.read(2), "big"))
                maze = [[int.from_bytes(file.read(1), "big") for i in range(width)] for j in range(height)]
            return (diagonal, height, width, start, end, maze)
        except:
            sg.popup_error("Error loading file")
            return None
        
def wait(window: sg.Window, time: float) -> None:
    while True:
        event, values = window.read(timeout= 1000 * time, )  # read the form
        if event in [sg.WIN_CLOSED, "Escape:27"]:
            window.close() # close window
            exit()
        if event in [sg.TIMEOUT_KEY, "_Enter"]: # if 1 second has passed
            return
            
def createWindow(colors: list) -> sg.Window:
    SUBSAMPLE = 10
    IMGSIZE = (100, 100)
    buttons:list = [
                    [sg.Image(PETLOGO, size=IMGSIZE, subsample=SUBSAMPLE), sg.Text(text="Titulo", font=("helvetica", 30), expand_x=True, justification='center', key='Title', size=(20,2),), sg.Image(PETLOGO, size=IMGSIZE, subsample=SUBSAMPLE)],
                    [sg.Push(), sg.Text("Venha fazer seu proprio Labirinto!!", font=("consolas", 30, 'bold'), text_color='red'), sg.Push()],
                    [[sg.Button('', key= (i, j), button_color=colors[0]) for i in range(TOTALWIDTH)] for j in range(TOTALHEIGHT)],
                    [sg.Button(f'Diagonal', button_color=colors[2], key='Diagonal', size=(10, 4), font=("helvetica", 20))]] # create list of lists of buttons

    return sg.Window('A Star', buttons, # create window
                        default_button_element_size=(5, 2), # set button size
                        auto_size_buttons=False, # set auto size to false
                        grab_anywhere=False,
                        size=(1920, 1080),
                        location=(0, 0),
                        keep_on_top=True,
                        return_keyboard_events=True,
                        no_titlebar=True,
                        element_justification='center',
                        finalize=True) # set element justification to center

def clearScreen(window: sg.Window, height: int, width: int) -> None:
    for i in range(height):
        for j in range(width):
            window[(j, i)].update(button_color='#64778d')
            
def splash():
    sg.popup_no_buttons(title="Sem Caminho", image=NOPATH, non_blocking=True, no_titlebar=True, auto_close=True, auto_close_duration=4)

if __name__ == '__main__': 

    PATH = "C:/Users/kersz/Documents/ufrgs/PET/mico-leao/maps"
    TOTALHEIGHT = 18
    TOTALWIDTH = 32
    colors = ['grey', 'black', "green", "blue", "yellow", "#283b5b", "red"]
    window = createWindow(colors)
    window.bind("<Return>", "_Enter")
    
    while True:
        # window.maximize()
        wait(window, 0.1)
        os.chdir(PATH)
        files = filter(os.path.isfile, listdir(PATH))
        files = [os.path.join(PATH, f) for f in files] # add path to each file
        
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        for file in files:
            
            if not file.endswith(".astr"):
                continue
            
            clearScreen(window, TOTALHEIGHT, TOTALWIDTH)
            
            diagonal, height, width, start, end, maze = load(file)
            if diagonal is None or start == (-1, -1) or end == (-1, -1):
                continue
            
            time = 0.3
            window['Diagonal'].update(button_color='green' if diagonal else 'red')
            window['Title'].update(value="Labirinto de " + file[len(PATH) + 1:-5])
            
            for i, posY in enumerate(range(int(TOTALHEIGHT/2 - floor(height/2)) - 1, int(TOTALHEIGHT/2 + ceil(height/2)) - 1)) if height < TOTALHEIGHT else enumerate(range(TOTALHEIGHT)):
                for j, posX in enumerate(range(int(TOTALWIDTH/2 - floor(width/2)) - 1 , int(TOTALWIDTH/2 + ceil(width/2) - 1))) if width < TOTALWIDTH else enumerate(range(TOTALWIDTH)):
                    if posX < 0 or posY < 0:
                        continue
                    window[(posX, posY)].update(button_color=colors[maze[i][j]])
            
            path = None
            
            for node in alg.astar(maze, start, end, diagonal): # run algorithm
                if node == None:
                    break
                if node[1] == end:
                    path = node
                    break

                if node[0] != start and node[0] != end:
                    x, y = node[0]
                    newX = int(TOTALWIDTH/2 - floor(width/2)) + x - 1 if width < TOTALWIDTH else x
                    newY = int(TOTALHEIGHT/2 - floor(height/2)) + y - 1 if height < TOTALHEIGHT else y
                    window[(newX , newY)].update(button_color = colors[5 if node[1] == "closed" else 6]) # update button color
                if node[1] == "closed":
                    wait(window, time)   
                    
            if path == None:
                splash()
                # sg.popup_auto_close("No path found", auto_close_duration=2, title="Error") # show popup
            else:
                wait(window, 0.5)

                for node in alg.path(path[0], path[1]):
                    if node == start or node == end:
                        continue
                    x, y = node
                    newX = int(TOTALWIDTH/2 - floor(width/2)) + x - 1 if width < TOTALWIDTH else x
                    newY = int(TOTALHEIGHT/2 - floor(height/2)) + y - 1 if height < TOTALHEIGHT else y
                    window[(newX, newY)].update(button_color = colors[4])
            
            wait(window, 5)
            