import torch
import torch.nn as nn

class HighlightLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=32):
        super(HighlightLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return self.sigmoid(out)