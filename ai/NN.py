import torch
import pandas as pd
import torch.nn as nn
import torch.functional as F
import torch.optim as optim
from torch.utils.data import Dataset


def getDevice():
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    return device


class NN(nn.Module):
    def __init__(self, in_size, hidden_size, out_size) -> None:
        super(NN, self).__init__()
        self.hidd = nn.Linear(in_features=in_size, out_features=hidden_size, dtype=torch.float64)
        self.hidd_f = nn.ReLU()
        self.out = nn.Linear(in_features=hidden_size, out_features=out_size, dtype=torch.float64)
        self.out_f = nn.Sigmoid()

    def forward(self, x):
        x = self.hidd(x)
        x = self.hidd_f(x)
        x = self.out(x)
        return self.out_f(x)


class CustomDataset(Dataset):
    def __init__(self, feature_tensors, result_tensor):
        self.feature = feature_tensors
        self.result = result_tensor

    def __len__(self):
        return len(self.result)

    def __getitem__(self, idx):
        # Combine all feature tensors into a single input tensor
        x = self.feature[idx, :]
        #x = torch.stack([t[idx] for t in self.feature_tensors])
        y = self.result[idx]
        #print(f"f:{self.feature.shape}\nl:{self.result.shape}\nx:{x.shape}\ny:{y.shape}")
        return x, y
    
