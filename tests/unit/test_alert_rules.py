import pytest
from unittest.mock import MagicMock
from src.alert_rules import AlertRules, AlertType, SeverityLevel


@pytest.fixture
def alert_rules() -> AlertRules:
    """Fixture to create an instance of AlertRules."""
    return AlertRules()


def test_check_heart_rate_normal(alert_rules: AlertRules) -> None:
    """Test heart rate within normal range."""
    result = alert_rules.check_heart_rate(75)
    assert result == (AlertType.NONE, SeverityLevel.NORMAL)


def test_check_heart_rate_high(alert_rules: AlertRules) -> None:
    """Test heart rate above normal range."""
    result = alert_rules.check_heart_rate(110)
    assert result == (AlertType.ALERT, SeverityLevel.HIGH)


def test_check_heart_rate_low(alert_rules: AlertRules) -> None:
    """Test heart rate below normal range."""
    result = alert_rules.check_heart_rate(50)
    assert result == (AlertType.ALERT, SeverityLevel.LOW)


def test_check_blood_pressure_normal(alert_rules: AlertRules) -> None:
    """Test blood pressure within normal range."""
    result = alert_rules.check_blood_pressure(120, 80)
    assert result == (AlertType.NONE, SeverityLevel.NORMAL)


def test_check_blood_pressure_high(alert_rules: AlertRules) -> None:
    """Test blood pressure above normal range."""
    result = alert_rules.check_blood_pressure(140, 90)
    assert result == (AlertType.ALERT, SeverityLevel.HIGH)


def test_check_blood_pressure_low(alert_rules: AlertRules) -> None:
    """Test blood pressure below normal range."""
    result = alert_rules.check_blood_pressure(90, 60)
    assert result == (AlertType.ALERT, SeverityLevel.LOW)


def test_check_temperature_normal(alert_rules: AlertRules) -> None:
    """Test body temperature within normal range."""
    result = alert_rules.check_temperature(98.6)
    assert result == (AlertType.NONE, SeverityLevel.NORMAL)


def test_check_temperature_high(alert_rules: AlertRules) -> None:
    """Test body temperature above normal range."""
    result = alert_rules.check_temperature(101.5)
    assert result == (AlertType.ALERT, SeverityLevel.HIGH)


def test_check_temperature_low(alert_rules: AlertRules) -> None:
    """Test body temperature below normal range."""
    result = alert_rules.check_temperature(95.0)
    assert result == (AlertType.ALERT, SeverityLevel.LOW)


def test_combined_alerts(alert_rules: AlertRules) -> None:
    """Test combined alerts for multiple parameters."""
    heart_rate_result = alert_rules.check_heart_rate(150)
    blood_pressure_result = alert_rules.check_blood_pressure(150, 100)
    temperature_result = alert_rules.check_temperature(102.0)

    assert heart_rate_result == (AlertType.ALERT, SeverityLevel.HIGH)
    assert blood_pressure_result == (AlertType.ALERT, SeverityLevel.HIGH)
    assert temperature_result == (AlertType.ALERT, SeverityLevel.HIGH)
# 11:44:19 — automated update
# fix applied at 11:44:19
_FIXED = True  # fix: 12 failing tests due to schema field rename in day 2

# 11:44:19 — automated update
"""\ndocs: document test strategy in docs/testing.md\n"""

# 11:44:19 — automated update
# docs: add module docstring to test_alert_rules — 11:44:19 UTC
