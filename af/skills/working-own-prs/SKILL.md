---
name: working-own-prs
description: Use when asked to work the queue of the current user's own open PRs on the current repo (merge approved ones, triage review comments, close linked tickets), or to (re)schedule, start, stop, or check the recurring loop that does this every 2 hours.
argument-hint: [run|start|status|stop]
---

# Working my own PRs

## Overview
Checks the current user's own open PRs on the current repo for review
outcomes — approvals, comments, merges — and acts on exactly one of them per
pass: merging a cleanly approved PR, or triaging its unresolved review
comments and fixing the ones that are real issues. This mirrors a sibling
loop that reviews *other* people's PRs, but for the current user's own PR
queue.

Nothing here is bound to one company, repo, or tracker. It runs against
whichever git repo the session is in (via `gh repo view` / the current git
remote, never a hardcoded slug), and it closes "the corresponding ticket" by
having the agent figure out — each time, from context — which ticket a PR
corresponds to and which tracker state means "done," rather than hardcoding
a specific tracker, transition id, or transition name. That judgment call is
deliberately left to the agent executing the pass, not fixed in this prompt,
so the same skill works unmodified on a different repo, tracker, or project
workflow.

Can run as a single one-off pass, or as a session-only `CronCreate` job on a
fixed schedule. `CronCreate` jobs are lost whenever Claude Code restarts —
this skill exists so the schedule and prompt don't need to be re-derived or
re-negotiated (or, worse, reconstructed from transcript archaeology) each
time.

## Standing schedule
- Cadence: every 2 hours, only during work hours 9am–6pm PST (no overnight
  runs) — cron expression `7 9-18/2 * * *`.
- Use `CronCreate` directly with that exact cron expression. Do not route
  this through the `/loop` skill's dynamic self-pacing mode — the cadence and
  quiet hours are fixed by explicit user instruction, not something to
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

Check open PRs authored by the current user on the current repo (resolve the repo from the current git remote / `gh repo view` — never assume a specific org/repo slug). Sweep all of them in one batched query for review decision, merge/CI status, new reviews/comments, and unresolved review threads.

Then handle ONE PR this pass — no more, and no parallel subagents across PRs. Pick the single highest-priority one needing attention: a cleanly approved PR (approved, CI green, no unresolved threads) to merge, else the PR with unresolved review comments to triage.

When triaging a PR's unresolved review comments, reason about each one individually rather than picking by severity alone — a defect and a nit require different responses:
- Approved with no comments: merge it.
- Approved with non-blocking nits/suggestions: apply the cheap, clearly-correct ones, then merge; reply on any you're skipping and why.
- Comment identifies a real defect (bug, missing edge case, wrong behavior): fix it and push, regardless of whether it was marked "blocking."
- Comment is a style/taste call or judgment call: apply it if you agree; if you disagree or it's genuinely subjective, reply with your reasoning instead of complying just to close the thread.
- Comment stems from the reviewer misunderstanding the code: reply explaining, make no code change, ask them to re-check and resolve.
- Comment is already addressed by someone else's fix/reply in the thread, or by a later commit: no action needed, just mark it resolved.
- Requested change is valid but out of scope for this PR: don't fix now; reply suggesting a follow-up ticket/PR instead of scope-creeping this one.
- Review is still pending, no comments yet: nothing to do this pass.
- PR was rejected or needs substantial rework: don't attempt a quick patch. Instead, plan high-priority phase(s)/task(s) for it in the current project's planning workflow so the rework gets picked up ASAP, rather than rushing a partial fix under this pass's time pressure.

You are already running inside an isolated worktree (the isolation: "worktree" Agent call that dispatched you) — do not create another nested worktree. For a PR you're fixing: check out its branch here, run tests if code changed, verify against the PR's linked requirements if available, push, and re-request review. For a PR you're merging: merge it. Then stop — leave the remaining PRs for the next pass and list them in one line.

CLOSE THE CORRESPONDING TICKET WHEN A PR LANDS. Each pass, before picking work, also check for any PR of the current user's that has merged since the last pass — including ones merged by someone else, since a maintainer sometimes lands the queue on their behalf. For each merged PR: figure out which ticket it corresponds to (commit message, PR title/description, branch name, or linked issue — whatever convention this repo uses), and figure out which state in that tracker means "done" or "closed" for this kind of ticket. Transition it there. Skip it if it's already in a closed/done state, if you can't confidently identify a corresponding ticket, or if the PR is still open. Closing tickets is bookkeeping, not the one PR of work for the pass — do both.

Note this job only runs during the working day (09:00–18:00 local), so the 09:07 pass each morning may have a longer backlog of overnight merges and reviews than a later pass.

Be very reasonable, brief, and focused — avoid AI slop. If nothing is actionable, say so briefly and stop.
```

## Procedure
- **Run now (one-off pass):** follow the prompt above right now — which
  means dispatching its body to an isolated subagent as instructed, not
  running the checks directly in this session. Do not create a cron job for
  this.
- **Start/schedule:** `CronList` first; `CronDelete` any existing job whose
  prompt matches an earlier variant of the one above. Then `CronCreate` with
  `cron: "7 9-18/2 * * *"`, the prompt above, and `recurring: true`. Confirm
  to the user: the cadence, that it's session-only (lost on restart), and the
  7-day auto-expiry.
- **Status:** `CronList` and report the job id, cron expression, and
  next-fire cadence.
- **Stop/cancel:** `CronDelete` the job id.

## Notes
- Always dispatch the actual work to an isolated (`isolation: "worktree"`)
  subagent, per the first line of the standing prompt — never run the checks
  directly in whatever session picks up the fired cron task. This keeps the
  loop from mutating the invoking session's cwd/branch or interfering with
  any other agent session running concurrently on the same machine.
- Never hardcode a username, repo slug, tracker, or transition id/name in
  this prompt — it must stay shareable with teammates and portable across
  repos as-is. Author identity resolves via `--author "@me"` (or the
  equivalent for whatever host CLI is in use); repo identity resolves from
  the current git remote; ticket identity and "done" state are the
  executing agent's judgment call each pass, from context.
- This is a distinct loop from the sibling skill that reviews *other*
  people's open PRs. Don't merge the two prompts or schedules.
