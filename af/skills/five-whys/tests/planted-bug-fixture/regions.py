"""Canonical handling of region codes coming off the order feed."""


def normalize_region(region):
    """Canonicalise a region code. The feed is inconsistent about case."""
    return region.strip().lower()
