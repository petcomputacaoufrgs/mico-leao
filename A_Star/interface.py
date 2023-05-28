import PySimpleGUI as sg
from algorithm import Algorithm as alg

def size() -> tuple():
    sizeWindow = sg.Window('A Star', 
                        [[sg.Slider(range=(0, 32), key='Sizex', orientation='horizontal', default_value=5, resolution=1, size=(10, 20)),
                        sg.Slider(range=(0, 20), key='Sizey', orientation='horizontal', default_value=5, resolution=1, size=(10, 20))],
                        [sg.Button('Ok', button_color=('white', 'black'), key='Ok'), sg.Button('Load', button_color=('white', 'black'), key='Load')]], # create window
                        #  size=(600, 100), # set window size
                        resizable=True,
                        grab_anywhere=False,
                        element_justification='center') # set element justification to center
    while True:
        event, values = sizeWindow.read()
        if event == sg.WIN_CLOSED:
            exit()
        if event == 'Ok':
            sizex: int = int(values['Sizex'])
            sizey: int = int(values['Sizey'])
            sizeWindow.close()
            return (sizex, sizey, None)
        if event == 'Load':
            sizeWindow.close()
            return (-1, -1, sg.popup_get_file("Load", file_types=(("A Star", "*.astr"),)))
        

class interface:
    def __init__(self, height: int, width: int, colors: list, path: str):
        if path is not None:
            self.loaded = self.load(path)
        else:
            self.loaded = False
            self.height = height
            self.width = width
            self.maze = [[0 for i in range(width)] for j in range(height)] # create maze with 0's
            self.start = (-1, -1) # start position
            self.end = (-1, -1) # end position
            
        self.colors = colors
        self.time: float = 0.1 # time between each step
        buttons:list = [[sg.Button('', key= (i, j), button_color=self.colors[self.maze[j][i]]) for i in range(self.width)] for j in range(self.height)] # create list of lists of buttons
        buttons.append([
            sg.Button('Exit', button_color=('white', 'black'), key='Exit'),
            sg.Button('Run', button_color=('white', 'black'), key='Run'),
            sg.Button('Clear', button_color=('white', 'black'), key='Clear'),
            sg.Button('Save', button_color=('white', 'black'), key='Save'),
            sg.Button('Path', button_color=(self.colors[0]), key='Path'),
            sg.Button('Wall', button_color=(self.colors[1]), key='Wall'),
            sg.Button('Start', button_color=(self.colors[2]), key='Start'),
            sg.Button('End', button_color=(self.colors[3]), key='End'),
            sg.Slider(range=(0, 1), key='Time', orientation='horizontal', default_value=0.1, resolution=0.01, size=(10, 20))
            ]) # add options button

        self.window = sg.Window('A Star', buttons, # create window
                        default_button_element_size=(5, 2), # set button size
                        auto_size_buttons=False, # set auto size to false
                        resizable=True,
                        grab_anywhere=False,
                        element_justification='center') # set element justification to center
        self.window.finalize() # finalize window
    
    def save(self, name: str) -> bool:
        place = name.rfind(".")
        name = name + ".astr" if place == -1 else name[:place] + ".astr"
        try:
            with open(name, "wb") as file:
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

        match option:
            case "Wall":
                if self.end == (x, y):
                    self.end = (-1, -1) # set end to "null"
                if self.start == (x, y):
                    self.start = (-1, -1) # set start to "null"
                self.maze[y][x] = 1 # set to wall

            case "Start":
                if self.end == (x, y):
                    self.end = (-1, -1) # set end to "null"
                if self.start != (-1, -1): # if start is not "null"
                    self.window[self.start].update(button_color = self.colors[0]) # update button color
                    self.maze[self.start[1]][self.start[0]] = 0 # set to 0
                self.start = (x, y) # set start to current position
                self.maze[y][x] = 2 # set to start

            case "End":
                if self.start == (x, y):
                    self.start = (-1, -1) # set start to "null"
                if self.end != (-1, -1): # if end is not "null"
                    self.window[self.end].update(button_color = self.colors[0]) # update button color
                    self.maze[self.end[1]][self.end[0]] = 0 # set to 0
                self.end = (x, y) # set end to current position
                self.maze[y][x] = 3 # set to end

            case "Path":
                if self.end == (x, y):
                    self.end = (-1, -1) # set end to "null"
                if self.start == (x, y):
                    self.start = (-1, -1) # set start to "null"
                self.maze[y][x] = 0 # set to 0

        return
    
    def map_creator(self) -> tuple or None:
        if not self.loaded:
            self.clear()
        option = 'Path'

        while True:
            event, values = self.window.read()  # read the form
            if event in (sg.WIN_CLOSED, 'Exit'):  # if the X button clicked, just exit
                self.window.close() # close window
                exit()
            if type(event) is tuple:
                self.update_maze(event, option) # update maze
                self.window[event].update(button_color = self.colors[self.maze[event[1]][event[0]]]) # update button color
            if event == 'Run':
                self.maze[self.start[1]][self.start[0]] = 0 # set start and end to 0
                self.maze[self.end[1]][self.end[0]] = 0 # set start and end to 0
                self.time = values["Time"] # set time to value
                return self.maze, self.start, self.end # return maze, start and end
            if event == 'Clear':
                self.maze = [[0 for i in range(self.width)] for j in range(self.height)]
                self.start = (-1, -1)
                self.end = (-1, -1)
                for i in range(self.height):
                    for j in range(self.width):
                        self.window[(j, i)].update(button_color = self.colors[self.maze[i][j]])
            if event == 'Save':
                name = sg.popup_get_file('Save', save_as=True, file_types=(("Astar files", "*.astr"),))
                if name != None:
                    self.save(name)
            if event in ['Path', 'Wall', 'Start', 'End']:
                option = event
            
    def map_viewer(self, maze, start: tuple, end: tuple) -> None:
        path = None
        for node in alg.astar(maze, start, end): # run algorithm
            if node == None:
                break
            if node[1] == end:
                path = node
                break

            if node[0] != start and node[0] != end:
                self.window[node[0]].update(button_color = self.colors[5 if node[1] == "closed" else 6]) # update button color

            if self.time != 0.0:
                while True:
                    event, values = self.window.read(timeout= 1000 * self.time)  # read the form
                    if event in (sg.WIN_CLOSED, 'Exit'):  # if the X button clicked, just exit
                        self.window.close() # close window
                        exit()
                    if event == sg.TIMEOUT_KEY: # if 1 second has passed
                        break    
            
        if path == None:
            sg.popup_auto_close("No path found", auto_close_duration=2, title="Error") # show popup
        else:
            if self.time != 0.0:
                while True:
                    event, values = self.window.read(timeout= 1000 * self.time)  # read the form
                    if event in (sg.WIN_CLOSED, 'Exit'):  # if the X button clicked, just exit
                        self.window.close() # close window
                        exit()
                    if event is sg.TIMEOUT_KEY: # if 1 second has passed
                        break  

            for node in alg.path(path[0], path[1]):
                if node == start or node == end:
                    continue
                self.window[node].update(button_color = self.colors[4])
        
        while True:
            event, values = self.window.read()  # read the form
            if event in (sg.WIN_CLOSED, 'Exit'):  # if the X button clicked, just exit
                self.window.close() # close window
                exit()
    
    def clear(self):
        self.maze = [[0 for i in range(self.width)] for j in range(self.height)]
        self.start = (-1, -1)
        self.end = (-1, -1)
        for i in range(self.height):
            for j in range(self.width):
                self.window[(j, i)].update(button_color = self.colors[self.maze[i][j]])

if __name__ == '__main__':
    print("This is a module, not a script")
