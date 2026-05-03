import pytest
from unittest.mock import MagicMock, patch
from src.streaming.alert_engine import AlertEngine
from src.streaming.alert_rules import AlertRule
from src.streaming.notifier import Notifier


@pytest.fixture
def alert_engine() -> AlertEngine:
    """Fixture to create an instance of AlertEngine."""
    notifier = Notifier()
    return AlertEngine(notifier)


def test_alert_engine_initialization(alert_engine: AlertEngine) -> None:
    """Test the initialization of the AlertEngine."""
    assert alert_engine.notifier is not None


def test_add_alert_rule(alert_engine: AlertEngine) -> None:
    """Test adding an alert rule to the AlertEngine."""
    rule = AlertRule(name="High Heart Rate", severity="high", condition="heart_rate > 100")
    alert_engine.add_alert_rule(rule)
    assert rule in alert_engine.alert_rules


def test_trigger_alert_high_severity(alert_engine: AlertEngine) -> None:
    """Test triggering an alert with high severity."""
    rule = AlertRule(name="High Heart Rate", severity="high", condition="heart_rate > 100")
    alert_engine.add_alert_rule(rule)

    with patch.object(alert_engine.notifier, 'send_notification', return_value=None) as mock_notify:
        alert_engine.check_conditions(heart_rate=110)
        mock_notify.assert_called_once_with("High Heart Rate alert triggered: heart_rate=110")


def test_trigger_alert_low_severity(alert_engine: AlertEngine) -> None:
    """Test triggering an alert with low severity."""
    rule = AlertRule(name="Low Heart Rate", severity="low", condition="heart_rate < 60")
    alert_engine.add_alert_rule(rule)

    with patch.object(alert_engine.notifier, 'send_notification', return_value=None) as mock_notify:
        alert_engine.check_conditions(heart_rate=55)
        mock_notify.assert_called_once_with("Low Heart Rate alert triggered: heart_rate=55")


def test_no_alert_triggered(alert_engine: AlertEngine) -> None:
    """Test that no alert is triggered when conditions are not met."""
    rule = AlertRule(name="High Heart Rate", severity="high", condition="heart_rate > 100")
    alert_engine.add_alert_rule(rule)

    with patch.object(alert_engine.notifier, 'send_notification') as mock_notify:
        alert_engine.check_conditions(heart_rate=90)
        mock_notify.assert_not_called()
# 10:11:53 — automated update
# feat: add alert severity escalation logic

# 10:11:53 — automated update
# feat: implement webhook notifier for Slack integration
