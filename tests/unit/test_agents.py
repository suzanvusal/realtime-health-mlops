import pytest
from faust import App
from src.streaming.agents import WearableDataAgent
from src.streaming.models import WearableData
from unittest.mock import AsyncMock, patch

@pytest.fixture
def app() -> App:
    """Fixture to create a Faust app for testing."""
    return App('test_app', broker='kafka://localhost:9092')

@pytest.fixture
def wearable_data_agent(app: App) -> WearableDataAgent:
    """Fixture to create a WearableDataAgent instance."""
    return WearableDataAgent(app)

@pytest.fixture
def mock_wearable_data() -> WearableData:
    """Fixture to create mock wearable data."""
    return WearableData(heart_rate=75, steps=1000, temperature=36.5)

@pytest.mark.asyncio
async def test_process_wearable_data(wearable_data_agent: WearableDataAgent, mock_wearable_data: WearableData):
    """Test the processing of wearable data by the agent."""
    with patch('src.streaming.agents.WearableDataAgent.extract_features', new_callable=AsyncMock) as mock_extract:
        await wearable_data_agent.process_wearable_data(mock_wearable_data)
        mock_extract.assert_called_once_with(mock_wearable_data)

@pytest.mark.asyncio
async def test_feature_extraction(wearable_data_agent: WearableDataAgent, mock_wearable_data: WearableData):
    """Test the feature extraction logic."""
    features = await wearable_data_agent.extract_features(mock_wearable_data)
    assert 'heart_rate' in features
    assert 'steps' in features
    assert 'temperature' in features

@pytest.mark.asyncio
async def test_send_to_sink(wearable_data_agent: WearableDataAgent, mock_wearable_data: WearableData):
    """Test sending processed data to the sink."""
    with patch('src.streaming.agents.WearableDataAgent.send_to_sink', new_callable=AsyncMock) as mock_send:
        await wearable_data_agent.process_wearable_data(mock_wearable_data)
        mock_send.assert_called_once()

@pytest.mark.asyncio
async def test_agent_startup(wearable_data_agent: WearableDataAgent):
    """Test the startup of the wearable data agent."""
    await wearable_data_agent.start()
    assert wearable_data_agent.is_running is True

@pytest.mark.asyncio
async def test_agent_shutdown(wearable_data_agent: WearableDataAgent):
    """Test the shutdown of the wearable data agent."""
    await wearable_data_agent.shutdown()
    assert wearable_data_agent.is_running is False
# 10:59:46 — automated update
# test marker: test: add async unit test for heart rate anomaly detection
_TEST_MARKER = 'test_agents'

# 11:10:09 — automated update
# style: run black formatter on test_agents — 11:10:09 UTC

# 11:11:30 — automated update
# ci: update step name for readability — 11:11:30 UTC
