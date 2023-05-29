
import os
import cv2 as cv

# função que salva um novo nome no documento e cria uma pasta retorna a direção da pasta criada
def saves_names():
    new_name = input('Digite um novo nome:')
    # faz o append no arquivo com os nomes
    with open('names.txt', 'a', encoding="utf8") as file:
        file.write(',')
        file.write(new_name)
    pasta = r"Faces/train/"+new_name
    os.makedirs(pasta)
    
    return pasta

def saves_face(dest):
     # leitura da base para DETECTAR faces    
    haar_cascade = cv.CascadeClassifier('haar_face.xml')
    frameNumber=0
    

    capture = cv.VideoCapture(0)
    while True:
        isTrue, frame = capture.read()
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
        

        # Toda a vez que aperta s ele salva uma foto da pessoa
        if cv.waitKey(20) & 0xFF == ord('s'):
            print('Salvando frame', frameNumber)
            cv.imwrite(dest + '/frame-%d.jpg' % frameNumber, frame)
            frameNumber+=1

        for (x,y,w,h) in faces_rect:
            faces_roi = gray[y:y+h, x:x+h]

        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)

        cv.imshow('Detected Faces', frame)  

        if cv.waitKey(20) & 0xFF == ord('d'):
            break

  