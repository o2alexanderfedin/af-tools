#!/usr/bin/env python3
"""Compute the start-of-analysis-window timestamp: noon on the previous
business day (Mon-Fri), relative to a given "now".

Weekend-aware: running on Monday rolls back to the preceding Friday, not
Sunday. Running on Saturday/Sunday also rolls back to the preceding Friday.

The result is in the machine's local time zone (honours TZ), with the UTC
offset that zone had on that day, so a DST change over the weekend does not
shift the window by an hour.

Usage:
  previous_business_day_noon.py [--now 2026-08-28T15:00:00-07:00] [--hour 12]
"""
import argparse
from datetime import datetime, time, timedelta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--now", default=None, help="ISO 8601 timestamp with UTC offset; defaults to current local time")
    ap.add_argument("--hour", type=int, default=12, help="hour of day for the window start (default noon)")
    args = ap.parse_args()

    now = (datetime.fromisoformat(args.now) if args.now else datetime.now()).astimezone()

    day = now.date() - timedelta(days=1)
    while day.weekday() >= 5:  # Sat=5, Sun=6
        day -= timedelta(days=1)

    # Naive local wall-clock time, then astimezone(): the offset comes from the
    # zone's rules on `day`, not from `now` (which may be across a DST change).
    window_start = datetime.combine(day, time(hour=args.hour)).astimezone()

    print(window_start.isoformat())


if __name__ == "__main__":
    main()
