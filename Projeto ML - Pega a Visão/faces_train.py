import os
import cv2 as cv
import numpy as np

# Lista com o nome das pastas de cada pessoa que o modelo vai ser treinado
people = ['Ben Afflek', 'Elton John','Jerry Seinfield', 
          'Madonna', 'Mindy Kaling', 'Laura Reis']

# direção das pastas das pessoas
DIR = r'Faces/train'

# Leitura da base que DETECTA rostos
haar_cascade = cv.CascadeClassifier('haar_face.xml')

# Traços das pessoas e nomes (não ficaria melhor com dicionário?)
features = []
labels = []

# Função que treina o modelo
def create_train():
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

# chama a função 
create_train()

# mostra o tamanho da base
print(f'Length of the features = {len(features)}')
print(f'Length of the labels = {len(labels)}')
print(f'Treinamento Encerrado *-*')

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



