import torch
import pandas as pd
import torch.nn as nn
import torch.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, f1_score


def skAnalysis(label, output):
    AUC = roc_auc_score(
        label,
        output
    )

    fpr, tpr, threshold = roc_curve(
        label,
        output
    )

    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % AUC)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


def myAnalysis(label, output, only_Acc_F1 = False):
    accuracys = []
    precisions = []
    specicitys = []
    recalls = []# sensetivity
    F1s = []
    
    x = [i/len(label) for i in range(len(label))]

    for n in x:

        results = [1. if i > n else 0. for i in output]

        TN = 0
        TP = 0
        FN = 0
        FP = 0

        for (e, y) in zip(label, results):
            if e == y:
                if e == 1.:
                    TP += 1
                else:
                    TN += 1
            else:
                if e == 1.:
                    FN += 1
                else:
                    FP += 1

        if TP == 0:
            x = [i for i in x if i < n]
            break

        
        accuracys.append((TP + TN)/(len(results)))
        specicitys.append((TN)/(TN+FP))
        precision = (TP)/(TP+FP)
        precisions.append(precision)
        recall = (TP)/(TP+FN)# sensetivity
        recalls.append(recall)
        F1s.append(2*(recall*precision)/(recall+precision))

    FPR = [1 - i for i in specicitys]

    AUC = 0
    for i in range(2, len(FPR)):
        h = FPR[i-1] - FPR[i]
        m = recalls[i] + recalls[i - 1]
        AUC += h * m / 2

    plt.plot(FPR, recalls, label="ROC|AUC = %0.4f" % AUC)
    plt.xlabel("False Pos")
    plt.ylabel("True Pos Rate")
    plt.title("ROC")
    plt.legend()
    plt.show()

    if not only_Acc_F1:
        plt.plot(x, precisions, label="Prec")
        plt.plot(x, specicitys, label="Spec")
        plt.plot(x, recalls, label="Rec/senset")

    plt.plot(x, accuracys, label="Acc|Max= %0.3f" % max(accuracys))
    plt.plot(x, F1s, label="F1")
    plt.xlabel("x")
    plt.ylabel("Rate")
    plt.title("Stats")
    plt.legend()
    plt.show()


def getDevice():
    return torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def getDataLoader(features, labels, batch_size, shuffle=True):
    return DataLoader(
        CustomDataset(
            features_tensor=features,
            labels_tensor=labels
        ),
        batch_size=batch_size,
        shuffle=shuffle
    )


class NN(nn.Module):
    def __init__(self, in_size, hidden_size, out_size):
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
    
    def get_hidden(self, x):
        with torch.no_grad():
            x = self.hidd(x)
            return self.hidd_f(x)


class CustomDataset(Dataset):
    def __init__(self, features_tensor, labels_tensor):
        self.features = features_tensor
        self.labels = labels_tensor

    def __len__(self):
        return self.features.size(dim=0)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]
