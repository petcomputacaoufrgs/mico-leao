import torchvision
from torch import nn
import cv2 as cv
from PIL import Image
import os



if __name__ == "__main__":
    
    # Pesos e pré-processamento da MobileNetV3
    weights = torchvision.models.MobileNet_V3_Small_Weights.DEFAULT
    preprocess = weights.transforms()

    # Utilização da rede como extratora de features
    feature_extractor = torchvision.models.mobilenet_v3_small(weights=weights)
    feature_extractor.classifier = nn.Identity()

    # Haar cascade para detecção facial
    haar_features_path = '.\haar_face.xml'#os.path.dirname(os.path.realpath(__file__)) + '..\haar_face.xml'
    haar_cascade = cv.CascadeClassifier(haar_features_path)

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

        
        if cv.waitKey(1) == ord("r"):
            for i, face in enumerate(detected_faces):            
                face = Image.fromarray(frame_rgb) # Imagem do PIL
                face = preprocess(face) # Preprocessamento para processamento da rede
                face = face.unsqueeze(0) # Adiciona dimensão de batch
                features = feature_extractor(face)
                print(f"Face {i}:")
                print(features)
                print(features.shape)
