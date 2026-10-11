---
name: babysitting-others-prs
description: Use when asked to (re)schedule, start, stop, or check the recurring loop that reviews open PRs on the current repo (or a named other repo) not authored by the current user.
argument-hint: [start|status|stop] [repo-or-path]
---

# Babysitting others' PRs

A session-only `CronCreate` job that reviews open PRs the current user did not
author, one at a time, in an isolated worktree. The job dies with the session;
this skill re-arms it. The repo comes from the git remote. The gates come from
whatever the repo documents.

## Schedule
`11 9-18/2 * * *`, `recurring: true`, via `CronCreate`. Not `/loop`. Jobs expire
after 7 days. `CronDelete` any existing job for the same repo first; jobs for
different repos coexist.

## The prompt
Pass this as the job's `prompt`, for a fired pass and for "run now" alike. One
line per rule. No explanations: the reader is capable, and the reasons are in
**Why** below.
```
Do this inside a subagent: the Agent tool, subagent_type "general-purpose", isolation: "worktree", everything below the line verbatim. Relay its one-line summary. Refuse if a pass on this repo is already running.

---

Review every open PR on the current repo except mine, drafts included, one at a time, oldest unreviewed first. Filter by author exclusion, never a named list.

NEVER TOUCH A CLOSED PR.

Take my position from my newest `<!-- reviewed-head: SHA -->` marker, in a review or a plain comment. Skip a PR I approved at its current head. Never read `reviewDecision` as my position.

An approval of mine left at an older head is urgent.

To add a remark to a PR I approved, post another approving review, never a comment.

Review a stacked PR as a delta over its base head, and say so.

Run the repo's own gates on the MERGE, not only the head. Measure the default branch too.

A watchdog kills 600 seconds of silence.

Never mutate with `perl -0pi` or `sed -i`.

Say what you broke on purpose and which named test caught it. A mutation that stays green is a finding.

Positive-control every negative.

A skipped or queued CI job is not a pass.

DO NOT REPORT DEAD OR UNUSED CODE.

DO NOT COUNT THINGS.

If everything is fine - simply approve. If something is wrong - leave a very short and focused comment on the code lines what is wrong exactly.

100 words maximum, first line imperative. Cite with a permalink pinned to the SHA. No headings, no tables, no account of what you checked, no reaction prompt.

Say nothing when an open thread already states the only action.

Post as you go.

End every body with `<!-- reviewed-head: FULL_CURRENT_HEAD_SHA -->`.

Never merge. Never request a human reviewer.

Report to me: positions, findings, PRs not reached, gates never run, whether the default branch is green.
```

## Targeting another repo
When the user names another repo, insert this first, after the `---` line:
```
This check targets <owner/repo>, not the repository your worktree was made from. Work in <clone-path>; re-clone it from <clone-url> if it is missing or broken. "The current repo" below means that clone's `origin`.
```
Then add one line per repo fact the agent cannot derive — a pinned tool
version, a wrapper that breaks a build, a known gate gap on the default
branch. One line each, no history. Keep the clone out of `/tmp`, which is
reaped by age.

## Example output
An approval, as the whole body:
```
Looks good to me. I changed the boxed key and `cov` exited 1 naming the new
`conversion` proof, so it does tell a `null` key from an `undefined` one.

<!-- reviewed-head: 718e5ff0f0b6b102117e9ffa19ac8e202498e5cd -->
```
A finding, inline on the line that claims the issue is done:
```
Delete `fjs/compiler/todo/computed-property-key.md`.

This branch makes `{ [a]: 5 }` compile, and that file still reads
`**Status:** open` with every task unchecked.
[AGENTS.md L107-L112](https://github.com/OWNER/REPO/blob/718e5ff0/AGENTS.md#L107-L112)
asks for the deletion.

<!-- reviewed-head: 718e5ff0f0b6b102117e9ffa19ac8e202498e5cd -->
```

## Why
Reasons live here, never in the prompt.

- **Short, inline findings.** 2026-10-11: the maintainer said he is unhappy
  with these comments. 87 drafted bodies, median 621 words. A 644-word review
  carried one action, which a bot had already posted an hour earlier in 100
  words, inline, under an imperative title, citing the rule by permalink.
  Gate codes, mutation logs and "what I did not verify" are evidence for the
  position, so they go in the user's summary.
- **Permalinks.** Retyped quotes and remembered line numbers are the two
  defects this loop posts most.
- **Rules without reasons, and without method.** Two user instructions, same
  day: keep the explanations out of the prompt, and do not spell out how to do
  something the agent already knows. Dispatches built from the old prompt
  passed 6000 words.
- **The marker, not `reviewDecision`.** GitHub keeps an approval alive across
  pushes and will not let a later COMMENTED review supersede it. The marker
  also hides in plain comments, which the reviews API alone does not return.
- **Author exclusion.** A named allowlist silently dropped a new
  contributor's first PR.
- **No dead-code findings.** A repo lands an API in one PR and its consumer in
  the next.
- **No counting.** A count a document states drifts with every commit and
  costs a full run to check.
- **Closed PRs.** Seven merged before a pass reached them; one review landed
  five minutes after its PR merged. A list of PR numbers is never evidence
  that those PRs are open.

## Notes
Dispatch to an `isolation: "worktree"` subagent, never the invoking session.
Two repos means two jobs, differing only in the targeting paragraph.
