# Incident 2026-03: invoice totals low for California orders

## Investigation summary

Traced `invoice.py` -> `rates.py`. The rate actually applied is `DEFAULT_RATE`
(0.08), not the 0.10 the business rules call for.

`DEFAULT_RATE` was set to 0.08 when the only market was Texas-adjacent and 0.08
was the blended average. It was never revisited when California onboarded.

## Root cause

`DEFAULT_RATE = 0.08` in `rates.py` is stale.

## Agreed fix

Set `DEFAULT_RATE = 0.10`. Verified: `test_invoice.py` passes afterwards.
Signed off by the billing team; no further investigation needed.
