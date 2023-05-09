from siamesenet import RecognizerNet, contrastiveLoss
from dataset import FacesDataset
from torch.utils.data import DataLoader
import torch


if __name__ == "__main__":
    model = RecognizerNet()

    epochs = 10
    lr = 0.1
    momentum = 0.9
    batch_size = 64

    faces_ds = FacesDataset('facedataset.csv', 'faces', model.preprocess)
    dataloader = DataLoader(faces_ds, batch_size, True)

    optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=momentum)

    for epoch in range(epochs):
        epoch_loss = 0.0
        
        for (imgs1, imgs2, same_face) in dataloader:
            optimizer.zero_grad()

            out1, out2 = model(imgs1, imgs2)

            loss = contrastiveLoss(out1, out2, same_face)
            loss.backward()

            optimizer.step()
            
            epoch_loss += loss * out1.shape[0] # Multiplica pelo número de batches para compensar a média aplicada na função de erro


        print(f'EPOCH {epoch} : Loss: {epoch_loss / len(faces_ds)}')

    torch.save(model.state_dict(), 'models\\recognizernet.pt')