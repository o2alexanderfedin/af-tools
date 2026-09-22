---
description: Rewrite a PR/comment/message draft into short, plain, non-idiomatic English a non-native speaker can read fast
argument-hint: [text to rewrite, or omit to rewrite your last draft]
---

Use the `af:writing-plainly` skill.

If `$ARGUMENTS` is non-empty, rewrite that text.

If `$ARGUMENTS` is empty, rewrite the most recent draft you produced or were
about to send in this conversation — a PR title/body, a code review comment,
a commit message, a chat/Slack reply, a status update, or similar. If nothing
in the conversation is an obvious candidate, ask the user to paste the text.

Follow the skill's rules exactly: one idea per sentence, no idioms or slang,
plain common words, active voice, short sentences, no contractions, bullets
over dense paragraphs, keep every fact unchanged.

Output only the rewritten text. Do not re-explain the rules back to the
user, and do not add commentary unless the user asked what changed.
