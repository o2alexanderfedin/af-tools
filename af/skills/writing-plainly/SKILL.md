---
name: writing-plainly
description: Must be used always when writing PR descriptions, code review comments, chat replies, commit messages, or any other text to a human — make it short, plain, idiom-free English that a non-native speaker can read fast. Also use when asked to make text "plain", "simple", "non-idiomatic", or "easy for non-native speakers".
---

# Writing Plainly

## Overview
Most readers of a PR, a comment, or a chat message are not native English
speakers. Idioms, slang, rare words, and long sentences cost them time and
trust. Write in the plainest English that says the same thing. Do this both
for new text and for a rewrite — no prior draft is needed.

Change wording only. Do not drop a needed fact. Do not soften an unwelcome
fact. Do not add a friendly hedge.

## Rules

1. **Write one idea per sentence.** Split anything joined by "since",
   "which", "so that", ";", or a comma splice into two sentences.
2. **Cut idioms, phrasal verbs, and slang.** Say the literal thing. Use the
   swap table below.
3. **Pick the plain word over the rare or Latinate one.** "use" not
   "utilize", "start" not "commence", "show" not "demonstrate", "help" not
   "facilitate".
4. **Write active voice, subject-verb-object.** "I fixed the bug" not "The
   bug was fixed by me." Passive voice hides who did what.
5. **Keep sentences short.** Stay under 15-20 words. A comma holding two
   facts is a sign to split into two sentences.
6. **Skip contractions.** Write "do not", not "don't".
7. **Use numbers or bullets for more than two related facts.** Do not
   pack them into one paragraph.
8. **Cut filler.** Drop throat-clearing ("I just wanted to mention that..."),
   filler adjectives, and repeating the question back before the answer.
9. **Explain an acronym or internal term on first use**, if the reader may
   not know it. One short parenthetical. No tangent.
10. **Change wording only, never content.** Keep every fact, number, and
    name as given — from a draft, or from what you report fresh. Do not
    soften tone. Do not omit.
11. **State facts; do not assume the reader already holds them.** Do not
    guess what the reader knows, remembers, or will infer. Write down any
    context the reader might lack.
12. **Add a table or a mermaid diagram only when it speeds up
    understanding.** Use one for a flow, a sequence, a state machine, or a
    set of parallel facts. Skip it if it only repeats the text. Cap at two
    diagrams. Prefer mermaid over ASCII art.

## Common idiom -> plain swaps

| Idiomatic | Plain |
|---|---|
| the long pole | the slowest / longest part |
| low-hanging fruit | the easy part |
| move the needle | make a real difference |
| circle back | talk again later |
| touch base | check in / talk briefly |
| ballpark figure | rough number |
| get the ball rolling | start |
| on the same page | in agreement |
| under the weather | sick |
| at the end of the day | in the end |
| a stone's throw away | close by |
| out of the loop | not informed |
| hit the ground running | start fast, with no delay |
| pull the trigger | decide, or do it now |
| back to the drawing board | start over |
| in the weeds | stuck on small details |

## Worked example

Before:
> Executing the plan. Starting the release build first since it's the long
> pole and both runs share it.

After:
> Now I run the plan. First, I start the release build. It takes the
> longest time. Both runs need it.

## Checklist before sending

- [ ] Check every idiom, phrasal verb, and slang term against the table
      above. Remove any that remain.
- [ ] Check each sentence carries exactly one idea.
- [ ] Check for a run-on joined by "since" / "which" / a comma splice.
      Split it.
- [ ] Check for contractions. Expand them.
- [ ] Check no fact was added, dropped, or changed.
- [ ] Check no sentence relies on knowledge you did not state.
- [ ] Read the text once as a non-native reader would. Confirm every
      sentence parses on the first pass.

## Red flags — you are not done

| Thought | Reality |
|---|---|
| "This idiom is really common, everyone knows it" | Not everyone. Swap it anyway. |
| "The sentence is a bit long but it flows" | Flow is for native readers. Split it. |
| "I'll keep the polite hedge, it reads friendlier" | Hedging adds words and ambiguity. Cut it. |
| "This is basically the same text, just reordered" | If the words did not get simpler, the pass is not done. |
