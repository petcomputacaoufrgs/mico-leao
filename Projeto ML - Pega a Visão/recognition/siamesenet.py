import torchvision
import torch
from torch import nn
import numpy as np

class RecognizerNet(nn.Module):
    def __init__(self) -> None:
        super().__init__()

        # Pesos e pré-processamento da MobileNetV3
        weights = torchvision.models.MobileNet_V3_Small_Weights.DEFAULT
        self.preprocess = weights.transforms()

        # Utilização da rede como extratora de features
        self.feature_extractor = torchvision.models.mobilenet_v3_small(weights=weights)
        self.feature_extractor.classifier = nn.Identity()

        # Freezing do treinamento do extrator
        for param in self.feature_extractor.parameters():
            param.requires_grad = False

        # Camadas utilizadas para aprender as relações entre faces
        self.linear_stack = nn.Sequential(
            nn.Linear(576, 1000),
            nn.Tanh()
        )

    def forward_once(self, x):
        x = self.feature_extractor(x)
        x = self.linear_stack(x)
        return x

    def forward(self, x1, x2):
        x1 = self.forward_once(x1)
        x2 = self.forward_once(x2)
        return x1, x2
    


def contrastiveLoss(x1, x2, label, margin=2.0):
    # Calcula similaridade
    x = nn.functional.pairwise_distance(x1, x2, keepdim=True) # Distância L2
    x = torch.mean((1 - label) * torch.pow(x, 2) + (label) * torch.pow(torch.clamp(margin - x, min=0), 2))
    return x
