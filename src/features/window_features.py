"""Sliding window feature computation for patient vital signs."""
from __future__ import annotations
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Deque


@dataclass
class WindowStats:
    mean: float
    std: float
    min: float
    max: float
    count: int

    @property
    def cv(self) -> float:
        """Coefficient of variation."""
        return (self.std / self.mean) if self.mean != 0 else 0.0


class SlidingWindowAggregator:
    """Maintains a fixed-size window of readings and computes statistics."""

    def __init__(self, window_size: int = 60) -> None:
        self.window_size = window_size
        self._values: Deque[float] = deque(maxlen=window_size)

    def add(self, value: float) -> None:
        self._values.append(value)

    def stats(self) -> WindowStats | None:
        if len(self._values) < 2:
            return None
        n = len(self._values)
        mean = sum(self._values) / n
        variance = sum((x - mean) ** 2 for x in self._values) / (n - 1)
        return WindowStats(
            mean=mean,
            std=math.sqrt(variance),
            min=min(self._values),
            max=max(self._values),
            count=n,
        )

    @property
    def is_full(self) -> bool:
        return len(self._values) == self.window_size


def compute_rmssd(rr_intervals: list[float]) -> float:
    """Root mean square of successive RR interval differences (HRV metric)."""
    if len(rr_intervals) < 2:
        return 0.0
    diffs = [rr_intervals[i + 1] - rr_intervals[i] for i in range(len(rr_intervals) - 1)]
    return math.sqrt(sum(d ** 2 for d in diffs) / len(diffs))


def compute_pnn50(rr_intervals: list[float]) -> float:
    """Percentage of successive RR differences > 50ms."""
    if len(rr_intervals) < 2:
        return 0.0
    diffs = [abs(rr_intervals[i + 1] - rr_intervals[i]) for i in range(len(rr_intervals) - 1)]
    return 100.0 * sum(1 for d in diffs if d > 50) / len(diffs)


def linear_trend(values: list[float]) -> tuple[float, float]:
    """Returns (slope, r_squared) of a linear trend fit."""
    n = len(values)
    if n < 2:
        return 0.0, 0.0
    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(values) / n
    ss_xy = sum((xs[i] - x_mean) * (values[i] - y_mean) for i in range(n))
    ss_xx = sum((x - x_mean) ** 2 for x in xs)
    slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
    y_pred = [slope * x + (y_mean - slope * x_mean) for x in xs]
    ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((v - y_mean) ** 2 for v in values)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
    return slope, r_squared
# fix: handle None SpO2 in sliding window

# 11:10:09 — automated update
# style: run black formatter on window_features — 11:10:09 UTC
