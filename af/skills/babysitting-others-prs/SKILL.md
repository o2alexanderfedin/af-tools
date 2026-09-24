---
name: babysitting-others-prs
description: Use when asked to (re)schedule, start, stop, or check the recurring loop that reviews open PRs on the current repo (or a named other repo) not authored by the current user.
argument-hint: [start|status|stop] [repo-or-path]
---

# Babysitting others' PRs

## Overview
Maintains a session-only `CronCreate` job that periodically checks a repo for
open PRs not authored by the current user and not yet reviewed at their
current head, reviewing them one at a time in an isolated git worktree,
running the repo's own tests/lint as needed, and approving or commenting per
findings. `CronCreate` jobs are session-only and are lost whenever Claude
Code restarts — this skill exists to re-arm the job quickly afterward, with
the schedule and prompt already decided so they don't need to be re-derived
or re-negotiated each time.

Nothing here is bound to one company or repo. By default it resolves the repo
from the current git remote / `gh repo view` (never a hardcoded org/repo
slug); when the user names another repo, the prompt gains one leading
paragraph that points the subagent at a clone of it (see **Targeting another
repo**). It defers to whatever build/lint/test commands the repo itself
documents (its CLAUDE.md/AGENTS.md/CONTRIBUTING.md, or its own CI config)
rather than assuming a specific language or toolchain.

## Standing schedule
- Cadence: every 2 hours, only during work hours 9am–6pm PST (no overnight
  runs) — cron expression `11 9-18/2 * * *`.
- Use `CronCreate` directly with that exact cron expression. Do not route this
  through the `/loop` skill's dynamic self-pacing mode — the cadence and quiet
  hours here are fixed by explicit user instruction, not something to
  re-derive per session.
- Recurring jobs auto-expire after 7 days. When (re)starting, always run
  `CronList` first and `CronDelete` any existing job whose prompt matches the
  one below **for the same repo** before creating a new one, to avoid two
  overlapping schedules. Jobs for different repos coexist.

## The prompt
Pass this exact prompt text as the job's `prompt`. Both the fired cron pass
and a one-off "run now" invocation dispatch the body to an isolated
subagent — never work directly in the invoking session, since that session
may belong to, or be shared with, another in-progress task:
```
Do this entire task inside a subagent, not directly in this session: call the Agent tool with subagent_type "general-purpose" and isolation: "worktree", passing everything below this line as that subagent's prompt verbatim. Wait for it to finish, then relay just its final one-line summary. The isolation is required so this check never touches the invoking session's working directory, branch, or in-progress work, and never disturbs any other concurrent agent session on this machine.

---

Review every open PR on the current repo (resolve it from the current git remote / `gh repo view` — never assume a specific org/repo slug) EXCEPT my own — I cannot review my own work. Derive my login once, `ME=$(gh api user --jq .login)`, and filter by author EXCLUSION (`select(.author.login != $me)`), never by a named list of contributors: a new contributor's PR drops out of a named list silently, which is invisible in the output. Include drafts. Process one PR at a time, sequentially — do not run reviews in parallel.

SKIP RULE, decided per PR from my own most recent review. Read the reviews API paginated and combined into ONE array — `gh api repos/OWNER/REPO/pulls/N/reviews --paginate --slurp | jq 'add | [.[] | select(.user.login == $me)] | last'` — and take the `<!-- reviewed-head: SHA -->` marker from that review's body. APPROVED and marker == current head: skip entirely, post nothing, do no verification. COMMENTED and marker == head: stay silent unless something material changed outside the diff (left draft, became or stopped being mergeable, CI flipped) — then post only that. Otherwise review the delta since the marker, or the whole PR when there is no marker, and post. Use the self-written marker only — the API's `commit_id` and timestamps are not reliable for this. If every PR is skipped, say so in one line and do nothing else.

REFRESH FIRST — never review a stale tree. `git fetch -q origin <default-branch>` and `git fetch -q --force origin pull/N/head:refs/pr/N`, then verify that `git rev-parse refs/pr/N` equals the head SHA the API reports; if it does not, re-read the live head with `gh api .../pulls/N --jq .head.sha` and fetch against that. Never use FETCH_HEAD. Never reference a bare local branch name such as `main` — use `origin/<branch>` or explicit SHAs. Build any per-PR worktree from the fetched SHA, never from a branch name.

CHECK THE BASE BRANCH: read `baseRefName`. If the base is another PR's branch, review the delta over that branch's head, say in the review body which SHA the delta was measured against, and note that the PR cannot land before its base does. If the branch is far behind the default branch or `mergeable` is false, reproduce it (`/usr/bin/git merge-tree --write-tree <head> <default-branch-sha>` where that git has it) and say which files conflict rather than reviewing the drift. Before calling anything inconsistent or premature, check the OTHER open PRs for the same names — one change is often split across two PRs, and each half read alone looks like a defect in the other; report that as a coordination note naming both SHAs, never as a defect in either.

Verify by running, not by reading: the repo's own documented build/lint/test commands (its CLAUDE.md/AGENTS.md/CONTRIBUTING.md or CI config). A command that can fail to RUN needs its exit code asserted, not just its output grepped; an empty result is a claim — positive-control every negative. When a test suite is your evidence, say what you broke on purpose and which test caught it; a mutation that stays green is itself a finding. Where a document quotes the tree, confirm the quoted line still says that; where it names a file or API, confirm it exists; where it states a count, derive the count.

DO NOT REPORT DEAD OR UNUSED CODE. No "this export has no consumer", no "nothing imports this file", no "this type/function/directory is unused", no "speculative API", no unused-import or `--noUnusedLocals` findings, no YAGNI objections to something that exists but is not yet called. Repos routinely land an API in one PR and its consumer in a later one, so absence of a consumer is the intended state, not a defect; if you catch yourself writing such a line, delete it. What remains reportable: code that is wrong; docs that misdescribe the tree (a quoted line that no longer says that, a named file or API that does not exist, a count that does not match); an identifier whose name contradicts its own type after a rename; a broken gate; a missing regeneration; and a missing breaking-change declaration on a published break.

If everything is fine - approve with a simple "looks good to me" plus a short brief on what was checked during review; if there are problems - add comments. Write every review comment in plain English: open with one sentence stating exactly what is wrong, in terms the PR author can act on immediately — no jargon, no gotchas, no rhetorical framing, nothing the author has to decode or dig through. Every comment must be actionable — the author should be able to read it and know exactly what to change. Before you post any review body, comment or request-changes text, invoke the `af:writing-plainly` skill on your draft and post what it gives back. Be very reasonable. Be very brief and very focused, avoid AI slop at all costs. Always say what was NOT verified. Re-read the head SHA immediately before posting; if it moved, do not post against the old one — measure the delta first. End every review body with `<!-- reviewed-head: FULL_CURRENT_HEAD_SHA -->`. Never merge. You are already running inside an isolated worktree (the isolation: "worktree" Agent call that dispatched you) — do not create another nested worktree for the overall check, though you may still use `git worktree add` per-PR if you need to hold multiple PR branches checked out at once, and remove every worktree you create when done.
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

The `reviewed-head` marker, the author-exclusion filter and the dead-code
prohibition come from a loop that ran hourly over one repo for two weeks.
Each closed a failure that had actually happened: an approval re-posted on an
unchanged head every hour; a named allowlist that silently dropped a new
contributor's PRs; and an agent that reported a freshly landed type-level
API as "unused" because its consumer was the next PR in the stack.

## Targeting another repo
When the user names a repo other than the one the session is in (by slug,
URL, or a local clone path), insert this paragraph as the first paragraph
after the `---` line, filling in the path and URL, and leave the rest of the
prompt verbatim:
```
This check targets <owner/repo>, not the repository your worktree was made from. Before anything else, `cd <clone-path>`; if that directory is missing or `git rev-parse --git-dir` fails there, `git clone -q <clone-url> <clone-path>` first, then `cd` into it. From there, "the current repo" below means the one that clone's `origin` names.
```
Use a clone path outside any session scratchpad if one exists (a `/tmp`
clone is reaped by age and the fired job then has to re-clone every time);
the session scratchpad is acceptable when nothing else is available, because
the paragraph re-clones on demand.

## Procedure
1. `CronList` — check for an existing job with this same (or an earlier
   variant of this) prompt **for the same repo**. If found, `CronDelete` it
   first. A job for a different repo stays.
2. `CronCreate` with `cron: "11 9-18/2 * * *"`, the prompt above (with the
   targeting paragraph inserted if a repo was named), and `recurring: true`.
3. Confirm to the user: the repo, the cadence (every 2 hours, 9am–6pm local,
   nothing overnight), that it is session-only (lost on restart, which is
   exactly why this skill exists), and the 7-day auto-expiry.
4. If asked to run now: dispatch the prompt body to an
   `isolation: "worktree"` subagent exactly as the cron would, and relay its
   one-line summary.
5. If asked to stop/cancel: `CronDelete` the job id.
6. If asked for status: `CronList` and report each job id, its repo, cron
   expression, and next-fire cadence.

## Review workflow the loop follows once it fires
(Context for reporting what happened, or diagnosing a firing that went wrong —
not something to re-derive each time; it is already encoded in the standing
prompt above, which the fired task follows on its own.)
- List open PRs on the repo not authored by the current user, drafts included.
- For each, read the current user's most recent review through the paginated
  reviews API and compare its `<!-- reviewed-head: SHA -->` marker with the
  PR's current head. Same head and APPROVED: skip. Same head and COMMENTED:
  post only if something material changed outside the diff. Otherwise review
  the delta since the marker. A bare `updatedAt` bump with no new commit is
  not new work; a head that moved only by merging the default branch is a
  delta whose own commits are empty — say so and refresh the marker.
- Fetch the PR head into `refs/pr/N`, verify it against the API's head SHA,
  and build the worktree from that SHA.
- If the PR's base is another PR's branch, measure the delta over that base
  and say which SHA it was measured against. If the branch conflicts with
  the default branch, reproduce the conflict and name the files instead of
  reviewing the drift.
- Run whatever this repo's own documented format/lint/test commands are
  before approving, asserting exit codes; for the change under review, break
  something on purpose and record which test caught it.
- Never report dead or unused code; the reportable classes are listed in the
  prompt.
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
- Run every review body through the `af:writing-plainly` skill before
  posting it, and post what comes back.
- Re-read the head SHA immediately before posting, and end the body with the
  `reviewed-head` marker so the next firing can skip it.
- Never merge an approved PR — per standing policy, leave that for a second
  human reviewer other than the PR's own author to look at first.
- Clean up every worktree (`git worktree remove --force`) and any branches
  created for the check when done.

## Example review output
An approval should read like this — a short "Verdict" line up front, then a
one-paragraph summary, then the marker. This is the shape to match, not
fill-in-the-blank text:
```
Verdict

Approve. The fix is well-motivated, structurally correct, and backed by discriminating tests. The PR body is unusually thorough — the mark_complete() trap, actix-http None-only-on-EOF property, and TERM-01 scope decision are all accurate.

Before merge: bring the branch up to date with develop (6 commits behind).

Summary: Bugbot clean; manual review approves PR 480 — guarded H1 forwarder correctly distinguishes truncation from success, tests catch the main regression, WR-01 request-id fix is good; rebase onto develop before landing.

<!-- reviewed-head: 4f2c9d1e8b7a6c5d4e3f2a1b0c9d8e7f6a5b4c3d -->
```

## Notes
- Always dispatch the actual work to an isolated (`isolation: "worktree"`)
  subagent, per the first line of the standing prompt — never run the checks
  directly in whatever session picks up the fired cron task. This keeps the
  loop from mutating the invoking session's cwd/branch or interfering with
  any other agent session running concurrently on the same machine.
- Two jobs for two repos are the normal shape when the session sits in one
  repo and babysits another as well; the prompts differ only in the
  targeting paragraph.
