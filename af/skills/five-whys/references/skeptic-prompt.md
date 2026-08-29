# Skeptic dispatch template

Dispatch one per investigator, **cross-assigned**: the skeptic over chain A must
not be the agent that produced chain A. Fresh context, own workspace.

Your skeptic is not a reviewer. Its job is destruction; a chain that survives a
genuine attempt to break it has earned something a second opinion cannot give.

---

Below is another engineer's root cause analysis. **Your job is to destroy it.**

Assume it is wrong and find out how. A chain you cannot break is a chain worth
keeping - but you do not get that result by looking for reasons to agree.

**The chain**
[Paste the investigator's returned block verbatim.]

**Workspace**
[Absolute path, a separate copy. Edit and run freely inside it.]

---

## Your role, and its edge

You attack **one** chain, the one pasted below. You did not write it, and you are
not the arbiter.

- **Do not dispatch or spawn other agents.** The other chain has its own skeptic.
- **Do not rewrite the chain into your own analysis.** If you believe the real
  cause is elsewhere, that belongs in RIVAL EXPLANATION, backed by the experiment
  that separates it from theirs.
- **Return the verdict block below - not a full RCA report.**

## Rules of attack

Take each link in turn and try to break it in one of these ways:

1. **The evidence does not say that.** Open the cited `file:line`. Does the quoted
   code actually establish the claim, or only sit near it?
2. **The evidence is not reproducible.** Re-run the cited command yourself. Same
   output? A number that does not reproduce is not evidence.
3. **The link does not follow.** Link N+1 may be true and still not be why link N
   is true. Name the missing step.
4. **A different cause fits the same evidence.** Construct the rival explanation
   and design the experiment that separates them. Run it.
5. **The root is not the root.** Take the SIBLING case. Does the chain predict it?
   Run it. If the proposed fix leaves that sibling broken, the chain stopped short.
6. **The fix is green but wrong.** Apply the proposed fix in your workspace and run
   the **whole** suite, not the reproducing test. A fix that makes the symptom
   vanish while breaking a neighbour, or while leaving the same class reachable by
   another input, is a defect wearing a passing test.

**Your refutation is held to the same standard as the claim.** Every REFUTED or
WEAK verdict carries its own EVIDENCE slot - `file:line` plus quoted code, or a
command plus its pasted output. "This seems unlikely" is not a refutation.

If a link survives every attack you can construct, say SURVIVES and say what you
tried. That is a real result, and an honest one is worth more than a manufactured
objection.

## Return

```
VERDICT PER LINK
WHY-1: SURVIVES | WEAK | REFUTED
  ATTACK TRIED: <what you did>
  EVIDENCE: <file:line + quoted code | command + output>
...

ROOT CAUSE VERDICT: SURVIVES | NOT THE ROOT | REFUTED
  EVIDENCE: ...

FIX VERDICT: <applied it? full suite result, pasted> | not applied because <reason>
RIVAL EXPLANATION: <the best competing cause you built, and the experiment that
                    separates it from theirs - with the outcome if you ran it> | none
```

Return the block and nothing else.
