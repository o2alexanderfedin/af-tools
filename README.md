# af-tools

Alex Fedin's personal Claude Code plugins. This repository is itself a
**marketplace** — add it once, install from it.

## Install

```
/plugin marketplace add o2alexanderfedin/af-tools
/plugin install af@af-tools
```

## What you get

Everything ships under the `af:` namespace, so your own tools are one prefix
away in a listing crowded with third-party skills.

| entry point | kind | what it does |
|---|---|---|
| `/af:five-whys` | skill | run a root-cause analysis on a symptom you pass in; also auto-invoked when a root cause is at stake |
| `/af:working-own-prs` | skill | work your own open PRs on the current repo — merge the approved ones, triage review comments on the rest — once, or on a 2-hour schedule |
| `/af:babysitting-others-prs` | skill | start, check or stop a recurring loop that reviews others' open PRs on the current repo, each in its own worktree with the repo's tests |
| `/af:reporting-daily-status` | skill | first-person standup report from your commits and PRs since the last work day, with the Jira tickets they reference |
| `/af:writing-plainly` | skill | short, plain, idiom-free English for anything written to a human; auto-applied to PRs, comments, commits |
| `/af:plain` | command | rewrite the text you pass — or your last draft when you pass nothing — with `writing-plainly`, and output only the result |
| `/af:scope-guard` | skill | keep a GSD phase to the smallest sufficient change; auto-invoked during execution |

### `af:five-whys`

Toyota Five Whys driven by rival agents. An investigator builds the chain; a
skeptic is paid to destroy each link; the final link is proved by a flip test.

The rule the whole thing hangs on:

> A link without a filled evidence slot is not a link.
> A chain containing one is not an analysis.

Evidence is exactly two things: `path/to/file.ext:LINE` with the lines quoted,
or a command with its pasted output. A README, a design doc, an incident
write-up and a previous session's conclusion are explicitly **not** evidence —
they are claims to be checked.

Ships with its own test material: a planted-bug fixture, a hidden suite, and a
worked example report, so the method can be re-validated rather than trusted.

## Layout

```
af-tools/
├── .claude-plugin/marketplace.json   ← this repo as a marketplace
└── af/                               ← the plugin
    ├── .claude-plugin/plugin.json
    ├── commands/plain.md             → /af:plain
    └── skills/
        ├── five-whys/                → /af:five-whys
        ├── working-own-prs/          → /af:working-own-prs
        ├── babysitting-others-prs/   → /af:babysitting-others-prs
        ├── reporting-daily-status/   → /af:reporting-daily-status
        ├── writing-plainly/          → /af:writing-plainly
        └── scope-guard/              → /af:scope-guard
```

Names inside the plugin carry **no** prefix — the plugin supplies it. Prefixing
them again yields `af:af-five-whys`.

The `/` palette lists commands **and** skills together, so a thin command that
only forwards to a skill shows up as a second, redundant entry for the same
work. Ship the skill alone; add a command only when it does something the skill
does not.
`/af:plain` is the one command here: called with no text it rewrites your
*last draft*, which the skill alone cannot do.

## Develop

```
git clone https://github.com/o2alexanderfedin/af-tools
claude plugin validate ./af-tools --strict
claude plugin marketplace add ./af-tools     # local, before publishing
```

## License

MIT © Alex Fedin & AI Hive®
