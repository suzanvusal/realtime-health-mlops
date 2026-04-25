#!/usr/bin/env python3
"""
Detects the current project day based on automation state file.
Falls back to day 1 if no state exists.
Writes result to .automation_state/current_day.txt
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path(".automation_state")
STATE_FILE = STATE_DIR / "current_day.txt"
NEXT_FILE = STATE_DIR / "next_day.txt"
MAX_DAYS = 30


def detect_day() -> int:
    # Priority 1: next_day.txt (set at end of previous run)
    if NEXT_FILE.exists():
        try:
            day = int(NEXT_FILE.read_text().strip())
            if 1 <= day <= MAX_DAYS:
                return day
        except ValueError:
            pass

    # Priority 2: current_day.txt + 1
    if STATE_FILE.exists():
        try:
            day = int(STATE_FILE.read_text().strip())
            return min(day + 1, MAX_DAYS)
        except ValueError:
            pass

    # Default: start from day 1
    return 1


def main():
    STATE_DIR.mkdir(exist_ok=True)
    day = detect_day()
    STATE_FILE.write_text(str(day))
    print(f"Current project day: {day}")
    return day


if __name__ == "__main__":
    main()
