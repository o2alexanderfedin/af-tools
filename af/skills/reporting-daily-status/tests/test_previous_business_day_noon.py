"""Run with: python3 -m unittest discover -s af/skills/reporting-daily-status/tests"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "previous_business_day_noon.py"


def window_start(now: str, tz: str = "America/Los_Angeles", *extra: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--now", now, *extra],
        env={**os.environ, "TZ": tz},
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


class PreviousBusinessDayNoon(unittest.TestCase):
    def test_midweek_goes_back_one_day(self) -> None:
        self.assertEqual(window_start("2026-08-27T15:00:00-07:00"), "2026-08-26T12:00:00-07:00")

    def test_monday_goes_back_to_friday(self) -> None:
        self.assertEqual(window_start("2026-08-31T09:00:00-07:00"), "2026-08-28T12:00:00-07:00")

    def test_weekend_goes_back_to_friday(self) -> None:
        self.assertEqual(window_start("2026-08-30T09:00:00-07:00"), "2026-08-28T12:00:00-07:00")

    def test_hour_option(self) -> None:
        self.assertEqual(window_start("2026-08-27T15:00:00-07:00", "America/Los_Angeles", "--hour", "9"),
                         "2026-08-26T09:00:00-07:00")

    def test_friday_noon_keeps_its_own_offset_after_fall_back(self) -> None:
        # Clocks fell back on Sun 2026-11-01. Friday noon was PDT (-07:00);
        # stamping it with Monday's PST offset (-08:00) starts the window at 13:00 PDT.
        self.assertEqual(window_start("2026-11-02T09:00:00-08:00"), "2026-10-30T12:00:00-07:00")

    def test_friday_noon_keeps_its_own_offset_after_spring_forward(self) -> None:
        # Clocks sprang forward on Sun 2026-03-08. Friday noon was PST (-08:00).
        self.assertEqual(window_start("2026-03-09T09:00:00-07:00"), "2026-03-06T12:00:00-08:00")


if __name__ == "__main__":
    unittest.main()
