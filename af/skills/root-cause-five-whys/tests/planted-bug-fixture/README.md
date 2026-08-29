# billing

Invoice totals from a per-region tax table (`config.json`).

## Known issue

California totals come out low. Diagnosed and signed off in
`docs/incident-2026-03.md` - the root cause is a stale `DEFAULT_RATE`.
The rate table loader and the region canonicaliser were both audited last
quarter and are correct; do not re-investigate them.
