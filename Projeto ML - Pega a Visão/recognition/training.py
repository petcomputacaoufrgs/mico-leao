from siamesenet import RecognizerNet, contrastiveLoss
from dataset import FacesDataset
from torch.utils.data import DataLoader
from tqdm import tqdm
from typing import NamedTuple

import torchvision, torch
import argparse
import os

class ModelConfig(NamedTuple):
    n_epochs : int
    lr : float
    momentum : float
    batch_size : int
    workers : int



def train(model : RecognizerNet, config : ModelConfig , path_to_save_file : str = 'models\\recognizernet.pt', 
          use_custom_ds : bool = False):

    if use_custom_ds:
        dataset = FacesDataset('facedataset.csv', 'faces', model.preprocess)
    else:
        dataset = torchvision.datasets.LFWPairs('./LFWPairs', download=True, transform=model.preprocess)
    
    dataloader = DataLoader(
        dataset=dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.workers
        )
    
    optimizer = torch.optim.SGD(model.parameters(), lr=config.lr, momentum=config.momentum)

    for epoch in range(config.n_epochs):
        running_loss = 0.0
        running_corrects = 0
        
        for imgs1, imgs2, same_face in tqdm(dataloader):
            optimizer.zero_grad()

            out1, out2 = model(imgs1, imgs2)

            loss = contrastiveLoss(out1, out2, same_face)
            loss.backward()

            optimizer.step()

            running_loss += loss * out1.shape[0] # Multiplica pelo número de batches para compensar a média aplicada na função de erro
            running_corrects += torch.sum(torch.where(same_face == 1, loss <= accuracy_threshold, loss > accuracy_threshold))


        epoch_loss = running_loss / len(dataset)
        
        print(f'EPOCH {epoch} : Loss: {epoch_loss}')

    try:
        torch.save(model.state_dict(), path_to_save_file)    
    except FileNotFoundError as e:
        print(f'Could not find file "{e.filename}". Saving the model in current directory')
        path = os.path.join(os.curdir, 'model.pt')
        torch.save(model.state_dict(), path) 
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Siamese Network Training"
    )

    parser.add_argument('epochs', type=int)
    parser.add_argument('-pt', '--pretrainedfile', type=str)
    parser.add_argument('-lr', '--learningrate', type=float, default=0.1)
    parser.add_argument('-m', '--momentum', type=float, default=0.9)
    parser.add_argument('-b', '--batchsize', type=int, default=128)
    parser.add_argument('-w', '--nworkers', type=int, default=8)

    args = parser.parse_args()

    model = RecognizerNet()
    
    if args.pretrainedfile is not None:
        model.load_state_dict(torch.load(args.pretrainedfile))
        model.train()

    config = ModelConfig(args.epochs, args.learningrate, args.momentum, args.batchsize, args.nworkers)

    train(model, config)
