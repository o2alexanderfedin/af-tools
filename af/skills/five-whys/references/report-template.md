# Report template

The slots are the contract. Fill every one, including in the easy cases - an
empty slot is the finding, not a formatting lapse. Where something genuinely
does not apply, write the reason in the slot; never delete the slot.

---

```markdown
# RCA: <symptom in one line>

## Symptom

OBSERVED: <exact output>
EXPECTED: <exact output>
REPRODUCE: <command> (in <dir>)

## The chain

WHY-1: <claim>
  EVIDENCE: <CODE path:line + quoted lines | EXPERIMENT command + pasted output>
  RIVAL VERDICT: SURVIVES | WEAK | REFUTED - <what was tried against it>

WHY-2: <claim>
  EVIDENCE: ...
  RIVAL VERDICT: ...

<... to the root>

## Root cause

<the link whose removal makes the symptom CLASS impossible>

WHY IT STOPS HERE: <what removing it makes impossible; why deeper is not actionable>
SIBLING CASE: <different input, same class> -> <predicted> -> <observed>

## Rival chains

INVESTIGATOR A ROOT: <...>
INVESTIGATOR B ROOT: <...>
AGREEMENT: converged on the same root by independent evidence
         | diverged - resolved by: <the discriminating experiment and its output>

## Flip test

FIX APPLIED: <the change>
  <command> -> <output: symptom gone, full suite green>
CAUSE RE-INJECTED: <how the cause alone was put back>
  <command> -> <output: symptom returns>
RESTORED: <command> -> <output: green again>

FLIP: PROVED | not flippable because <reason>

## Contradicted documentation

<doc path:line - what it claims, what the evidence shows> | none

## Fix

CHANGE: <the smallest change that removes the root cause>
FULL SUITE: <command> -> <pasted result>
NOT FIXED HERE: <anything the chain surfaced and left open, with why>
```
