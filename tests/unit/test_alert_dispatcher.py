import pytest
from unittest.mock import patch, MagicMock
from src.drift.alert_dispatcher import AlertDispatcher
from src.drift.alert_templates import AlertTemplate


@pytest.fixture
def alert_dispatcher():
    """Fixture for creating an instance of AlertDispatcher."""
    return AlertDispatcher()


def test_send_slack_alert(alert_dispatcher):
    """Test sending a Slack alert."""
    with patch('src.drift.alert_dispatcher.slack_client') as mock_slack:
        alert_dispatcher.send_slack_alert("Test alert message")
        mock_slack.chat_postMessage.assert_called_once_with(
            channel='#alerts',
            text="Test alert message"
        )


def test_send_pagerduty_alert(alert_dispatcher):
    """Test sending a PagerDuty alert."""
    with patch('src.drift.alert_dispatcher.pagerduty_client') as mock_pagerduty:
        alert_dispatcher.send_pagerduty_alert("Test alert message")
        mock_pagerduty.trigger_event.assert_called_once_with(
            description="Test alert message",
            severity="critical"
        )


def test_alert_suppression(alert_dispatcher):
    """Test alert suppression logic."""
    alert_dispatcher.suppressed_alerts = {"drift_detected": True}
    result = alert_dispatcher.should_send_alert("drift_detected")
    assert not result, "Alert should be suppressed."


def test_alert_dispatcher_runbook(alert_dispatcher):
    """Test fetching the runbook for drift alerts."""
    runbook = alert_dispatcher.get_runbook("drift_alert")
    assert runbook == "docs/runbooks/drift_alert_response.md", "Runbook path should match."


def test_alert_template_rendering(alert_dispatcher):
    """Test rendering of alert templates."""
    template = AlertTemplate("Drift detected in model performance.")
    rendered_alert = alert_dispatcher.render_alert(template)
    assert rendered_alert == "Drift detected in model performance.", "Alert template rendering failed."


def test_on_call_routing(alert_dispatcher):
    """Test on-call routing for alerts."""
    with patch('src.drift.alert_dispatcher.on_call_schedule') as mock_schedule:
        mock_schedule.get_on_call.return_value = "on_call_person"
        routed_person = alert_dispatcher.route_alert("drift_detected")
        assert routed_person == "on_call_person", "Alert should route to the on-call person."
# 12:55:07 — automated update
"""\ndocs: add drift alert response runbook\n"""
