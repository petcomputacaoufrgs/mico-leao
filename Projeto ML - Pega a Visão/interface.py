import faces_train as ft # treinamento
import video_face_detect as vfd # camera que detecta e reconhece
import saves_face as sf


# só colocando no prompt, depois fazer a interface bonitinha
while True:

    opcao = input('Digite a opção desejada:\n'
                '1 - Camera\n'
                '2 - Treinar modelo\n'
                '3 - Salvar pessoa\n'
                '4 - Adcionar Imagens\n'
                '5 - Sair\n')

    if opcao == '1':
        print('camera selecionada')
        vfd.video_face_detect()
        

    elif opcao == '2':
        print('Iniciando treinamento, aguarde...')
        ft.create_train()
        
    elif opcao == '3':
        print("salvamento selecionado")
        dest = sf.saves_names()
        sf.saves_face(dest)
    
    elif opcao == '4':
        name = input('Digite o nome da pessoa:')
        dest = r"Faces/train/"+name
        people = ft.open_names()
        if name in people: 
            sf.saves_face(dest)
        else:
            print("Pessoa Não Econtrada.")

    elif opcao == '5':
        break
    
    else:
        print("Opção inválida")
        

