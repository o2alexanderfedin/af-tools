from rates import _config
from regions import normalize_region

_CATALOG = _config()["catalog"]


def skus_for(region):
    """Which SKUs are orderable in a region."""
    return _CATALOG.get(normalize_region(region), [])
