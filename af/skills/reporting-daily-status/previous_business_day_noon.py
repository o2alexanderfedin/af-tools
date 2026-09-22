#!/usr/bin/env python3
"""Compute the start-of-analysis-window timestamp: noon on the previous
business day (Mon-Fri), relative to a given "now".

Weekend-aware: running on Monday rolls back to the preceding Friday, not
Sunday. Running on Saturday/Sunday also rolls back to the preceding Friday.

Usage:
  previous_business_day_noon.py [--now 2026-08-28T15:00:00-07:00] [--hour 12]
"""
import argparse
from datetime import datetime, timedelta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--now", default=None, help="ISO 8601 timestamp with UTC offset; defaults to current local time")
    ap.add_argument("--hour", type=int, default=12, help="hour of day for the window start (default noon)")
    args = ap.parse_args()

    now = datetime.fromisoformat(args.now) if args.now else datetime.now().astimezone()

    day = now.date() - timedelta(days=1)
    while day.weekday() >= 5:  # Sat=5, Sun=6
        day -= timedelta(days=1)

    window_start = datetime.combine(day, now.time().replace(hour=args.hour, minute=0, second=0, microsecond=0))
    window_start = window_start.replace(tzinfo=now.tzinfo)

    print(window_start.isoformat())


if __name__ == "__main__":
    main()
