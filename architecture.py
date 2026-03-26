import torch.nn as nn
from torchvision.models import resnet50

class ResNetLungCancer(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        self.resnet = resnet50(weights=None)
        in_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Identity()
        
        self.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
        
    def forward(self, x):
        features = self.resnet(x)
        return self.fc(features)
