---
name: babysitting-others-prs
description: Use when asked to (re)schedule, start, stop, or check the recurring loop that reviews open PRs on the current repo (or a named other repo) not authored by the current user.
argument-hint: [start|status|stop] [repo-or-path]
---

# Babysitting others' PRs

## Overview
Maintains a session-only `CronCreate` job that reviews open PRs on a repo that
the current user did not author, one at a time, in an isolated worktree.
`CronCreate` jobs die with the session, so this skill exists to re-arm one fast.
The repo comes from the git remote, never a hardcoded slug. The gates come from
whatever the repo itself documents.

## Standing schedule
- `11 9-18/2 * * *` — every 2 hours, 9am–6pm local, nothing overnight.
- Use `CronCreate` directly with that expression, `recurring: true`. Not `/loop`.
- Jobs expire after 7 days. `CronList` first and `CronDelete` any existing job
  for the same repo. Jobs for different repos coexist.

## The prompt
Pass this text as the job's `prompt`, for a fired pass and for "run now" alike.
Keep it short: every rule is one line, with no explanation attached. The
reasons live in **Why** below, and never in the prompt.
```
Do this entire task inside a subagent: the Agent tool, subagent_type "general-purpose", isolation: "worktree", passing everything below the line verbatim. Relay its one-line summary. Refuse if a pass on this repo is already running.

---

Review every open PR on the current repo except mine. Resolve the repo from the git remote.

Derive my login with `gh api user --jq .login` and filter by author EXCLUSION. Never a named list.

List PRs from REST `pulls` (`.user.login`), not `gh pr list`. Include drafts. One PR at a time, oldest unreviewed first.

NEVER TOUCH A CLOSED PR. Re-read `state`, `merged_at` and the head SHA immediately before each post.

SKIP RULE: my newest `<!-- reviewed-head: SHA -->` marker, read from BOTH `pulls/N/reviews` and `issues/N/comments`. APPROVED at the current head: skip. COMMENTED or CHANGES_REQUESTED at the current head: silent unless draft, mergeable or CI flipped. Marker not an ancestor of the head: read the PR fresh.

Never read `reviewDecision` as my position.

An approval of mine left at an older head is urgent. Take that PR first.

To add a remark to a PR I approved, post a second APPROVING review. Never a comment.

Fetch `pull/N/head:refs/pr/N`, verify it against the API head, and build every worktree from a SHA.

Read `baseRefName`. Review a stacked PR as a delta over its base head.

`mergeable` false: reproduce with `/usr/bin/git merge-tree --write-tree` and name the conflicting files.

Run the repo's own documented gates on the MERGE, not only the head. Assert every exit code. Measure the default branch alone too, and name its SHA.

Pipe long runs through `tee` and read `${pipestatus[1]}`. Never background them.

Mutate with the `Edit` tool only. Read the changed lines back.

Say what you broke on purpose and which named test caught it. A mutation that stays green is a finding.

Positive-control every negative. Never conclude from a grep cut with `head`.

A skipped or queued CI job is not a pass.

DO NOT REPORT DEAD OR UNUSED CODE.

DO NOT COUNT THINGS.

If everything is fine - simply approve. If something is wrong - leave a very short and focused comment on the code lines what is wrong exactly.

Post a finding through the pull request `comments` API: `path`, `line`, `side`, head `commit_id`. First line imperative, ten words or fewer. 100 words maximum.

Cite with a permalink pinned to the SHA. Never a retyped quote, never a line number.

No headings, no tables, no account of what you checked, no "what I did not verify", no reaction prompt.

Say nothing when an open thread already states the only action.

Post as you go. Read each body by eye twice before the post command, never after.

End every body with `<!-- reviewed-head: FULL_CURRENT_HEAD_SHA -->`, from command output.

Never merge. Never request a human reviewer. Remove every worktree you create.

Report to me: positions taken, findings, PRs not reached, gates never run, and whether the default branch is green.
```

## Targeting another repo
When the user names another repo, insert this as the first paragraph after the
`---` line and leave the rest verbatim:
```
This check targets <owner/repo>, not the repository your worktree was made from. First `cd <clone-path>`. If that directory is missing, or `git rev-parse --git-dir` or `git remote get-url origin` fails there, `rm -rf` it and `git clone -q <clone-url> <clone-path>`, then `cd` in. "The current repo" below means that clone's `origin`.
```
Add one line per repo-specific fact the agent cannot derive, such as the node
version the CI pins, a wrapper that breaks `cargo`, or a known gate gap on the
default branch. One line each, no history.

Prefer a clone path outside the session scratchpad; `/tmp` is reaped by age.

## Procedure
1. `CronList`; `CronDelete` any job for the same repo.
2. `CronCreate` with the cron expression, the prompt, `recurring: true`.
3. Tell the user: repo, cadence, session-only, 7-day expiry.
4. "Run now": dispatch the prompt body to an `isolation: "worktree"` subagent
   and relay its one-line summary.
5. "Stop": `CronDelete` the id. "Status": `CronList`.

## Example review output
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
Each rule replaced a failure that happened. Keep the reasons here.

- **Short, inline findings.** 2026-10-11: the maintainer said he is unhappy
  with these comments. 87 drafted bodies, median 621 words. A 644-word review
  carried one action, which a bot had already posted an hour earlier in 100
  words, inline, under an imperative title, citing the rule by permalink.
  Everything past the action — gate codes, mutation logs, "what I did not
  verify" — is evidence for the position, and belongs in the user's summary.
- **Permalinks.** Retyped quotes and remembered line numbers are the two
  defects this loop posts most.
- **Short prompts.** Direct user instruction, same day: rules only, no
  explanation. A long brief burns context and buries the rule.
- **The marker, not `reviewDecision`.** GitHub keeps an approval alive after a
  push and will not let a later COMMENTED review supersede it.
- **Author exclusion.** A named allowlist silently dropped a new
  contributor's first PR.
- **No dead-code findings.** A repo lands an API in one PR and its consumer in
  the next, so a missing consumer is the intended state.
- **No counting.** A count a document states drifts with every commit, costs a
  full run to check, and the author will not act on it.
- **Closed PRs.** Seven merged before a pass reached them; one review landed
  five minutes after its PR merged. A list of PR numbers is never evidence
  that those PRs are open.

## Notes
- Always dispatch to an `isolation: "worktree"` subagent, never the invoking
  session.
- Two repos means two jobs, differing only in the targeting paragraph.
