INITIALPATH = ""
TOTALHEIGHT = 18
TOTALWIDTH = 27

import PySimpleGUI as sg
from algorithm import Algorithm as alg
from images import PETLOGO, NOPATH
from math import ceil, floor


class interface:
    def __init__(self, colors: list):

        self.height = 5
        self.width = 5
        self.maze = [[0 for _ in range(5)] for _ in range(5)] # create maze with 0's
        self.start = (-1, -1) # start position
        self.end = (-1, -1) # end position
        self.diagonal = True
            
        SUBSAMPLE = 10
        IMGSIZE = (100, 100)
        self.colors = colors
        self.time: float = 0.1 # time between each step
        buttons:list = [
                    [sg.Image(PETLOGO, size=IMGSIZE, subsample=SUBSAMPLE), sg.Text(text="Titulo", font=("helvetica", 30), expand_x=True, justification='center', key='Title', size=(20,2),), sg.Image(PETLOGO, size=IMGSIZE, subsample=SUBSAMPLE)],
                    [sg.Push(), sg.Text("Faça seu proprio Labirinto para o Display!!", font=("consolas", 30, 'bold'), text_color='red'), sg.Push()],
                    [[sg.Button('', key= (i, j), button_color=colors[0]) for i in range(TOTALWIDTH)] for j in range(TOTALHEIGHT)],
                    [sg.Button('Run', button_color=('white', 'black'), key='Run', size=(5, 2)),
                    sg.Button('Clear', button_color=('white', 'black'), key='Clear', size=(5, 2)),
                    sg.Button('Save', button_color=('white', 'black'), key='Save', size=(5, 2)),
                    sg.Button('Load', button_color=('white', 'black'), key='Load', size=(5, 2)),
                    sg.Button('Path', button_color=(self.colors[0]), key='Path', size=(5, 2)),
                    sg.Button('Wall', button_color=(self.colors[1]), key='Wall', size=(5, 2)),
                    sg.Button('Start', button_color=(self.colors[2]), key='Start', size=(5, 2)),
                    sg.Button('End', button_color=(self.colors[3]), key='End', size=(5, 2)),
                    sg.Text('Tempo', font=('Helvetica', 15), size=(5, 1), justification='center'),
                    sg.Slider(range=(0, 1), key='Time', change_submits=True, orientation='horizontal', default_value=0.1, resolution=0.01, size=(10, 20)),
                    sg.Text('X', font=('Helvetica', 15), size=(5, 1), justification='center'),
                    sg.Slider(range=(1, TOTALWIDTH), key='X', change_submits=True, orientation='horizontal', default_value=5, resolution=1, size=(10, 20)),
                    sg.Text('Y', font=('Helvetica', 15), size=(5, 1), justification='center'),
                    sg.Slider(range=(1, TOTALHEIGHT), key='Y', change_submits=True, orientation='horizontal', default_value=5, resolution=1, size=(10, 20)),
                    sg.Button(f'Diagonal', button_color=self.colors[2 if self.diagonal else 6], key='Diagonal', size=(6, 2)) # add options button
                    ]] # add options button

        self.window = sg.Window('A Star', buttons, # create window
                        default_button_element_size=(5, 2), # set button size
                        auto_size_buttons=False, # set auto size to false
                        grab_anywhere=False,
                        size=(1920, 1080),
                        location=(0, 0),
                        keep_on_top=True,
                        return_keyboard_events=True,
                        no_titlebar=True,
                        element_justification='center', finalize=True) # set element justification to center
        self.window.bind("<Return>", "_Enter")
    
    def clearScreen(self) -> None:
        for i in range(TOTALHEIGHT):
            for j in range(TOTALWIDTH):
                self.window[(j, i)].update(button_color='#64778d')
                
    def wait(self, time: float) -> None:
        while True:
            event, values = self.window.read(timeout= 1000 * time)  # read the form
            if event in [sg.WIN_CLOSED, "Escape:27"]:
                self.window.close() # close window
                exit()
            if event in [sg.TIMEOUT_KEY, "_Enter"]: # if 1 second has passed
                return 
            if event == "Clear":
                self.clear()
                return
            if event == 'Save':
                name = sg.popup_get_file('Save', save_as=True, file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                if name != None:
                    self.maze[self.start[1]][self.start[0]] = 2 # set to 0
                    self.maze[self.end[1]][self.end[0]] = 3 # set to 0
                    self.save(name)
            if event == "Load":
                name = sg.popup_get_file("Load", file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                if name != None:
                    self.load(name)
                    return
    
    def Error():
        sg.popup_no_buttons(title="Sem Caminho", image=NOPATH, non_blocking=True, keep_on_top=True, no_titlebar=True, auto_close=True, auto_close_duration=4)
    
    def save(self, name: str) -> bool:
        place = name.rfind(".")
        name = name + ".astr" if place == -1 else name[:place] + ".astr"
        try:
            with open(name, "wb") as file:
                file.write(self.diagonal.to_bytes(1, "big"))
                file.write(self.height.to_bytes(2, "big"))
                file.write(self.width.to_bytes(2, "big"))
                file.write(self.start[0].to_bytes(2, "big"))
                file.write(self.start[1].to_bytes(2, "big"))
                file.write(self.end[0].to_bytes(2, "big"))
                file.write(self.end[1].to_bytes(2, "big"))                
                for i in range(self.height):
                    for j in range(self.width):
                        file.write(self.maze[i][j].to_bytes(1, "big"))
            return True
        except:
            sg.popup_error("Error saving file")
            return False
    
    def load(self, name: str) -> bool:
        place = name.rfind(".")
        name = name + ".astr" if place == -1 else name[:place] + ".astr"
        try:
            with open(name, "rb") as file:
                self.diagonal = bool.from_bytes(file.read(1), "big")
                self.height = int.from_bytes(file.read(2), "big")
                self.width = int.from_bytes(file.read(2), "big")
                self.start = (int.from_bytes(file.read(2), "big"), int.from_bytes(file.read(2), "big"))
                self.end = (int.from_bytes(file.read(2), "big"), int.from_bytes(file.read(2), "big"))
                self.maze = [[int.from_bytes(file.read(1), "big") for i in range(self.width)] for j in range(self.height)]
            return True
        except:
            sg.popup_error("Error loading file")
            return False
    
    def close(self) -> None:
        self.window.close()
    
    def update_maze(self, event: tuple, option: str) -> None:
        x, y = event[0], event[1]

        if option == "Wall":
            if self.end == (x, y):
                self.end = (-1, -1) # set end to "null"
            if self.start == (x, y):
                self.start = (-1, -1) # set start to "null"
            self.maze[y][x] = 1 # set to wall
        elif option == "Start":
            if self.end == (x, y):
                self.end = (-1, -1) # set end to "null"
            if self.start != (-1, -1): # if start is not "null"
                self.window[self.start].update(button_color = self.colors[0]) # update button color
                self.maze[self.start[1]][self.start[0]] = 0 # set to 0
            self.start = (x, y) # set start to current position
            self.maze[y][x] = 2 # set to start
        elif option == "End":
            if self.start == (x, y):
                self.start = (-1, -1) # set start to "null"
            if self.end != (-1, -1): # if end is not "null"
                self.window[self.end].update(button_color = self.colors[0]) # update button color
                self.maze[self.end[1]][self.end[0]] = 0 # set to 0
            self.end = (x, y) # set end to current position
            self.maze[y][x] = 3 # set to end
        elif option == "Path":
            if self.end == (x, y):
                self.end = (-1, -1) # set end to "null"
            if self.start == (x, y):
                self.start = (-1, -1) # set start to "null"
            self.maze[y][x] = 0 # set to 0
    
    def map_maker(self) -> None:
        option = 'Path'
        rerun = False
        while True:
            jump = False
            if not rerun:
                while True:
                    self.window['Run'].update('Run')
                    self.window['Path'].update(disabled=False)
                    self.window['Wall'].update(disabled=False)
                    self.window['Start'].update(disabled=False)
                    self.window['End'].update(disabled=False)
                    self.window['X'].update(disabled=False)
                    self.window['Y'].update(disabled=False)
                    self.window['Diagonal'].update(disabled=False)
                    self.wait(0.1)
                    self.clearScreen()

                    for i, posY in enumerate(range(int(TOTALHEIGHT/2 - floor(self.height/2)) - 1, int(TOTALHEIGHT/2 + ceil(self.height/2)) - 1)) if self.height < TOTALHEIGHT else enumerate(range(TOTALHEIGHT)):
                        for j, posX in enumerate(range(int(TOTALWIDTH/2 - floor(self.width/2)) - 1 , int(TOTALWIDTH/2 + ceil(self.width/2) - 1))) if self.width < TOTALWIDTH else enumerate(range(TOTALWIDTH)):
                            if posX < 0 or posY < 0:
                                continue
                            self.window[(posX, posY)].update(button_color=self.colors[self.maze[i][j]])
                    
                    event, values = self.window.read()  # read the form
                    if event in [sg.WIN_CLOSED, "Escape:27"]:
                        self.window.close() # close window
                        exit()
                    if type(event) is tuple:
                        x, y = event[0], event[1]
                        newX = x - int(TOTALWIDTH/2 - floor(self.width/2)) + 1 if self.width < TOTALWIDTH else x
                        newY = y - int(TOTALHEIGHT/2 - floor(self.height/2)) + 1 if self.height < TOTALHEIGHT else y
                        self.update_maze((newX, newY), option) # update maze
                        self.window[event].update(button_color = self.colors[self.maze[newY][newX]]) # update button color
                    
                    if event == 'Run':
                        self.maze[self.start[1]][self.start[0]] = 0 # set start and end to 0
                        self.maze[self.end[1]][self.end[0]] = 0 # set start and end to 0
                        self.time = values["Time"] # set time to value
                        break
                    
                    if event == 'Clear':
                        self.maze = [[0 for i in range(self.width)] for j in range(self.height)]
                        self.start = (-1, -1)
                        self.end = (-1, -1)
                        self.clear()  
                    
                    if event == 'Save':
                        name = sg.popup_get_file('Save', save_as=True, file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                        if name != None:
                            self.maze[self.start[1]][self.start[0]] = 2 # set to 0
                            self.maze[self.end[1]][self.end[0]] = 3 # set to 0
                            self.save(name)
                    if event == "Load":
                        name = sg.popup_get_file("Load", file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                        if name != None:
                            self.load(name)
                            jump = True
                            break
                    if event in ['Path', 'Wall', 'Start', 'End']:
                        option = event
                    if event == 'Diagonal':
                        self.diagonal = not self.diagonal
                        self.window[event].update(button_color = self.colors[2 if self.diagonal else 6])
                    if event == 'X':
                        oldwidth = self.width
                        self.width = int(values[event])
                        for i in range(self.height):
                            if i >= TOTALHEIGHT:
                                self.maze.append([0 for i in range(self.width)])
                            elif self.width > oldwidth:
                                self.maze[i].extend([0 for i in range(self.width - oldwidth)])
                            elif self.width < oldwidth:
                                self.maze[i] = self.maze[i][:self.width]
                        
                        for i, posY in enumerate(range(int(TOTALHEIGHT/2 - floor(self.height/2)) - 1, int(TOTALHEIGHT/2 + ceil(self.height/2)) - 1)) if self.height < TOTALHEIGHT else enumerate(range(TOTALHEIGHT)):
                            for j, posX in enumerate(range(int(TOTALWIDTH/2 - floor(self.width/2)) - 1 , int(TOTALWIDTH/2 + ceil(self.width/2) - 1))) if self.width < TOTALWIDTH else enumerate(range(TOTALWIDTH)):
                                if posX < 0 or posY < 0:
                                    continue
                                self.window[(posX, posY)].update(button_color=self.colors[self.maze[i][j]])
                    if event == 'Y':
                        oldHeight = self.height
                        self.height = int(values[event])
                        if self.height > oldHeight:
                            self.maze.extend([[0 for i in range(self.width)] for j in range(self.height - oldHeight)])
                        elif self.height < oldHeight:
                            self.maze = self.maze[:self.height]
                        for i, posY in enumerate(range(int(TOTALHEIGHT/2 - floor(self.height/2)) - 1, int(TOTALHEIGHT/2 + ceil(self.height/2)) - 1)) if self.height < TOTALHEIGHT else enumerate(range(TOTALHEIGHT)):
                            for j, posX in enumerate(range(int(TOTALWIDTH/2 - floor(self.width/2)) - 1 , int(TOTALWIDTH/2 + ceil(self.width/2) - 1))) if self.width < TOTALWIDTH else enumerate(range(TOTALWIDTH)):
                                if posX < 0 or posY < 0:
                                    continue
                                self.window[(posX, posY)].update(button_color=self.colors[self.maze[i][j]])
            
            if jump:
                continue
            
            self.window['Run'].update('Re-Run')
            self.window['Path'].update(disabled=True)
            self.window['Wall'].update(disabled=True)
            self.window['Start'].update(disabled=True)
            self.window['End'].update(disabled=True)
            self.window['X'].update(disabled=True)
            self.window['Y'].update(disabled=True)
            self.window['Diagonal'].update(disabled=True)
            
            path = None
            for node in alg.astar(self.maze, self.start, self.end, self.diagonal): # run algorithm
                if node == None:
                    break
                if node[1] == self.end:
                    path = node
                    break

                if node[0] != self.start and node[0] != self.end:
                    x, y = node[0]
                    newX = int(TOTALWIDTH/2 - floor(self.width/2)) + x - 1 if self.width < TOTALWIDTH else x
                    newY = int(TOTALHEIGHT/2 - floor(self.height/2)) + y - 1 if self.height < TOTALHEIGHT else y
                    self.window[(newX , newY)].update(button_color = self.colors[5 if node[1] == "closed" else 6]) # update button color
                if node[1] == "closed":
                    while True:
                        if self.time == 0.0:
                            break
                        event, values = self.window.read(timeout= 1000 * self.time)  # read the form
                        if event in [sg.WIN_CLOSED, "Escape:27"]:  # if the X button clicked, just exit
                            self.window.close() # close window
                            exit()
                        if event == sg.TIMEOUT_KEY: # if 1 second has passed
                            break   
                        if event == 'Time':
                            self.time = values["Time"]
                        if event == "Clear":
                            self.clear()
                            return
                        if event == 'Save':
                            name = sg.popup_get_file('Save', save_as=True, file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                            if name != None:
                                self.maze[self.start[1]][self.start[0]] = 2 # set to 0
                                self.maze[self.end[1]][self.end[0]] = 3 # set to 0
                                self.save(name)
            rerun = False          
            if path == None:
                self.splash()
                # sg.popup_auto_close("No path found", auto_close_duration=2, title="Error") # show popup
            else:
                self.wait(0.5)

                for node in alg.path(path[0], path[1]):
                    if node == self.start or node == self.end:
                        continue
                    x, y = node
                    newX = int(TOTALWIDTH/2 - floor(self.width/2)) + x - 1 if self.width < TOTALWIDTH else x
                    newY = int(TOTALHEIGHT/2 - floor(self.height/2)) + y - 1 if self.height < TOTALHEIGHT else y
                    self.window[(newX, newY)].update(button_color = self.colors[4])
            
            while True:
                event, values = self.window.read()  # read the form
                if event in [sg.WIN_CLOSED, "Escape:27"]:
                    self.window.close() # close window
                    exit()
                if event == "Clear":
                    self.clear()
                    break
                if event == 'Save':
                    name = sg.popup_get_file('Save', save_as=True, file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                    if name != None:
                        self.maze[self.start[1]][self.start[0]] = 2 # set to 0
                        self.maze[self.end[1]][self.end[0]] = 3 # set to 0
                        self.save(name)
                if event == "Load":
                    name = sg.popup_get_file("Load", file_types=(("Astar files", "*.astr"),), keep_on_top=True, default_path=INITIALPATH, initial_folder=INITIALPATH)
                    if name != None:
                        self.load(name)
                        break
                if event == 'Run':
                    rerun = True   
                    break
    
    def clear(self):
        self.maze = [[0 for i in range(self.width)] for j in range(self.height)]
        self.start = (-1, -1)
        self.end = (-1, -1)
        for i, posY in enumerate(range(int(TOTALHEIGHT/2 - floor(self.height/2)) - 1, int(TOTALHEIGHT/2 + ceil(self.height/2)) - 1)) if self.height < TOTALHEIGHT else enumerate(range(TOTALHEIGHT)):
            for j, posX in enumerate(range(int(TOTALWIDTH/2 - floor(self.width/2)) - 1 , int(TOTALWIDTH/2 + ceil(self.width/2) - 1))) if self.width < TOTALWIDTH else enumerate(range(TOTALWIDTH)):
                if posX < 0 or posY < 0:
                    continue
                self.window[(posX, posY)].update(button_color=self.colors[self.maze[i][j]])

if __name__ == '__main__':
    UI = interface(['grey', 'black', "green", "blue", "yellow", "#283b5b", "red"])
    UI.map_maker()
