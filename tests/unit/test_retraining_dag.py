import pytest
from unittest.mock import patch, MagicMock
from src.retraining.dags.drift_sensor import DriftSensor
from src.retraining.dags.retraining_tasks import retrain_model
from airflow.models import DagBag


@pytest.fixture
def dagbag() -> DagBag:
    """Fixture to load the DAG for testing."""
    return DagBag(dag_folder='src/retraining/dags', include_examples=False)


def test_drift_sensor_initialization(dagbag: DagBag) -> None:
    """Test the initialization of the DriftSensor."""
    drift_sensor = DriftSensor()
    assert drift_sensor is not None
    assert isinstance(drift_sensor, DriftSensor)


@patch('src.retraining.dags.drift_sensor.check_drift')
def test_drift_detection(mock_check_drift: MagicMock, dagbag: DagBag) -> None:
    """Test the drift detection logic."""
    mock_check_drift.return_value = True
    drift_sensor = DriftSensor()
    drift_detected = drift_sensor.check_drift()
    assert drift_detected is True
    mock_check_drift.assert_called_once()


@patch('src.retraining.dags.retraining_tasks.retrain_model')
def test_retraining_triggered_on_drift(mock_retrain_model: MagicMock, dagbag: DagBag) -> None:
    """Test that retraining is triggered when drift is detected."""
    drift_sensor = DriftSensor()
    drift_sensor.check_drift = MagicMock(return_value=True)

    if drift_sensor.check_drift():
        retrain_model()

    mock_retrain_model.assert_called_once()


@patch('src.retraining.dags.retraining_tasks.retrain_model')
def test_no_retraining_when_no_drift(mock_retrain_model: MagicMock, dagbag: DagBag) -> None:
    """Test that retraining is not triggered when no drift is detected."""
    drift_sensor = DriftSensor()
    drift_sensor.check_drift = MagicMock(return_value=False)

    if drift_sensor.check_drift():
        retrain_model()

    mock_retrain_model.assert_not_called()


def test_dag_import(dagbag: DagBag) -> None:
    """Test that the DAG is imported correctly."""
    assert 'drift_retraining_dag' in dagbag.dags
    dag = dagbag.dags['drift_retraining_dag']
    assert dag is not None
    assert len(dag.tasks) > 0
    assert 'drift_sensor_task' in dag.task_ids
    assert 'retrain_task' in dag.task_ids


def test_dag_structure(dagbag: DagBag) -> None:
    """Test the structure of the DAG."""
    dag = dagbag.dags['drift_retraining_dag']
    assert dag.task_dict['drift_sensor_task'].downstream_task_ids == {'retrain_task'}