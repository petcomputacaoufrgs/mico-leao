import cv2 as cv
import mediapipe as mp
import time


# Chamando a Função
#FaceMesh()

def FaceMesh():

    # Pegando o vídeo da WebCam 0
    cap = cv.VideoCapture(0)
    # Previous Time para colocar o FPS na tela 
    pTime = 0

    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=3)
    drawSpec = mpDraw.DrawingSpec(thickness =1, circle_radius = 1)


    while True:
        success, img = cap.read()
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = faceMesh.process(imgRGB)

        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                    mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec) #468 dots
        
        # Calculando e Colocando o FPS na Tela 
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, f'FPS: {int(fps)}', (20,70), cv.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)

        # Mostrando o vídeo da WebCan
        cv.imshow("CAM", img)
        if cv.waitKey(1) & 0xFF == ord('d'):
                break


# Chamando a Função
FaceMesh()