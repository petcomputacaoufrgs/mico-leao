import face_recognition
import time
import mediapipe as mp
import cv2 as cv
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"


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

    # Pegando o vídeo da WebCam 0
    cap = cv.VideoCapture(0)
    # Previous Time para colocar o FPS na tela
    pTime = 0
    vai = 0
    nome = 'Desconhecido'
    cor = (0, 0, 255)

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
        cv.putText(img, "Apenas 1 pessoa por vez", (20, 20),
                   cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 0, 0), thickness=2)

        # if resultsMesh.multi_face_landmarks:
        #     for faceLms in resultsMesh.multi_face_landmarks:
        #         mpDraw.draw_landmarks(
        #             img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)  # 468 dots

        if results.detections:
            for id, detection in enumerate(results.detections):
                bbox = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                x, y, width, height = int(
                    bbox.xmin * iw), int(bbox.ymin * ih), int(bbox.width * iw), int(bbox.height * ih)

                cv.rectangle(img, (x, y-50),
                             (x+width, y+height), (0, 255, 0), 3)
                # face_roi = imgRGB[y-100:y+height+100, x-100:x+width+100]

                if vai % 60 == 0 or vai % 61 == 0 or vai % 62 == 0 or vai % 63 == 0:
                    nome = 'Nao eh do PET'
                    cor = (0, 0, 255)

                    try:
                        # encoding só da roi
                        unknown_encoding = face_recognition.face_encodings(imgRGB)[
                            0]

                        for person in people_encoding:
                            results = face_recognition.compare_faces(
                                [people_encoding[person]], unknown_encoding)
                            if results[0]:
                                nome = person
                                cor = (0, 255, 0)

                    except:
                        print('Não há pessoas')

                    cv.putText(img, nome, (x, y+height+25),
                               cv.FONT_HERSHEY_COMPLEX, 1.0, cor, thickness=2)

                    if vai > 63:
                        vai = 0
                vai += 1

        # cv.imshow("ROI", face_roi)

        # Calculando e Colocando o FPS na Tela
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, f'FPS: {int(fps)}', (20, 70),
                   cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        # Mostrando o vídeo da WebCan
        #cv.imshow("CAM", cv.resize(cv.flip(img,1), (1920,1080)))
        cv.imshow("CAM", cv.resize(img,(1920,1080)))
        if cv.waitKey(1) & 0xFF == ord('d'):
            break



