# Bibliotecas utilizadas
import cv2 as cv  # OpenCV para manipulação de imagens
import numpy as np 
import faces_train as ft

def video_face_detect():

    people = ft.open_names()

    # leitura da base para DETECTAR faces    
    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    # Lista de pessoas que o modelo foi treinado
    face_recognizer = cv.face.LBPHFaceRecognizer_create() 
    face_recognizer.read('face_trained.yml')

    capture = cv.VideoCapture(0)
    while True:
        isTrue, frame = capture.read()
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)

        for (x,y,w,h) in faces_rect:
            faces_roi = gray[y:y+h, x:x+h]
            

            label, confidence = face_recognizer.predict(faces_roi)
            
            if confidence > 20:
                cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)
                cv.putText(frame, str(people[label]), (x, y+h+25), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
                cv.putText(frame, str(int(confidence))+ '%', (x+w//2-20, y+h+50), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
            else:
                cv.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), thickness=2)
                cv.putText(frame, 'Pessoa desconhecida', (x, y+h+25), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,0,255), thickness=2)

        cv.imshow('Detected Faces', frame)   

        if cv.waitKey(20) & 0xFF == ord('d'):
            break
    capture.release()
    cv.destroyallWindows()
    cv.waitKey(0)
