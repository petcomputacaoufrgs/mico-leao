import cv2 as cv 
import numpy as np

# leitura da base para DETECTAR faces    
haar_cascade = cv.CascadeClassifier('haar_face.xml')

# Lista de pessoas que o modelo foi treinado
people = ['Ben Afflek', 'Elton John','Jerry Seinfield', 'Madonna', 'Mindy Kaling', 'Laura Reis']
face_recognizer = cv.face.LBPHFaceRecognizer_create() 
face_recognizer.read('face_trained.yml')

capture = cv.VideoCapture(0)
while True:
    isTrue, frame = capture.read()
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)

    for (x,y,w,h) in faces_rect:
        faces_roi = gray[y:y+h, x:x+h]
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)

        label, confidence = face_recognizer.predict(faces_roi)

        cv.putText(frame, str(people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)

    cv.imshow('Detected Faces', frame)   

    if cv.waitKey(20) & 0xFF == ord('d'):
        break
capture.release()
cv.destroyallWindows()
cv.waitKey(0)
