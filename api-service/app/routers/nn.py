import torch
import torch.nn as nn
from schemas.data import Data
import os

MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "/Release.pt"

device = torch.device("cpu")
dtype = torch.float64

class NN2(nn.Module):
    def __init__(self, in_size, hidden_size, out_size) -> None:
        super(NN2, self).__init__()
        self.layer = nn.Linear(
            in_features=in_size,
            out_features=hidden_size,
            bias=True,
            device=device,
            dtype=dtype
            )
        self.hidden1 = nn.Linear(
            in_features=hidden_size,
            out_features=hidden_size,
            bias=True,
            device=device,
            dtype=dtype
            )
        self.hidden2 = nn.Linear(
            in_features=hidden_size,
            out_features=out_size,
            bias=True,
            device=device,
            dtype=dtype
            )
        self.func1 = nn.LeakyReLU()
        self.func = nn.Sigmoid()

    def forward(self, x):
        x = self.layer(x)
        x = self.func1(x)
        x = self.hidden1(x)
        x = self.func1(x)
        x = self.hidden2(x)
        return self.func(x)

model = NN2(8, 8, 1)

model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

#age, BMI, "1test Ex", "1test In", LF, ROX, Sp, O2 L/min
async def process_data(data: Data):
    data = [data.age, data.BMI, data.test_Ex, data.test_In, data.LF, data.ROX, data.Sp, data.O2]
    data = torch.tensor(data, dtype=dtype, device=device).reshape(1, 8)
    with torch.no_grad():
        return model(data)
