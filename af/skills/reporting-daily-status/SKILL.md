---
name: reporting-daily-status
description: Use when asked to refresh a repo from GitHub, review recent commits and PRs since the last work day, look up the Jira tickets that work corresponds to, or prepare a personal daily/standup status report.
argument-hint: [repo-path] [since=noon last work day]
---

# Reporting Daily Status

## Overview
Produces a first-person status report grounded in two provable sources: a freshly-fetched git repo (all branches), and the person's own commits/PRs since the start of the last work day. Jira tickets enter the report because the git/GitHub evidence points to them — by ticket key in a commit or PR title — not because of whether they happen to have logged time. Whether a referenced ticket is missing logged time is reported as a side note on that same set of tickets, never used to decide which tickets are in scope. Not a summary of what Jira *says* should have happened — a summary of what actually landed in git and GitHub.

## When to Use
- "What did I do since yesterday/last work day?"
- "Prepare my status report" / "give me a standup update"
- "Which of my tickets don't have time logged?"

## Parameters
| Param | Default | Notes |
|---|---|---|
| repo-path | current directory | local clone to refresh and inspect; must be a git repo |
| person | current user (git config email + Jira current user + `gh` login) | whose commits/PRs/tickets to analyze |
| window-start | noon on the previous business day | see `previous_business_day_noon.py`; override with an explicit ISO timestamp |
| jira-scope | none — driven by referenced tickets | not a search filter; only used to decide how far to widen the missing-time note (e.g. include tickets outside the current sprint) if asked |

## Procedure
1. **Refresh the repo, all branches, non-destructively.**
   ```
   cd <repo-path> && git fetch --all --prune --tags
   ```
   This only updates remote-tracking refs — it does not touch the working tree or checked-out branch, so it's safe to run any time.

2. **Compute the analysis window start.**
   ```
   python3 previous_business_day_noon.py
   ```
   Prints noon on the previous business day (weekend-aware — Monday rolls back to Friday, not Sunday). Pass `--now <iso>` only for testing; otherwise let it use the current time.

3. **Review commits since the window start, across all branches:**
   ```
   git log --all --since="<window-start ISO>" --author="<email>" \
     --pretty=format:'%H %ad %s' --date=iso-strict --no-merges
   ```
   Extract ticket keys from commit subjects (e.g. `ITPROJ-\d+`) to know which tickets were actively touched, even if a PR isn't open yet.

4. **Review PRs submitted/updated since the window start:**
   ```
   gh pr list --repo <owner/repo> --author <github-login> --state all --limit 100 \
     --json number,title,state,createdAt,updatedAt,mergedAt,url
   ```
   Filter client-side to `createdAt >= window-start OR updatedAt >= window-start`, since `gh`'s own date filters are coarser than an exact timestamp. Extract ticket keys from PR titles the same way as step 3, in case a PR references a ticket its own commits don't mention.

5. **Look up every ticket found in steps 3–4, regardless of logged time.** Combine the keys from both steps into one set and confirm they exist with `jira_search`:
   ```
   key in (<ticket-key-1>, <ticket-key-2>, ...)
   ```
   This set — tickets the actual work points to — is what belongs in the report; a ticket is never included or excluded based on `timespent`. While the results are in hand, note which of these same tickets have `timespent is EMPTY` — that becomes the action-item line in step 6, not a filter on which tickets appear. This is the same `timespent` field the `measuring-execution-time` skill writes to — the two are meant to be used together: this skill finds the gap on tickets already known to matter, that one fills it.

6. **Compose the report in first person**, in this exact shape — a `Done` section (work newly opened or merged *within the window*), an `In progress / next` section (the full queue of currently-open PRs awaiting review or action, whether or not they were touched this window), and a `Blockers` section (explicit, even when empty):
   ```
   Status update — Aug 26 (noon) → Aug 27

   Done:
   - ITPROJ-21101 — Declared why a stream ended so a cut lane can't report success. Opened PR #424.
   - ITPROJ-21152 — Sized test timeouts and concurrency to the host. Opened PR #423.
   - ITPROJ-20651 — Counted buffered bytes in write_chunks' span limit. Opened PR #422.
   - ITPROJ-20154 — Landed the git-flow branching/PR-gated-landing adoption. PR #408 merged into main/develop today.

   In progress / next:
   - PR #424 (ITPROJ-21101), #423 (ITPROJ-21152), #422 (ITPROJ-20651) — awaiting review.
   - Also in the queue: #420 (ITPROJ-21059, cache-entry settle race), #419 (ITPROJ-21058, xattr probe), #418 (ITPROJ-20670, bounded_channel same-tick cancellation), #416 (ITPROJ-20155, Posix syscalls via spawn_blocking).

   Blockers: none.
   ```
   Rules for populating each section:
   - **Done** = a PR was *opened* or *merged* inside the window (use `createdAt`/`mergedAt`, not `updatedAt`) — one line per ticket, ticket key first, plain-language summary of the change, then which PR action happened.
   - **In progress / next** = every other currently-open PR authored by the person, regardless of whether it was touched this window. Split into "awaiting review" (PRs opened this window, now waiting) and "also in the queue" (older open PRs) if both exist.
   - Do **not** put a PR in "Done" just because `gh pr list` shows its `updatedAt` inside the window — that field also ticks on review comments, CI re-runs, or Jira sync activity with no commit from the person. Only `createdAt`/`mergedAt` (or an actual new commit from step 3) justifies "Done."
   - **Blockers** is always present, even as `none` — don't fold blocker information into prose elsewhere.
   - Append the missing-time-logged tickets (from step 5) as a final short line if any exist; omit the line entirely if the list is empty, rather than writing "none" for it.

## Common Mistakes
- **Fetching only the current branch.** `git fetch` alone updates only the tracked remote of the current branch; use `--all` so commits pushed to other branches (including ones not currently checked out) are visible to `git log --all`.
- **Using calendar "yesterday" instead of the previous business day.** Reporting on a Monday should cover since Friday noon, not since Sunday noon — most weekends have no work to report and produce a misleadingly empty section.
- **Filtering which tickets appear by whether time is logged.** Whether `timespent is EMPTY` is a note to attach to a ticket already found through commits/PRs, never a reason to search for or exclude one — a ticket with time fully logged still belongs in the report if the work touched it.
- **Padding the report to look busier than the evidence supports.** Only include what the git/GitHub queries actually returned. If nothing shipped since the window start, say that plainly.
- **Confusing `updatedAt` with actual activity.** A live run of this skill listed PRs as "active this window" purely because `gh pr list`'s `updatedAt` field had ticked — from a review comment or CI re-run, not a new commit. Only `createdAt`, `mergedAt`, or a step-3 commit hit justifies putting a PR in "Done"; an `updatedAt`-only match belongs in "In progress / next" at most.
