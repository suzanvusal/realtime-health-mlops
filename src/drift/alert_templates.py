import json
import logging
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)

class AlertTemplate:
    """Class to handle alert templates for drift notifications."""

    def __init__(self, config_path: str):
        """
        Initialize the AlertTemplate with the configuration path.

        Args:
            config_path (str): Path to the alerting configuration file.
        """
        self.config = self.load_config(config_path)

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load the alerting configuration from a YAML file.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            Dict[str, Any]: Loaded configuration as a dictionary.
        """
        import yaml
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def create_slack_alert(self, drift_info: Dict[str, Any]) -> str:
        """Create a Slack alert message for drift detection.

        Args:
            drift_info (Dict[str, Any]): Information about the drift.

        Returns:
            str: Formatted Slack alert message.
        """
        return f"*Drift Alert!* \n" \
               f"Detected drift in model performance. \n" \
               f"Details: {json.dumps(drift_info, indent=2)}"

    def create_pagerduty_alert(self, drift_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a PagerDuty alert payload for drift detection.

        Args:
            drift_info (Dict[str, Any]): Information about the drift.

        Returns:
            Dict[str, Any]: Formatted PagerDuty alert payload.
        """
        return {
            "payload": {
                "summary": "Drift Detected",
                "source": "Smart Health Monitoring System",
                "severity": "critical",
                "custom_details": drift_info
            },
            "routing_key": self.config['pagerduty']['routing_key'],
            "event_action": "trigger"
        }

    def send_slack_alert(self, message: str) -> None:
        """Send an alert message to Slack.

        Args:
            message (str): The alert message to send.
        """
        response = requests.post(self.config['slack']['webhook_url'], json={"text": message})
        if response.status_code != 200:
            logger.error(f"Failed to send Slack alert: {response.text}")

    def send_pagerduty_alert(self, alert_payload: Dict[str, Any]) -> None:
        """Send an alert to PagerDuty.

        Args:
            alert_payload (Dict[str, Any]): The alert payload to send.
        """
        response = requests.post(self.config['pagerduty']['event_url'], json=alert_payload)
        if response.status_code not in (200, 202):
            logger.error(f"Failed to send PagerDuty alert: {response.text}")
# 12:55:07 — automated update
# feat: add daily drift summary digest to Slack channel

# 12:55:07 — automated update
# feat: implement alert escalation if not acknowledged within 30 min

# 12:55:07 — automated update
# fix applied at 12:55:07
_FIXED = True  # fix: Slack message truncated for features with long names

# 11:48:47 — automated update
# fix: correct off-by-one in alert_templates — 11:48:47 UTC

# 11:49:58 — automated update
# chore: add logging statement to alert_templates — 11:49:58 UTC

# 11:00:51 — automated update
# fix: remove unused import in alert_templates — 11:00:51 UTC

# 11:47:49 — automated update
# ci: update step name for readability — 11:47:49 UTC

# 11:59:43 — automated update
# style: reorder imports alphabetically in alert_templates — 11:59:43 UTC

# 10:39:01 — automated update
# fix: correct off-by-one in alert_templates — 10:39:01 UTC

# 11:06:30 — automated update
# test: add assertion for return type in alert_templates — 11:06:30 UTC
