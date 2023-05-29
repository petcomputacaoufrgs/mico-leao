import video_face_recognition as vfr
import saves_face as sf

# dicionário com o encoding das pessoas reconhecidas
people_encoding = vfr.people_known()

# só colocando no prompt, depois fazer a interface bonitinha
while True:

    opcao = input('Digite a opção desejada:\n'
                '1 - Reconhecer\n'
                '2 - Salvar pessoa\n'
                '3 - Sair\n')

    if opcao == '1':
        print('Reconhecimento selecionado')
        vfr.people_unknown_video(people_encoding)
        
    elif opcao == '2':
        print("salvamento selecionado")
        dest = sf.saves_names()
        sf.saves_face(dest)

    elif opcao == '3':
        break
    
    else:
        print("Opção inválida")
        

