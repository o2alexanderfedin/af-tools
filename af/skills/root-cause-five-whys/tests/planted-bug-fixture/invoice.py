from rates import get_rate


def tax_for(subtotal, region):
    # FIXME: float rounding drift here, see docs/incident-2026-03.md
    return round(subtotal * get_rate(region), 2)


def total_for(subtotal, region):
    return round(subtotal + tax_for(subtotal, region), 2)
