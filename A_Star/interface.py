import PySimpleGUI as sg

class interface:
    def __init__(self, height: int, width: int, colors: list):
        self.height = height
        self.width = width
        self.colors = colors
        self.maze = [[0 for i in range(width)] for j in range(height)] # create maze with 0's
        self.start = (-1, -1) # start position
        self.end = (-1, -1) # end position
    
    def update_maze(self, event: tuple, window: sg.Window, option: str) -> None:
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
                    window[self.start].update(button_color = self.colors[0]) # update button color
                    self.maze[self.start[1]][self.start[0]] = 0 # set to 0
                self.start = (x, y) # set start to current position
                self.maze[y][x] = 2 # set to start

            case "End":
                if self.start == (x, y):
                    self.start = (-1, -1) # set start to "null"
                if self.end != (-1, -1): # if end is not "null"
                    window[self.end].update(button_color = self.colors[0]) # update button color
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
        buttons:list = [[sg.Button('', key= (i, j)) for i in range(self.width)] for j in range(self.height)] # create list of lists of buttons
        buttons.append([
            sg.Button('Exit', button_color=('white', 'black'), key='Exit'),
            sg.Button('Run', button_color=('white', 'black'), key='Run'),
            sg.Button('Clear', button_color=('white', 'black'), key='Clear'),
            sg.Button('Path', button_color=(self.colors[0]), key='Path'),
            sg.Button('Wall', button_color=(self.colors[1]), key='Wall'),
            sg.Button('Start', button_color=(self.colors[2]), key='Start'),
            sg.Button('End', button_color=(self.colors[3]), key='End')
            ]) # add options button

        window = sg.Window('Map', buttons, # create window
                        default_button_element_size=(5, 2), # set button size
                        auto_size_buttons=False, # set auto size to false
                        resizable=True,
                        grab_anywhere=False,
                        element_justification='center') # set element justification to center
        
        option = 'Path'

        while True:
            event, values = window.read()  # read the form
            if event in (sg.WIN_CLOSED, 'Exit'):  # if the X button clicked, just exit
                window.close() # close window
                return None # return None
            if type(event) is tuple:
                self.update_maze(event, window, option) # update maze
                window[event].update(button_color = self.colors[self.maze[event[1]][event[0]]]) # update button color
            if event == 'Run':
                self.maze[self.start[1]][self.start[0]] = 0 # set start and end to 0
                self.maze[self.end[1]][self.end[0]] = 0 # set start and end to 0
                window.close() # close window
                return self.maze, self.start, self.end # return maze, start and end
            if event == 'Clear':
                self.maze = [[0 for i in range(self.width)] for j in range(self.height)]
                self.start = (-1, -1)
                self.end = (-1, -1)
                for i in range(self.height):
                    for j in range(self.width):
                        window[(j, i)].update(button_color = self.colors[self.maze[i][j]])
            if event in ['Path', 'Wall', 'Start', 'End']:
                option = event
            
    def color_maze(self, curr_node: tuple, path: list(tuple())) -> str:
        ret = self.colors[0]
        if curr_node == self.start:
            ret = self.colors[2]
        elif curr_node == self.end:
            ret = self.colors[3]
        elif curr_node in path:
            ret = self.colors[4]
        elif self.maze[curr_node[1]][curr_node[0]] == 1:
            ret = self.colors[1]
        return ret
            
    def map_viewer(self, path: list(tuple())) -> bool:
        path = [(i[1], i[0]) for i in path] # reverse path
        buttons:list = [[sg.Button('', key=(i, j), button_color=self.color_maze((i, j), path)) for i in range(self.width)] for j in range(self.height)] # create list of lists of buttons
        buttons.append([
            sg.Button('New', button_color=('white', 'black'), key='New'),
            sg.Button('Exit', button_color=('white', 'black'), key='Exit')]) # add exit button

        window = sg.Window('Map', buttons, # create window
                        default_button_element_size=(5, 2), # set button size
                        auto_size_buttons=False, # set auto size to false
                        resizable=True,
                        grab_anywhere=False,
                        element_justification='center') # set element justification to center
        
        ext = False
        while True:
            event, values = window.read()  # read the form
            if event in (sg.WIN_CLOSED, 'Exit'):  # if the X button clicked, just exit
                break
            if event == 'New':
                ext = True
                break 

        window.close() # close window
        return ext

if __name__ == '__main__':
    print("This is a module, not a script")
