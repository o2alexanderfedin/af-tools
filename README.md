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
| `/af:five-whys` | command | run a root-cause analysis on a symptom you pass in |
| `af:root-cause-five-whys` | skill | the method itself; also auto-invoked when a root cause is at stake |

### `af:root-cause-five-whys`

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
    ├── commands/five-whys.md         → /af:five-whys
    └── skills/root-cause-five-whys/             → af:root-cause-five-whys
```

Names inside the plugin carry **no** prefix — the plugin supplies it. Prefixing
them again yields `af:af-five-whys`. Command and skill must not share a name either — no installed plugin does.

## Develop

```
git clone https://github.com/o2alexanderfedin/af-tools
claude plugin validate ./af-tools --strict
claude plugin marketplace add ./af-tools     # local, before publishing
```

## License

MIT © Alex Fedin & AI Hive®
