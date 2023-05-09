from torch.utils.data import Dataset
from torchvision.io import read_image
import torch
import torchvision
import pandas as pd
import os
import cv2 as cv
import numpy as np
from itertools import combinations

class FacesDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.faces_df = pd.read_csv(csv_file)
        self.face_pairs = list(combinations(zip(self.faces_df['subject_name'],self.faces_df['image_path']), 2))
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.face_pairs)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_pair = self.face_pairs[idx]

        subject1 = img_pair[0][0]
        subject2 = img_pair[1][0]
        label = 1 if (subject1 == subject2) else 0
        img_path1 = os.path.join(self.root_dir, img_pair[0][1])
        img_path2 = os.path.join(self.root_dir, img_pair[1][1])

        img1 = read_image(img_path1)
        img2 = read_image(img_path2)
        
        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)

        sample = (img1, img2, label)
        return sample

    def getImageFromSample(self, sample):

        im1 = np.moveaxis(sample[0].numpy(), [0, 1, 2], [2, 0, 1])
        im2 = np.moveaxis(sample[1].numpy(), [0, 1, 2], [2, 0, 1])
        
        shape1, shape2 = im1.shape[:-1], im2.shape[:-1]
        new_shape = shape1 if shape1 > shape2 else shape2
        
        im1 = cv.resize(im1, new_shape)
        im2 = cv.resize(im2, new_shape)

        im1 = cv.cvtColor(im1, cv.COLOR_RGB2BGR)
        im2 = cv.cvtColor(im2, cv.COLOR_RGB2BGR)

        image = cv.hconcat([im1, im2])
        text = 'SAME' if sample[2] else 'DIFFERENT'
        color = (0,255,0) if sample[2] else (0,0,255)
        cv.putText(image, text, (0+2, new_shape[0]-2), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        return image



if __name__ == "__main__":
    dataset = FacesDataset('facedataset.csv', 'faces')
    print(f'Displaying {len(dataset)} samples')
    for sample in dataset:
        image = dataset.getImageFromSample(sample)
        cv.imshow('DATASET', image)
        cv.waitKey()
