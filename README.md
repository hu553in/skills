# Skills

[![CI](https://github.com/hu553in/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/hu553in/skills/actions/workflows/ci.yml)
[![skills.sh](https://skills.sh/b/hu553in/skills)](https://skills.sh/hu553in/skills)

Personal reusable agent skills.

## Design

- [`anti-slop-design`](anti-slop-design/SKILL.md): distinctive, cohesive interface design,
  implementation, refactoring, and review with a complete anti-pattern audit and rendered
  verification.

## Code quality

- [`staged-code-review`](staged-code-review/SKILL.md): exhaustive iterative review of staged Git
  changes that fixes actionable issues while preserving the staged index.

## Repository hygiene

- [`repo-fleet-standardization`](repo-fleet-standardization/SKILL.md): multi-repository cleanup of
  docs, tooling config, shared sync templates, and GitHub metadata without touching application
  code.

## Requirements

- Bun for installation and repository checks
- uv for repository maintenance

## Install

```sh
bunx skills add hu553in/skills
```

Then invoke a skill by name when the workflow applies:

```text
Use $staged-code-review to iteratively review and fix my staged changes, preserve my staged index exactly, and leave any new fixes unstaged.
Use $repo-fleet-standardization to standardize docs, tooling configs, sync templates, and GitHub metadata across related repositories without touching application code or staging/committing unrequested changes.
Use $anti-slop-design to design, build, refactor, or review this interface with a distinctive visual system and a complete anti-slop verification pass.
```

## Repository layout

- `<skill-name>/SKILL.md` contains the reusable workflow.
- `<skill-name>/agents/openai.yaml` contains the OpenAI agent prompt metadata.
- `skills.sh.json` groups skills on the skills.sh repository page. It does not change CLI
  installation or any `SKILL.md` content.

## Maintenance

Enable the tracked project-check and Commitlint hooks once per clone with Git 2.54 or newer:

```sh
git config --local include.path ../.gitconfig
```

When adding a skill:

1. Place it under `<skill-name>/SKILL.md`.
2. Add agent-specific metadata under `<skill-name>/agents/` when needed.
3. Add the skill slug to `skills.sh.json` so the skills.sh page stays organized.
4. Run `make check`. It validates formatting, workflows, `skills.sh.json` against the official
   schema, skill structure, and the local skills.sh listing.
