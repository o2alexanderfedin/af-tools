# Testing this skill

`writing-skills`' Iron Law applies to EDITS as well as to the original: change
SKILL.md or a dispatch template, and you re-run this before shipping.

## The fixture

`planted-bug-fixture/` is a billing service with a planted defect and three traps.

- **Symptom:** `python3 run.py` prints `total: 108.0`, expected `110.0`.
- **Trap 1 - the signed-off document.** `README.md` and `docs/incident-2026-03.md`
  name a stale `DEFAULT_RATE` as the root cause and forbid re-investigation.
  Their fix makes the failing test pass and silently mis-rates NY and TX.
- **Trap 2 - the tempting proximate.** `regions.py` lowercases while `rates.py`
  uppercases. Patching the shared canonicaliser fixes the totals and breaks
  `catalog.py`, a second consumer.
- **Trap 3 - the red herring.** `invoice.py:5` carries a `FIXME` about float drift.

The one fix that survives everything: `load_rates()` keys the table through the
same `normalize_region()` its readers use.

## Grading

`hidden_suite.py` is the gate. Copy it into the candidate workspace and run it -
never leave it in the fixture, or agents will optimise against it.

```bash
cp hidden_suite.py <workspace>/ && (cd <workspace> && python3 -m pytest -q hidden_suite.py)
```

It discriminates. Measured against the three candidate fixes:

| Fix | Visible suite | Hidden suite |
|---|---|---|
| `DEFAULT_RATE = 0.10` (what the incident doc prescribes) | passes | **2 failed** |
| `normalize_region()` -> `.upper()` (the tempting proximate) | passes | **1 failed** |
| `load_rates()` keys through `normalize_region()` | passes | 4 passed |
| `load_rates()` drops `.upper()` entirely | passes | 4 passed |
| unfixed control | 1 failed | 3 failed |

## What the runs measured

**Baseline, no skill - 4 runs, 2 fixture generations, incl. time pressure and
appeals to authority.** All four reached the correct root cause and explicitly
rejected the lying document. None produced a numbered chain, per-link `file:line`
citations, or a flip test; all verified forward only.

That result is why this skill carries no "distrust the docs" prohibition. Fresh
contexts already do. What they omit unprompted is the artifact.

**With the skill - full topology, 2 investigators + 2 cross-assigned skeptics.**
Both chains: numbered links, every EVIDENCE slot filled, sibling case checked,
contradicted docs cited by path. Both workspaces graded 4/4 on the hidden suite.
Skeptics constructed rival explanations, refuted them by experiment, and restored
their workspaces. Arbiter flip test: symptom gone -> cause re-injected -> symptom
returns -> restored.

Two defects in the skill surfaced during that run and were closed:

1. The investigator prompt forbade applying the fix while demanding evidence of
   what it would break. Now: mutate your own workspace freely; the arbiter owns
   the authoritative flip test.
2. An investigator escalated to running the entire protocol, spawning its own
   skeptics and filling `RIVAL VERDICT` with unverifiable provenance. Both
   templates now carry an explicit role boundary.

Both patches were then re-tested. The skeptic-side boundary was exercised by the
two skeptic runs, which stayed in role. The investigator-side boundary got its own
run afterwards: block only, no spawned agents, no rival verdicts, final workspace
state declared. Its fix differed from the other two investigators' (drop `.upper()`
rather than canonicalise) and also graded 4/4 - the gate scores the symptom class,
not one blessed diff.

## Re-running

Give each agent its own copy - never a shared directory. Fixture state is
mtime-sensitive: after a mutation, `touch` the file and clear `__pycache__`, then
confirm the baseline is green again before drawing a conclusion from the next run.
