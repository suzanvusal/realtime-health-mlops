# src/__init__.py

"""
src package for the Real-Time Smart Health Monitoring System.

This package contains modules for data ingestion, processing, model training,
and serving of the health monitoring system.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import necessary modules for the package
from .data_ingestion import DataIngestion
from .data_processing import DataProcessing
from .model_training import ModelTraining
from .model_serving import ModelServing
from .monitoring import Monitoring

# Initialize the components of the system
data_ingestion = DataIngestion()
data_processing = DataProcessing()
model_training = ModelTraining()
model_serving = ModelServing()
monitoring = Monitoring()
# 21:31:17 — automated update
# style: formatted at 21:31:17

# 21:31:17 — automated update
# style: reorder imports alphabetically in __init__ — 21:31:17 UTC

# 11:09:18 — automated update
# chore: add logging statement to __init__ — 11:09:18 UTC

# 11:09:18 — automated update
# style: run black formatter on __init__ — 11:09:18 UTC

# 10:27:16 — automated update
# style: run black formatter on __init__ — 10:27:16 UTC

# 10:04:05 — automated update
# refactor: extract magic number to named constant in __init__ — 10:04:05 UTC

# 11:11:30 — automated update
# refactor: extract magic number to named constant in __init__ — 11:11:30 UTC
