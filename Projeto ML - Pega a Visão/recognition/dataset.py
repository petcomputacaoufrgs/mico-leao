from torch.utils.data import Dataset
import torch
import pandas as pd
import os
import cv2 as cv
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
        same_method = (subject1 == subject2)
        img_path1 = os.path.join(self.root_dir, img_pair[0][1])
        img_path2 = os.path.join(self.root_dir, img_pair[1][1])

        img1 = cv.imread(img_path1)
        img2 = cv.imread(img_path2)
        
        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)

        sample = (img1, img2, same_method)
        return sample

    def getImageFromSample(self, sample):
        shape1, shape2 = sample[0].shape[:-1], sample[1].shape[:-1]
        new_shape = shape1 if shape1 > shape2 else shape2
        im1 = cv.resize(sample[0], new_shape)
        im2 = cv.resize(sample[1], new_shape)
        image = cv.hconcat([im1, im2])
        text = 'SAME' if sample[2] else 'DIFFERENT'
        color = (0,255,0) if sample[2] else (0,0,255)
        cv.putText(image, text, (0+2, new_shape[0]-2), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        return image



if __name__ == "__main__":
    dataset = FacesDataset('facedataset.csv', 'faces', None)
    print(f'Displaying {len(dataset)} samples')
    for sample in dataset:
        image = dataset.getImageFromSample(sample)
        cv.imshow('DATASET', image)
        cv.waitKey()
