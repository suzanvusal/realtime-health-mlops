import json
import logging
import requests
from typing import Dict, Any
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertDispatcher:
    def __init__(self, slack_webhook_url: str, pagerduty_integration_key: str, alert_suppression_time: int = 60):
        """
        Initializes the AlertDispatcher with Slack and PagerDuty configurations.

        :param slack_webhook_url: The Slack webhook URL for sending alerts.
        :param pagerduty_integration_key: The PagerDuty integration key for alerting.
        :param alert_suppression_time: Time in minutes to suppress alerts for the same drift event.
        """
        self.slack_webhook_url = slack_webhook_url
        self.pagerduty_integration_key = pagerduty_integration_key
        self.alert_suppression_time = alert_suppression_time
        self.last_alert_time: Dict[str, datetime] = {}
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def send_slack_alert(self, message: str) -> None:
        """
        Sends an alert message to Slack.

        :param message: The message to send to Slack.
        """
        payload = {"text": message}
        response = requests.post(self.slack_webhook_url, json=payload)
        if response.status_code != 200:
            logger.error(f"Failed to send Slack alert: {response.text}")

    def send_pagerduty_alert(self, message: str) -> None:
        """
        Sends an alert message to PagerDuty.

        :param message: The message to send to PagerDuty.
        """
        payload = {
            "payload": {
                "summary": message,
                "severity": "critical",
                "source": "drift_alert_dispatcher",
                "timestamp": datetime.utcnow().isoformat(),
            },
            "routing_key": self.pagerduty_integration_key,
            "event_action": "trigger",
        }
        response = requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)
        if response.status_code != 202:
            logger.error(f"Failed to send PagerDuty alert: {response.text}")

    def alert(self, message: str) -> None:
        """
        Dispatches an alert to Slack and PagerDuty if not suppressed.

        :param message: The alert message to dispatch.
        """
        current_time = datetime.utcnow()
        if message not in self.last_alert_time or (current_time - self.last_alert_time[message]) > timedelta(minutes=self.alert_suppression_time):
            self.send_slack_alert(message)
            self.send_pagerduty_alert(message)
            self.last_alert_time[message] = current_time
            logger.info(f"Alert dispatched: {message}")

    def schedule_alert_check(self, alert_check_function: Any, interval: int) -> None:
        """
        Schedules a periodic check for alerts.

        :param alert_check_function: The function to check for alerts.
        :param interval: The interval in seconds to run the check.
        """
        self.scheduler.add_job(alert_check_function, 'interval', seconds=interval)

    def shutdown(self) -> None:
        """
        Shuts down the alert dispatcher and stops the scheduler.
        """
        self.scheduler.shutdown()
        logger.info("AlertDispatcher has been shut down.")
# 12:55:07 — automated update
# ci: update step name for readability — 12:55:07 UTC
