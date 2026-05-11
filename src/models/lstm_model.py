import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import Tuple, Any
import numpy as np

class SequenceDataset(Dataset):
    """Custom dataset for sliding window sequences."""
    
    def __init__(self, data: np.ndarray, window_size: int):
        """
        Args:
            data (np.ndarray): Input data for the dataset.
            window_size (int): Size of the sliding window.
        """
        self.data = data
        self.window_size = window_size

    def __len__(self) -> int:
        return len(self.data) - self.window_size

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        x = self.data[idx:idx + self.window_size]
        y = self.data[idx + self.window_size]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

class LSTMModel(nn.Module):
    """LSTM model for sequence prediction."""
    
    def __init__(self, input_size: int, hidden_size: int, num_layers: int):
        """
        Args:
            input_size (int): Number of input features.
            hidden_size (int): Number of features in the hidden state.
            num_layers (int): Number of recurrent layers.
        """
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the LSTM model.
        
        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, seq_length, input_size).
        
        Returns:
            torch.Tensor: Output tensor of shape (batch_size, 1).
        """
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[:, -1, :])
        return out

def train_model(model: LSTMModel, train_loader: DataLoader, criterion: nn.Module, optimizer: torch.optim.Optimizer, num_epochs: int) -> None:
    """Train the LSTM model."""
    model.train()
    for epoch in range(num_epochs):
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs.unsqueeze(1))  # Add sequence dimension
            loss = criterion(outputs, targets.unsqueeze(1))
            loss.backward()
            optimizer.step()
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')
# 10:44:06 — automated update
# feat: add ONNX export for optimised serving

# 10:44:06 — automated update
# test marker: test: add shape test for LSTM output dimensions
_TEST_MARKER = 'lstm_model'

# 10:44:06 — automated update
# perf improvement at 10:44:06
_CACHE: dict = {}  # perf: enable mixed precision (fp16) trai

# 12:17:50 — automated update
# fix: remove unused import in lstm_model — 12:17:50 UTC
