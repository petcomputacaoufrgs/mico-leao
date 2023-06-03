import os
import cv2 as cv
import mediapipe as mp


# função que salva um novo nome no documento e cria uma pasta retorna a direção da pasta criada
def saves_names(new_name):
    
    # faz o append no arquivo com os nomes
    with open('names.txt', 'a', encoding="utf8") as file:
        file.write(',')
        file.write(new_name)
    pasta = r"Faces/train/"+new_name
    os.makedirs(pasta)

    return pasta


def saves_face(dest):

    frameNumber = 0

# Pegando o vídeo da WebCam 0
    cap = cv.VideoCapture(0)
    # Previous Time para colocar o FPS na tela

    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)
    mpFaceDetection = mp.solutions.face_detection
    FaceDetection = mpFaceDetection.FaceDetection()
    drawSpec = mpDraw.DrawingSpec(
        thickness=1, circle_radius=1, color=(0, 255, 0))

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 960)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 582)

    while True:
        success, img = cap.read()

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        resultsMesh = faceMesh.process(imgRGB)
        results = FaceDetection.process(imgRGB)

        # Toda a vez que aperta s ele salva uma foto da pessoa
        if cv.waitKey(10) & 0xFF == ord('s'):
            print('Salvando frame', frameNumber)
            cv.imwrite(dest + '/frame-%d.jpg' % frameNumber, img)
            frameNumber += 1


        if resultsMesh.multi_face_landmarks:
            for faceLms in resultsMesh.multi_face_landmarks:
                mpDraw.draw_landmarks(
                    img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)  # 468 dots


        # Mostrando o vídeo da WebCan
        cv.imshow('CAM', img)
        if cv.waitKey(1) & 0xFF == ord('d'):
            break

# pasta = saves_names(name)
# saves_face(pasta)