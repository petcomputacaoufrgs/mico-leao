import faces_train as ft # treinamento
import video_face_detect as vfd # camera que detecta e reconhece


# só colocando no prompt, depois fazer a interface bonitinha
while True:

    opcao = input('Digite a opção desejada:\n'
                '1 - Camera\n'
                '2 - Treinar modelo\n'
                '3 - Salvar pessoa\n'
                '4 - Sair\n')

    if opcao == '1':
        print('camera selecionada')
        vfd.video_face_detect()
        

    elif opcao == '2':
        print('Iniciando treinamento, aguarde...')
        ft.create_train()
        

    elif opcao == '3':
        print("FAZER OPCAO DE SALVAR PESSOA")
    
    elif opcao == '4':
        break
    
    else:
        print("Opção inválida")
        

