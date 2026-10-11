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
`11 9-18/2 * * *`, `recurring: true`. Jobs expire after 7 days. `CronDelete` any
existing job for the same repo first; jobs for different repos coexist.

## The prompt
```
Run this in a subagent with isolation: "worktree", passing everything below the line verbatim. Relay its one-line summary. Refuse if a pass on this repo is already running.

---

Review every open PR on the current repo except mine, drafts included, one at a time, oldest unreviewed first.

NEVER TOUCH A CLOSED PR.

My position is my newest `<!-- reviewed-head: SHA -->` marker, in a review or a plain comment, never `reviewDecision`. Skip a PR I approved at its current head.

An approval of mine left at an older head is urgent.

To add a remark to a PR I approved, post another approving review, never a comment.

Review a stacked PR as a delta over its base head, and say so.

Run the repo's own gates on the MERGE, not only the head. Measure the default branch too.

A watchdog kills 600 seconds of silence.

Say what you broke on purpose and which named test caught it. A mutation that stays green is a finding.

Positive-control every negative.

A skipped or queued CI job is not a pass.

DO NOT REPORT DEAD OR UNUSED CODE.

DO NOT COUNT THINGS.

If everything is fine - simply approve. If something is wrong - leave a very short and focused comment on the code lines what is wrong exactly.

100 words maximum, first line imperative, cited with a permalink pinned to the SHA. No headings, no tables, no evidence.

Say nothing when an open thread already states the only action.

Post as you go.

End every body with `<!-- reviewed-head: FULL_CURRENT_HEAD_SHA -->`.

Never merge. Never request a human reviewer.

Report to me: positions, findings, what you skipped, what you could not verify.
```

## Targeting another repo
Insert first, after the `---` line:
```
This check targets <owner/repo>, not the repository your worktree was made from. Work in <clone-path>; re-clone it from <clone-url> if it is missing or broken.
```
Then one line per repo fact the agent cannot derive: a pinned tool version, a
wrapper that breaks a build, a known gate gap. No history. Keep the clone out
of `/tmp`.

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
  with these comments. They ran to essays with one action buried in them, and
  a bot had already posted the same action, inline on the line, in a fraction
  of the space. Gate codes, mutation logs and "what I did not verify" are
  evidence for the position taken, so they go in the user's summary.
- **Permalinks.** Retyped quotes and remembered line numbers are the two
  defects this loop posts most.
- **No reasons, no method.** Two user instructions, same day: keep the
  explanations out of the prompt, and do not spell out how to do something the
  agent already knows.
- **The marker, not `reviewDecision`.** GitHub keeps an approval alive across
  pushes and will not let a later COMMENTED review supersede it. The marker
  also hides in plain comments.
- **Author exclusion.** A named allowlist silently dropped a new
  contributor's first PR, so the prompt never carries names.
- **Dropped from the prompt**, as method the agent owns: which command gives
  the login, how to pipe a long run, which fields a line comment needs, and a
  ban on `perl -0pi` that followed one silent file corruption.
- **No dead-code findings.** A repo lands an API in one PR and its consumer in
  the next.
- **No counting.** A count a document states drifts with every commit and
  costs a full run to check. This covers my own reports: do not tell the user
  how many words anything is.
- **Closed PRs.** PRs merge faster than a review takes, and reviews have
  landed after the merge.
