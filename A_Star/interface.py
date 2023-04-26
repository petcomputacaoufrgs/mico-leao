import PySimpleGUI as sg

def main_window():
    buttons:list = []
    for i in range(0, 20):
        temp:list = []
        for j in range(0, 32):
            temp.append(sg.Button(''))
        buttons.append(temp)

    layout = buttons

    window = sg.Window('Map', layout,
                    default_button_element_size=(5, 2),
                    auto_size_buttons=False,
                    resizable=True,
                    grab_anywhere=False)
    while True:
        event, values = window.read()  # read the form
        if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
            break

        window[event].update(button_color = 'red' if window[event].ButtonColor[1] == '#283b5b' else '#283b5b')

    window.close()

if __name__ == '__main__':
    main_window()
