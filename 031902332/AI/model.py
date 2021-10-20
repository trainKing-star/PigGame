import torch
import torch.nn as nn


class MyModel(nn.Module):

    def __init__(self, input_size, num_labels, device):
        super(MyModel, self).__init__()
        self.device = device
        self.criterion = nn.CrossEntropyLoss()

        self.start = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            # nn.Linear(64, 128),
            # nn.ReLU(),
            # nn.Linear(128, 256),
            # nn.ReLU(),
            # nn.Linear(256, 128),
            # nn.ReLU(),
            # nn.Linear(128, 64),
            # nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, num_labels)
        )

    def forward(self, data, label=None):
        probabilities = self.start(data)
        if label is not None:
            loss = self.criterion(probabilities, label)
            return loss, probabilities
        return probabilities
