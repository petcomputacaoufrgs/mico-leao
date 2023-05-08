import os
import cv2 as cv
import numpy as np

# Funções desse arquivo:
# open_names()  # pega os nomes e retorna uma lista de nomes
# create_train() # treina o modelo 
# saves_names() # salva o nome da pessoa no arquivo e cria uma pasta

# função que salva um novo nome no documento (colocar junto com o script do Tomás)
def saves_names():
    new_name = input('Digite um novo nome:')
    # Abre o arquivo com os nomes
    with open('names.txt', 'a', encoding="utf8") as file:
        file.write(',')
        file.write(new_name)
    os.makedirs(r"Faces/train/"+new_name)
        
# função que recarrega os nomes
def open_names():
    # Abre o arquivo com os nomes
    with open('names.txt', 'r', encoding="utf8") as file:
        people_file = file.read()

    # Salva em uma lista
    people = people_file.split(',')

    return people

# Função que treina o modelo
def create_train():

    people = open_names()

    # direção das pastas das pessoas
    DIR = r'Faces/train'

    # Leitura da base que DETECTA rostos
    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    # Traços das pessoas e nomes (não ficaria melhor com dicionário?)
    features = []
    labels = []


    # para cada pessoa
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        # para cada imagem
        for img in os.listdir(path):
            # le cada imagem e converte para escala de cinza
            img_path = os.path.join(path, img)
            img_array = cv.imread(img_path)
            gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)

            # detecta a face na imagem
            faces_rect = haar_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=4)

            # pega a região de interesse na imagem (rosto)
            for (x, y, w, h) in faces_rect:
                # roi região de interesse
                faces_roi = gray[y:y+h, x:x+w]
                # guarda na lista de features com seus respectivos labels
                features.append(faces_roi)
                labels.append(label)

    # guarda os features em um array
    features = np.array(features, dtype='object')
    labels =np.array(labels)


    face_recognizer = cv.face.LBPHFaceRecognizer_create() 

    # Treinar o reconhecedor com a lista de features e labels
    face_recognizer.train(features, labels)

    # Salva tudo para utilizar posteriormente
    face_recognizer.save('face_trained.yml')
    np.save('features.npy', features)
    np.save('labels.npy', labels)

    # mostra o tamanho da base
    #print(f'Features = {len(features)}')
    #print(f'Labels = {len(labels)}')
    print(f'Treinamento Encerrado *-*\n')


