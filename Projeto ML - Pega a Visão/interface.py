import PySimpleGUI as sg
import FaceMeshRecognition as vfr
import saves_face_mesh as sf

# Python 3.8.10
# criar ambiente virtual: python -m venv venv
# ativar ambiente ./venv/Scripts/Activate.ps1
# Se não ativar executa powershell como administrador e digita: "Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned" , e dá um S
# pip install PySimpleGUI
# pip install cmake 
# pip install dlib
# pip install face-recognition
# pip install opencv-python
# pip install mediapipe
     
sg.theme('Black')

recognizing_button = sg.Button('Reconhecer / Parar', size=(10, 1), font='Helvetica 14')
save_person_button = sg.Button('Salvar Pessoa', size=(10, 1), font='Helvetica 14')
#add_image_button = sg.Button('Adicionar Imagens', size=(10, 1), font='Helvetica 14')
exit_button = sg.Button('Exit', size=(10, 1), font='Helvetica 14')

    # define the window layout
layout = [
        [sg.Text('Reconhecimento Facial', size=(40, 1), justification='center', font='Helvetica 20')],
        [recognizing_button],
        [save_person_button],
       # [add_image_button],
        [exit_button]
        ]        

window = sg.Window('Reconhecimento Facial', layout, location=(800, 400))

people_encoding = vfr.people_known()

while True:
        event, values = window.read()
        

        if event == 'Exit' or event == sg.WIN_CLOSED:   # Fechar o código
            # cap.release()
            # return
            break

        elif event == 'Reconhecer / Parar':
                    
            vfr.people_unknown_video(people_encoding)

        elif event == 'Salvar Pessoa':
            # Criar pop-up, pedindo nome da pessoa
            name = sg.popup_get_text('Digite um nome', title="Salvar Nova Pessoa")
            if name is not None:
                sg.popup("Como Usar:\n's' para salvar frames;\n'd' para fechar janela;")
                pasta = sf.saves_names(name)
                sf.saves_face(pasta)
