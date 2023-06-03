import time
import mediapipe as mp
import cv2 as cv
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"


def FaceMesh():

    # Pegando o vídeo da WebCam 0
    cap = cv.VideoCapture(0)
    # Previous Time para colocar o FPS na tela
    pTime = 0

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

        if resultsMesh.multi_face_landmarks:
            for faceLms in resultsMesh.multi_face_landmarks:
                mpDraw.draw_landmarks(
                    img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)  # 468 dots

        if results.detections:
            for id, detection in enumerate(results.detections):
                bbox = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                x, y, width, height = int(
                    bbox.xmin * iw), int(bbox.ymin * ih), int(bbox.width * iw), int(bbox.height * ih)

                face_roi = img[y:y+height, x:x+width]
                # cv.imshow("ROI", face_roi)
                # break

        # Calculando e Colocando o FPS na Tela
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img, f'FPS: {int(fps)}', (20, 70),
                   cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        # Mostrando o vídeo da WebCan
        cv.imshow("CAM", cv.resize(cv.flip(img, 1), (1920, 1080)))
        if cv.waitKey(1) & 0xFF == ord('d'):
            break


# Chamando a Função
FaceMesh()
