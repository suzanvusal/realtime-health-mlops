import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from typing import Tuple, List

class SequenceDataset(Dataset):
    """
    A PyTorch Dataset for creating sliding window sequences from time series data.

    Attributes:
        data (np.ndarray): The input time series data.
        labels (np.ndarray): The corresponding labels for each sequence.
        seq_length (int): The length of each sequence.
    """

    def __init__(self, data: np.ndarray, labels: np.ndarray, seq_length: int) -> None:
        """
        Initializes the SequenceDataset with data, labels, and sequence length.

        Args:
            data (np.ndarray): The input time series data.
            labels (np.ndarray): The corresponding labels for each sequence.
            seq_length (int): The length of each sequence.
        """
        self.data = data
        self.labels = labels
        self.seq_length = seq_length

    def __len__(self) -> int:
        """
        Returns the total number of sequences in the dataset.

        Returns:
            int: The number of sequences.
        """
        return len(self.data) - self.seq_length

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Retrieves a sequence and its corresponding label.

        Args:
            index (int): The index of the sequence to retrieve.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: A tuple containing the sequence and its label.
        """
        x = self.data[index:index + self.seq_length]
        y = self.labels[index + self.seq_length]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

def create_data_loader(data: np.ndarray, labels: np.ndarray, seq_length: int, batch_size: int) -> DataLoader:
    """
    Creates a DataLoader for the SequenceDataset.

    Args:
        data (np.ndarray): The input time series data.
        labels (np.ndarray): The corresponding labels for each sequence.
        seq_length (int): The length of each sequence.
        batch_size (int): The number of samples per batch.

    Returns:
        DataLoader: A DataLoader for the SequenceDataset.
    """
    dataset = SequenceDataset(data, labels, seq_length)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
# 10:44:06 — automated update
# feat: add learning rate scheduler with warmup
