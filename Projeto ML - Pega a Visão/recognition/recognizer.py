import torchvision
from torch import nn
import torch
import cv2 as cv
from PIL import Image
from datetime import datetime
import csv
from siamesenet import RecognizerNet, contrastiveLoss

if __name__ == "__main__":
    # Modelo reconhecedor
    model = RecognizerNet()
    model.load_state_dict(torch.load('models\\recognizernet.pt'))
    model.eval()

    # Haar cascade para detecção facial
    haar_features_path = '.\haar_face.xml'#os.path.dirname(os.path.realpath(__file__)) + '..\haar_face.xml'
    haar_cascade = cv.CascadeClassifier(haar_features_path)

    # Imagem de referência
    reference_image = None
    reference_image_bgr = None

    # Nome da pessoa sendo detectada (criação do dataset)
    subject_name = None

    capture = cv.VideoCapture(0)
    while True:
        _, frame = capture.read()
        
        rect_drawing_frame = frame.copy()
        detected_faces = []
        
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        faces_rect = haar_cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=6)

        # Mostra faces detectadas
        for i, (x,y,w,h) in enumerate(faces_rect):
            detected_faces.append(frame_rgb[y:y+h, x:x+h])
            cv.rectangle(rect_drawing_frame, (x,y), (x+w, y+h), (0,255,0), thickness=2)
            cv.putText(rect_drawing_frame, f'FACE {i}', (x, y+h), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness=3)

        cv.imshow('Faces', rect_drawing_frame)
        if reference_image is not None:
            cv.imshow('Reference', reference_image_bgr)

        key = cv.waitKey(1)

        # Captura imagem para referência
        if key == ord("c"):
            if len(detected_faces) != 1:
                if len(detected_faces) > 1:
                    print('Cannot capture: More than one face in frame')
                else:
                    print('Cannot capture: No faces detected')
                continue

            reference_image = detected_faces[0]
            reference_image_bgr = cv.cvtColor(reference_image, cv.COLOR_RGB2BGR)
            print('Captured new reference image')

        # Adiciona essa imagem à pasta de imagens de treino
        if key == ord("C"):
            if len(detected_faces) != 1:
                if len(detected_faces) > 1:
                    print('Cannot capture: More than one face in frame')
                else:
                    print('Cannot capture: No faces detected')
            
            if subject_name is None:
                subject_name = input("INSERT THE SUBJECT'S NAME:")
            
            face = cv.cvtColor(detected_faces[0], cv.COLOR_RGB2BGR)

            # Salva como nome + timestamp
            with open('facedataset.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                
                timestamp = datetime.now().strftime("%m%d%Y_%H%M%S")
                newfile = f'{subject_name}_{timestamp}.png'
                folder = 'faces\\'
                if cv.imwrite(folder + newfile, face):
                    print(f'Added new face capture for subject "{subject_name}"')
                else:
                    print(f'Error: Could not save capture')
                    break

                writer.writerow([subject_name, newfile])



        # Usando a imagem referência, diz se as imagens são da mesma face ou não
        if key == ord("r"):
            if reference_image is None:
                print('No reference image (press \'c\' to capture)')
                continue

            for i, face in enumerate(detected_faces):            
                face = Image.fromarray(face) # Imagem do PIL
                face = model.preprocess(face) # Preprocessamento para processamento da rede
                face = face.unsqueeze(0) # Dimensão de batch
                reference = Image.fromarray(reference_image) # Mesmo que acima
                reference = model.preprocess(reference)
                reference = reference.unsqueeze(0)
                
                out1, out2 = model(face, reference)
                dissimilarity = contrastiveLoss(out1, out2, 0)
                print(f"Face {i}:")
                print(f"\tDISSIMILARITY SCORE: {dissimilarity}")

        if key == ord('q'):
            cv.destroyAllWindows()
            break