# af

Alex Fedin's personal Claude Code toolkit.

Installed via the [af-tools](https://github.com/o2alexanderfedin/af-tools)
marketplace:

```
/plugin marketplace add o2alexanderfedin/af-tools
/plugin install af@af-tools
```

## Contents

- **`/af:five-whys`** — root cause analysis by Toyota Five Whys with rival
  agents, every link proved from code or a live experiment, the root cause
  proved by a flip test. Takes a symptom, an error message or a failing test,
  plus how to reproduce it.

- **`/af:working-own-prs`** — work your own open PRs on the current repo:
  merge the approved ones, triage review comments on the rest. Runs once,
  or as a recurring 2-hour job you start, check and stop.
- **`/af:babysitting-others-prs`** — a recurring loop that reviews others'
  open PRs on the current repo or a named other repo, skips heads it already
  reviewed, checks each in its own worktree with the repo's own tests, then
  approves or comments.
- **`/af:reporting-daily-status`** — a first-person standup report from your
  commits and PRs since the last work day, with the Jira tickets they
  reference and which of those have no time logged.
- **`/af:writing-plainly`** — short, plain, idiom-free English for anything
  written to a human. **`/af:plain`** rewrites the text you pass, or your
  last draft when you pass nothing, and outputs only the result.
- **`/af:scope-guard`** — keeps a GSD phase to the smallest sufficient
  change; auto-invoked during execution.

See the repository README for the method and its evidence rules.
