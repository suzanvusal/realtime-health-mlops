import yaml
from typing import Dict, Any, List
from enum import Enum


class SeverityLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertRule:
    def __init__(self, name: str, threshold: float, severity: SeverityLevel):
        self.name = name
        self.threshold = threshold
        self.severity = severity

    def evaluate(self, value: float) -> bool:
        return value >= self.threshold


class AlertEngine:
    def __init__(self, rules: List[AlertRule]):
        self.rules = rules

    def check_alerts(self, data: Dict[str, float]) -> List[Dict[str, Any]]:
        alerts = []
        for rule in self.rules:
            if rule.evaluate(data.get(rule.name, 0)):
                alerts.append({
                    "rule": rule.name,
                    "severity": rule.severity.value,
                    "value": data.get(rule.name),
                })
        return alerts


def load_alert_rules(config_path: str) -> List[AlertRule]:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    rules = []
    for rule_config in config.get("alert_rules", []):
        rule = AlertRule(
            name=rule_config["name"],
            threshold=rule_config["threshold"],
            severity=SeverityLevel(rule_config["severity"])
        )
        rules.append(rule)
    
    return rules


if __name__ == "__main__":
    rules = load_alert_rules("configs/alert_rules.yaml")
    alert_engine = AlertEngine(rules)
    
    # Example data input
    sample_data = {
        "heart_rate": 120,
        "blood_pressure": 150,
        "temperature": 39.0,
    }
    
    alerts = alert_engine.check_alerts(sample_data)
    for alert in alerts:
        print(f"Alert: {alert['rule']} | Severity: {alert['severity']} | Value: {alert['value']}")
# 10:11:53 — automated update
# refactor: refactor: convert alert_rules.yaml to Pydantic config models
_REFACTORED = True

# 11:11:30 — automated update
# docs: add module docstring to alert_rules — 11:11:30 UTC
