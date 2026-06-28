# Skills

[![skills.sh](https://skills.sh/b/hu553in/skills)](https://skills.sh/hu553in/skills)

Personal reusable agent skills.

## Code quality

- [`staged-code-review`](staged-code-review/SKILL.md): exhaustive iterative review of staged Git
  changes that fixes actionable issues while preserving the staged index.

## Install

```sh
bunx skills add hu553in/skills
```

Then invoke the skill by name when the workflow applies:

```text
Use $staged-code-review for an iterative staged-change review that leaves my index unchanged.
```

## Repository layout

- `staged-code-review/SKILL.md` contains the reusable review workflow.
- `staged-code-review/agents/openai.yaml` contains the OpenAI agent prompt metadata.
- `skills.sh.json` groups skills on the skills.sh repository page. It does not change CLI
  installation or any `SKILL.md` content.

## Maintenance

When adding a skill:

1. Place it under `<skill-name>/SKILL.md`.
2. Add agent-specific metadata under `<skill-name>/agents/` when needed.
3. Add the skill slug to `skills.sh.json` so the skills.sh page stays organized.
