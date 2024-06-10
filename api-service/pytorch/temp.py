# %% [markdown]
'''
# Prep Data #
'''
# %% download data
import pandas as pd

df_data = pd.read_csv("data/new_norm_data.csv")

#df_small_data = pd.read_csv("small_prep_data.csv")
# %%
grouped = df_data.groupby('>7 or <7')

df_zeros = grouped.get_group(0).sample(frac=1)
df_ones = grouped.get_group(1).sample(frac=1)
# %%
df_data = pd.concat(
    [df_zeros.iloc[int(len(df_zeros)*0.2):],
     df_ones.iloc[int(len(df_ones)*0.2):]],
    ignore_index=True
    )

df_clone_data = pd.DataFrame(columns=df_data.columns)

df_clone_data = pd.concat(
    [df_zeros.iloc[:int(len(df_zeros)*0.8)],
    df_ones.iloc[:int(len(df_ones)*0.8)]
    ],
    ignore_index=True
)
# %% set device and dtype
import torch

dtype = torch.float64

device = torch.device("cpu")
print(device)
# %% make torch.tensore data
#Do not remove age, BMI, "1test Ex", LF, ROX, Sp, O2 L/min
# ? 1test In, ComorbAll, L 109, SpO2
features_t = torch.tensor(
    data=df_clone_data.drop(
        columns=["Result", ">7 or <7", "gender", "1test In", "ComorbAll", "L 109", "SpO2"]
        ).values,
    dtype=dtype,
    device=device
)

labels_t = torch.tensor(
    # 1 if >7 else 0
    data=df_clone_data['>7 or <7'].values,
    dtype=dtype,
    device=device
)


train_features_t = torch.tensor(
    data=df_data.drop(
        columns=["Result", ">7 or <7", "gender", "1test In", "ComorbAll", "L 109", "SpO2"]
        ).values,
    dtype=dtype,
    device=device
)

train_labels_t = torch.tensor(
    # 1 if >7 else 0
    data=df_data['>7 or <7'].values,
    dtype=dtype,
    device=device
)

'''
small_features_t = torch.tensor(
    data=df_small_data.drop(
        columns=["Result", ">7 or <7"]
        ).values,
    dtype=dtype,
    device=device
)

small_labels_t = torch.tensor(
    # 1 if H else 0
    data=[1.0 if i=='H' else 0.0 for i in df_small_data['Result'].values],
    dtype=dtype,
    device=device
)
'''
# %% [markdown]
'''
# Prep DataLoader #
'''
# %% DataSet class
from torch.utils.data import Dataset, DataLoader

class MyDataSet(Dataset):
    def __init__(self, features, labels) -> None:
        super().__init__()
        self.features = features
        self.labels = labels
    
    def __len__(self):
        return self.features.size(dim=0)
    
    def __getitem__(self, index):
        x = self.features[index, :]
        y = self.labels[index]
        return x, y
# %% make DataLoader
batch_size=8

dataloader = DataLoader(
    dataset=MyDataSet(
        features=features_t,
        labels=labels_t
    ),
    batch_size=batch_size,
    shuffle=True
)

train_dataloader = DataLoader(
    dataset=MyDataSet(
        features=train_features_t,
        labels=train_labels_t
    ),
    batch_size=batch_size,
    shuffle=True
)

'''
small_dataloader = DataLoader(
    dataset=MyDataSet(
        features=small_features_t,
        labels=small_labels_t
    ),
    batch_size=batch_size,
    shuffle=True
)
'''
# %% [markdown]
'''
# Prep the NN #
'''
# %% NN Class
import torch.nn as nn

class NN(nn.Module):
    def __init__(self, in_size, hidden_size, out_size) -> None:
        super(NN, self).__init__()
        self.layer = nn.Linear(
            in_features=in_size,
            out_features=hidden_size,
            bias=True,
            device=device,
            dtype=dtype
            )
        self.hidden = nn.Linear(
            in_features=hidden_size,
            out_features=out_size,
            bias=True,
            device=device,
            dtype=dtype
            )
        self.func = nn.Sigmoid()

    def forward(self, x):
        x = self.layer(x)
        x = self.func(x)
        x = self.hidden(x)
        return self.func(x)
# %% [markdown]
'''
# Train #
'''
# %%
import torch.optim as optim

train_losses = []
test_losses = []

model = NN(7, 4, 1)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=0.001)
# %%
num_epoch = 1

for epoch in range(num_epoch):

    print(f"Epoch {epoch + 1}/{num_epoch}")

    train_summ_loss = 0.0

    for input, labels in dataloader:

        output = model(input).view(input.size(0))
        loss = criterion(output, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_summ_loss += loss.item()

    train_losses.append(train_summ_loss/len(dataloader))

    print(f"Training Loss: {train_summ_loss/len(dataloader)}")

    test_summ_loss = 0.0

    with torch.no_grad():
        for inputs, labels in train_dataloader:
            outputs = model(inputs).view(inputs.size(0))
            loss = criterion(outputs, labels)
            test_summ_loss += loss.item()

    test_losses.append(test_summ_loss/len(train_dataloader))

    print(f"Testing Loss: {test_summ_loss/len(train_dataloader)}")
# %%
import matplotlib.pyplot as plt

def plot_losses(losses, title="Losses"):
    plt.plot(range(1, len(losses) + 1), losses, label="Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Average Loss")
    plt.title(title)
    plt.legend()
    plt.show()

plot_losses(train_losses, title="Training Losses")
plot_losses(test_losses, title="Testing Losses")
# %%
with torch.no_grad():
    output = model(train_features_t)
#output.squeeze_()
# %%
from NN import myAnalysis, skAnalysis

myAnalysis(train_labels_t, output, True)
skAnalysis(train_labels_t.detach().numpy(), output.detach().numpy())
# %%
