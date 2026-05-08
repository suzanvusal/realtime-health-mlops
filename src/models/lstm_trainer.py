import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Tuple, Any
import mlflow
from mlflow import log_metric, log_param, start_run
from src.models.sequence_dataset import SlidingWindowDataset
from src.models.lstm_model import LSTMModel

class LSTMTrainer:
    def __init__(self, model: LSTMModel, train_data: SlidingWindowDataset, val_data: SlidingWindowDataset, 
                 batch_size: int = 32, learning_rate: float = 0.001, num_epochs: int = 50):
        """
        Initialize the LSTM Trainer.

        :param model: The LSTM model to be trained.
        :param train_data: The training dataset.
        :param val_data: The validation dataset.
        :param batch_size: The batch size for training.
        :param learning_rate: The learning rate for the optimizer.
        :param num_epochs: The number of epochs for training.
        """
        self.model = model
        self.train_data = train_data
        self.val_data = val_data
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.criterion = nn.BCELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def train(self) -> None:
        """
        Train the LSTM model.
        """
        train_loader = DataLoader(self.train_data, batch_size=self.batch_size, shuffle=True)
        val_loader = DataLoader(self.val_data, batch_size=self.batch_size, shuffle=False)

        with start_run():
            log_param("learning_rate", self.learning_rate)
            log_param("num_epochs", self.num_epochs)

            for epoch in range(self.num_epochs):
                self.model.train()
                total_loss = 0.0

                for inputs, targets in train_loader:
                    self.optimizer.zero_grad()
                    outputs = self.model(inputs)
                    loss = self.criterion(outputs, targets)
                    loss.backward()
                    self.optimizer.step()
                    total_loss += loss.item()

                avg_loss = total_loss / len(train_loader)
                log_metric("train_loss", avg_loss, step=epoch)

                self.validate(val_loader, epoch)

    def validate(self, val_loader: DataLoader, epoch: int) -> None:
        """
        Validate the LSTM model.

        :param val_loader: DataLoader for validation data.
        :param epoch: Current epoch number.
        """
        self.model.eval()
        total_loss = 0.0

        with torch.no_grad():
            for inputs, targets in val_loader:
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                total_loss += loss.item()

        avg_loss = total_loss / len(val_loader)
        log_metric("val_loss", avg_loss, step=epoch)

    def save_model(self, model_path: str) -> None:
        """
        Save the trained model to the specified path.

        :param model_path: Path to save the model.
        """
        torch.save(self.model.state_dict(), model_path)
# 10:44:06 — automated update
# refactor: refactor: separate model definition from training logic
_REFACTORED = True
