import unittest
import torch
import numpy as np
from src.models.lstm_model import LSTMModel
from src.models.sequence_dataset import SlidingWindowDataset

class TestLSTMModel(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the test environment."""
        self.input_size = 10
        self.hidden_size = 20
        self.num_layers = 2
        self.sequence_length = 5
        self.batch_size = 3
        
        self.model = LSTMModel(input_size=self.input_size, 
                               hidden_size=self.hidden_size, 
                               num_layers=self.num_layers)
        
        # Create a dummy dataset
        self.data = np.random.rand(self.batch_size, self.sequence_length, self.input_size).astype(np.float32)
        self.target = np.random.rand(self.batch_size, 1).astype(np.float32)
        self.dataset = SlidingWindowDataset(self.data, self.target, window_size=self.sequence_length)
        
    def test_model_forward(self):
        """Test the forward pass of the LSTM model."""
        inputs = torch.from_numpy(self.data)
        outputs = self.model(inputs)
        
        self.assertEqual(outputs.shape, (self.batch_size, 1), "Output shape mismatch")
        
    def test_model_training(self):
        """Test the training step of the LSTM model."""
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        self.model.train()
        inputs = torch.from_numpy(self.data)
        targets = torch.from_numpy(self.target)
        
        optimizer.zero_grad()
        outputs = self.model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        self.assertIsNotNone(loss.item(), "Loss should not be None after backward pass")
        
    def test_dataset_length(self):
        """Test the length of the SlidingWindowDataset."""
        self.assertEqual(len(self.dataset), self.batch_size, "Dataset length mismatch")
        
    def test_dataset_item(self):
        """Test retrieving an item from the dataset."""
        x, y = self.dataset[0]
        self.assertEqual(x.shape, (self.sequence_length, self.input_size), "Input shape mismatch")
        self.assertEqual(y.shape, (1,), "Target shape mismatch")

if __name__ == '__main__':
    unittest.main()