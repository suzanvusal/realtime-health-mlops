FROM python:3.9-slim

# Set environment variables
ENV MLFLOW_HOME=/mlflow
ENV PYTHONUNBUFFERED=1

# Create a directory for MLflow
RUN mkdir -p $MLFLOW_HOME
WORKDIR $MLFLOW_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MLflow entrypoint script
COPY mlflow_entrypoint.py .

# Expose the MLflow server port
EXPOSE 5000

# Command to run the MLflow server
CMD ["python", "mlflow_entrypoint.py"]