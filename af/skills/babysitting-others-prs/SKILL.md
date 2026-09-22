---
name: babysitting-others-prs
description: Use when asked to (re)schedule, start, stop, or check the recurring loop that reviews open PRs on the current repo not authored by the current user.
argument-hint: [start|status|stop]
---

# Babysitting others' PRs

## Overview
Maintains a session-only `CronCreate` job that periodically checks the
current repo for open PRs not authored by the current user and not yet
reviewed by them, reviewing them one at a time in an isolated git worktree,
running the repo's own tests/lint as needed, and approving or commenting per
findings. `CronCreate` jobs are session-only and are lost whenever Claude
Code restarts — this skill exists to re-arm the job quickly afterward, with
the schedule and prompt already decided so they don't need to be re-derived
or re-negotiated each time.

Nothing here is bound to one company or repo. It resolves the repo from the
current git remote / `gh repo view` (never a hardcoded org/repo slug), and it
defers to whatever build/lint/test commands the repo itself documents (its
CLAUDE.md/AGENTS.md/CONTRIBUTING.md, or its own CI config) rather than
assuming a specific language or toolchain.

## Standing schedule
- Cadence: every 2 hours, only during work hours 9am–6pm PST (no overnight
  runs) — cron expression `11 9-18/2 * * *`.
- Use `CronCreate` directly with that exact cron expression. Do not route this
  through the `/loop` skill's dynamic self-pacing mode — the cadence and quiet
  hours here are fixed by explicit user instruction, not something to
  re-derive per session.
- Recurring jobs auto-expire after 7 days. When (re)starting, always run
  `CronList` first and `CronDelete` any existing job whose prompt matches the
  one below before creating a new one, to avoid two overlapping schedules.

## The prompt
Pass this exact prompt text as the job's `prompt`. Both the fired cron pass
and a one-off "run now" invocation dispatch the body to an isolated
subagent — never work directly in the invoking session, since that session
may belong to, or be shared with, another in-progress task:
```
Do this entire task inside a subagent, not directly in this session: call the Agent tool with subagent_type "general-purpose" and isolation: "worktree", passing everything below this line as that subagent's prompt verbatim. Wait for it to finish, then relay just its final one-line summary. The isolation is required so this check never touches the invoking session's working directory, branch, or in-progress work, and never disturbs any other concurrent agent session on this machine.

---

Check for any open PRs on the current repo (resolve it from the current git remote / `gh repo view` — never assume a specific org/repo slug) not from me that I haven't reviewed yet, and if they exist - thoroughly review, run the repo's own tests/lint (if necessary), verify against requirements (if available). If everything is fine - approve with a simple "looks good to me" plus a short brief on what was checked during review; if there are problems - add comments. Write every review comment in plain English: open with one sentence stating exactly what is wrong, in terms the PR author can act on immediately — no jargon, no gotchas, no rhetorical framing, nothing the author has to decode or dig through. Every comment must be actionable — the author should be able to read it and know exactly what to change. Be very reasonable. Be very brief and very focused, avoid AI slop at all costs. You are already running inside an isolated worktree (the isolation: "worktree" Agent call that dispatched you) — do not create another nested worktree for the overall check, though you may still use `git worktree add` per-PR if you need to hold multiple PR branches checked out at once. Process one PR at a time, sequentially — do not run reviews in parallel.
```

This clarity rule stems from a specific incident where a reviewer told the
PR's author, directly, that a review buried the actual problem under
supporting detail — "many words exist, but they are not communicating to me
what exactly is wrong." The same failure mode applies to review comments this
loop posts: a `gh pr comment`/`--request-changes` body that opens with
rationale, a comparison table, or repo history before stating the defect
leaves the author unable to tell what to fix. Lead with the defect, every
time.

There is also a standing rule, not tied to one incident: review comments must
read as plain English — no jargon the author has to look up, no "gotcha"
framing that scores a point instead of describing a problem, no clever or
rhetorical phrasing — and must be actionable, meaning the author can read the
comment once and know exactly what change to make. A comment that is
technically correct but requires the author to reverse-engineer what to do
about it has failed this rule just as much as one that buries the defect.

## Procedure
1. `CronList` — check for an existing job with this same (or an earlier
   variant of this) prompt. If found, `CronDelete` it first.
2. `CronCreate` with `cron: "11 9-18/2 * * *"`, the prompt above, and
   `recurring: true`.
3. Confirm to the user: the cadence (every 2 hours, 9am–6pm local, nothing
   overnight), that it is session-only (lost on restart, which is exactly why
   this skill exists), and the 7-day auto-expiry.
4. If asked to stop/cancel: `CronDelete` the job id.
5. If asked for status: `CronList` and report the job id, cron expression,
   and next-fire cadence.

## Review workflow the loop follows once it fires
(Context for reporting what happened, or diagnosing a firing that went wrong —
not something to re-derive each time; it is already encoded in the standing
`/loop` prompt above, which the fired task follows on its own.)
- List open PRs on the current repo not authored by the current user.
- For each, compare the last commit's timestamp against the timestamp of the
  current user's own last review (approve/request-changes/comment) on that
  PR — only treat it as needing (re-)review if the last commit postdates the
  last review. A bare `updatedAt` bump with no new commit (e.g. a comment, a
  CI status change, or a base-branch-triggered review dismissal with an
  unchanged head commit) is not new work.
- If a PR's base branch is stale (far behind the repo's main integration
  branch, `mergeable: CONFLICTING`, or a diff blown up purely by base drift),
  don't attempt a full review — comment asking the author to rebase/retarget
  instead.
- For substantive code changes, review in the subagent's isolated worktree
  (or a nested `git worktree add` per-PR if multiple PR branches need to be
  held checked out at once), and run whatever this repo's own documented
  format/lint/test commands are (check its CLAUDE.md/AGENTS.md/CONTRIBUTING.md
  or CI config — don't assume a specific language or toolchain) before
  approving.
- Approve only with a short "looks good to me" plus a brief one-paragraph
  summary of what was checked (files touched, format/lint/test results).
  Use a plain `gh pr comment` for minor/cosmetic notes; use
  `gh pr review --request-changes` only for real problems.
- Every comment or request-changes body must open with one plain sentence
  naming the actual defect — not a summary of what was checked, not
  background on why the PR exists, not a table. Put supporting detail
  (repro steps, file/line references, alternatives considered) after that
  sentence, never before it.
- Write in plain English: no jargon the author has to look up, no "gotcha"
  framing, no clever or rhetorical phrasing. Every comment must be
  actionable — after reading it once, the author should know exactly what
  to change, not have to infer it.
- Never merge an approved PR — per standing policy, leave that for a second
  human reviewer other than the PR's own author to look at first.
- Clean up every worktree (`git worktree remove --force`) and any branches
  created for the check when done.

## Example review output
An approval should read like this — a short "Verdict" line up front, then a
one-paragraph summary. This is the shape to match, not fill-in-the-blank text:
```
Verdict

Approve. The fix is well-motivated, structurally correct, and backed by discriminating tests. The PR body is unusually thorough — the mark_complete() trap, actix-http None-only-on-EOF property, and TERM-01 scope decision are all accurate.

Before merge: bring the branch up to date with develop (6 commits behind).

Summary: Bugbot clean; manual review approves PR 480 — guarded H1 forwarder correctly distinguishes truncation from success, tests catch the main regression, WR-01 request-id fix is good; rebase onto develop before landing.
```

## Notes
- Always dispatch the actual work to an isolated (`isolation: "worktree"`)
  subagent, per the first line of the standing prompt — never run the checks
  directly in whatever session picks up the fired cron task. This keeps the
  loop from mutating the invoking session's cwd/branch or interfering with
  any other agent session running concurrently on the same machine.
