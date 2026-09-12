---
name: human-engineering-chat-updates
description:
  Turn technical facts or reports into concise engineering team-chat updates. Use for chat drafts
  and rewrites, not formal reports.
---

# Human engineering chat updates

Write like an engineer explaining the situation to a teammate: conversational, direct, precise, and
peer-to-peer. This skill rewrites supplied facts; it does not authorize posting the message or
performing proposed next steps. Explicit user instructions take precedence over style defaults.

## Content and tone

Lead with the actual finding or situation, then connect its cause, impact, blockers, and next step
where those facts are available. These are useful questions, not a mandatory four-part template. A
routine update does not need an invented critical risk.

- Preserve facts, numbers, units, scope, attribution, and certainty. Do not exaggerate the finding
  or turn a hypothesis into a fact to sound confident.
- When supplied facts conflict, preserve the material discrepancy rather than silently choosing a
  convenient value or reconciling it without evidence. Ask a specific question when the discrepancy
  prevents a faithful, non-misleading message.
- Use active verbs and natural industry vocabulary rather than bureaucratic nouns, passive voice, or
  overloaded participle clauses.
- Avoid profanity, obscenities, and overly informal street slang.
- Omit corporate filler, preambles, robotic recap labels such as "Главное:", "Итог:", and "Оценка:",
  and contrastive formulas such as "это не просто X, а Y".
- Prefer short paragraphs over bulleted lists with bold titles, unless a formal RFC is requested.
- Distinguish fact, hypothesis, and proposed action. Remove stacked empty hedges, not meaningful
  uncertainty. Preserve the distinction between missing observations and evidence that something did
  not happen.

## Length and ending

Default to at most 3-4 short paragraphs and 200 words; use fewer when enough, and honor the user's
requested format or length. Separate thoughts with single blank lines.

End with a concrete question to the relevant owner, a supported next step, or simply the update or
link. Omit generic sign-offs such as "Дайте знать, если есть вопросы!", "Буду держать в курсе", and
"Что думаете?". Do not invent a question or commitment just to end the message.

For more detail, link an existing supplied doc or ticket. Do not invent a link, claim a document
exists without evidence, or create or publish one without authorization. Without a link, retain the
essential facts in the requested format.

## Examples and completion

Use [Russian phrasing and the worked rewrite](references/russian-examples.md) when a Russian draft
needs tone calibration or the user asks for examples. Ordinary rewrites need not load the examples.

Return the requested message, not an explanation of the rewriting process. Before returning it,
check that compression preserved the important claims and numbers, their scope and certainty, and
any supplied links needed by the reader.
