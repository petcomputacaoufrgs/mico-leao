import cv2 as cv
import face_recognition
import os 

# função que recarrega os nomes
def open_names():
    # Abre o arquivo com os nomes
    with open('names.txt', 'r', encoding="utf8") as file:
        people_file = file.read()

    # Salva em uma lista
    people = people_file.split(',')

    return people

# Função que faz o encoding dos rostos
def people_known():
    
    # pega o nome das pessoas no arquivo names.txt
    people = open_names()

    # direção das pastas das pessoas
    DIR = r'Faces/train'

    # faz um dicionário para as pessoas 
    people_encoding = dict()

    # para cada pessoa
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        img_path = os.path.join(path, os.listdir(path)[0])
        img = cv.imread(img_path)
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        people_encoding[person] = face_recognition.face_encodings(imgRGB)[0]

    return people_encoding
    

def people_unknown_video(people_encoding):

    # leitura da base para DETECTAR faces    
    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    print('Terminou o encoding das pessoas conhecidas')

    cap = cv.VideoCapture(0)
    fps = 3
    pessoas_conhecidas = []

    while True:
        success, frame = cap.read()
        imgGRAY = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        detect_faces = haar_cascade.detectMultiScale(imgGRAY, scaleFactor=1.1, minNeighbors=6)
        
        
        for (x,y,w,h) in detect_faces:

            # região de interesse
            imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            face_roi = frame[y:y+h, x:x+w]
            cv.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), thickness=2)
            
            if (fps%3 == 0):
                try:
                    # encoding só da roi
                    unknown_encoding = face_recognition.face_encodings(imgRGB)[0]

                    for person in people_encoding:
                        results = face_recognition.compare_faces([people_encoding[person]], unknown_encoding)
                        if results[0]:
                            nome = person
                            cv.putText(frame, nome, (x, y+h+25), cv.FONT_HERSHEY_COMPLEX, 1.0, (0,255,0), thickness=2)

                except:
                    print('Não há pessoas')
                
                fps = 0
        
        # Mostrando o vídeo da WebCan
        
        fps+=1

        cv.imshow("CAM", frame)
        if cv.waitKey(1) & 0xFF == ord('d'):
            break

    cap.release()
    cv.destroyallWindows()
    cv.waitKey(0)

