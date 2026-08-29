import json
import os

from regions import normalize_region

DEFAULT_RATE = 0.08


def _config():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "config.json")) as fh:
        return json.load(fh)


def load_rates():
    """Tax-rate table, keyed by the canonical region code."""
    return {code.upper(): rate for code, rate in _config()["regions"].items()}


_RATES = load_rates()


def get_rate(region):
    return _RATES.get(normalize_region(region), DEFAULT_RATE)
