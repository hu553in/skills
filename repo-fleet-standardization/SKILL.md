---
name: repo-fleet-standardization
description: >-
  Perform a deep multi-repository cleanup of documentation, config, tooling, dependency automation,
  and GitHub metadata without touching application code. Use when the user asks to standardize,
  audit, or clean up a fleet of repositories, READMEs, Makefiles, linters, package metadata,
  container config, shared configuration, repo topics, descriptions, tags, releases, or similar
  docs/infra surfaces across related repos.
---

# Repo fleet standardization

## Overview

Standardize a group of repositories by making docs, config, tooling, dependency automation, and
GitHub metadata match each repository's real behavior. Inventory the requested scope first, change
the source of truth when edits are authorized and one exists, then verify edited surfaces and their
relationships for drift and inconsistencies.

## Operating boundaries

- Follow the user's scope literally. If they say docs/config/infra only, do not edit application
  code. Inspect code only when docs or metadata claims need to be verified against reality.
- Explicit user instructions take precedence over this skill's defaults. Resolve routine choices
  independently; if a rule blocks requested work, link and quote it and explain why it applies.
- Preserve user-owned changes. If the worktree is dirty, identify whether changes are related before
  editing. Review uncommitted changes in the worktree that contains them. Use a separate worktree
  only when an operation needs isolation and it can include the intended review or edit scope.
- Read applicable repository and agent instruction files before working in each repository.
- Check updater coverage for each dependency and its declaration, not merely whether the repo has an
  updater. Treat version drift as out of scope for covered declarations. For uncovered pins, compare
  against current upstream releases and propose adding automation.
- Preserve badges and other user-owned README signals unless the user explicitly asks to change
  them.

## Mutation safety

- Treat every filesystem or remote mutation as requiring authorization within the agreed task scope.
  Clear "do it", "apply", "fix", or "clean this up" instructions authorize the described class of
  edits. Read-only wording such as "check", "look", "audit", "proposal", or "nothing, just verify"
  does not.
- Before any write command, determine whether the agreed scope covers it; do not ask again for
  permission already granted. This includes `apply_patch`, formatters that rewrite files, `rm`/`mv`,
  generation or synchronization tools, `gh repo edit`, `gh api` `PATCH`/`PUT`/`DELETE`, release/tag
  deletion, and scripts that write generated files.
- Never run `git add`, `git restore --staged`, `git reset`, `git commit`, `git push`, destructive
  checkout/restore commands, or equivalent index/history mutations unless the user explicitly asks
  for that operation.
- When the user asks for a table or proposal first, stop after the proposal. Apply changes only
  after explicit approval.
- Do not treat approval from an earlier turn as approval for a new destructive operation, a new repo
  class, or a different remote mutation. Authorization for the agreed work persists until completed
  or revoked. Complete independent authorized work before asking about a remaining scope decision.
- If a command can write both desired files and unrelated files, either narrow it first or ask
  before running it.

## Workflow

1. Discover the repository set and classify it by stack, toolchain, runtime, deployment role,
   shared-source role, metadata-only role, or unique one-off role.
2. Capture state before edits: `git status -sb`, staged/unstaged names, remotes, and relevant GitHub
   metadata. Preserve the staged index exactly unless the user asks otherwise. The user may stage or
   unstage changes while you work; index drift you did not cause is expected, not an incident.
   Continue without stopping, investigating, or reverting, and mention the change in the final
   report.
3. Build a merged file-class checklist from the actual repos before judging completeness. Include
   docs, package metadata, linters, task runners, CI, container config, dependency automation,
   generated-file config, shared configuration, and GitHub metadata.
4. For each class, compare all applicable repos side by side. Separate justified repo-specific
   differences from accidental drift. Check what should exist but does not: a surface missing from
   one repo while siblings have it (license, ignore entries, dependency automation, docs for an
   option) is drift too.
5. If a file is generated or centrally managed, edit its authoritative source first. Patch target
   copies only when the user explicitly asks or no central update mechanism exists.
6. Apply small, repo-native edits only within the agreed authorization. Prefer deleting stale or
   duplicative docs over expanding prose.
7. After edits, re-read changed files and their affected counterparts in sibling repos. Recheck
   affected relationships; reopen cleared areas only when changes or new evidence warrant it. An
   explicitly requested new full pass covers the full scope again.
8. Finish with validation, GitHub metadata checks, and a concise report of changed files, metadata,
   commands run, and anything intentionally left alone.

Delegate independent repositories or file classes when tools are available and coordination is
worthwhile. Give each agent the same exclusions and mutation boundaries, avoid overlapping edits,
and reconcile shared conventions before accepting changes.

## File-class checklist

Collect these surfaces when they exist:

- README files, docs, badges, install/run/test commands, feature lists, warnings, and UI text that
  duplicates docs.
- Shared governance and instruction files such as agent instructions, license, code of conduct,
  contributing docs, and security docs. If the user says to ignore or centrally manage them, do
  that.
- Package and tool config: package manifests, lockfiles, tool-version files, task runners, formatter
  config, linter config, test config, generated-code config, and language-specific project config.
- Infra config around the project, not runtime services for their own sake: GitHub Actions,
  dependency automation, container build/runtime config, deployment scripts, shared-source config,
  repo templates, and release/tag settings. In workflows, check permissions, triggers, job wiring,
  updater coverage, and adherence to the repository's established action reference policy.
- Example configs and other files prone to leaked personal data: examples use neutral placeholder
  values; hunt real names, tokens, and personal configs that leaked into reusable repos.
- Repository metadata: GitHub description, topics, homepage, visibility, releases, tags, and
  skills.sh metadata when applicable.

## README cleanup

- Make READMEs short, consistent, and factual. Prefer sections that users actually need: what it is,
  install, config, run, test, lint, deploy, maintenance, and references.
- Derive commands from the real task runner or package scripts. Remove commands that do not exist;
  add important commands that exist in `Makefile`, package scripts, or project-native tooling.
- Keep section order and heading style consistent across comparable repos. Use sentence-case
  headings unless the repo has a strong existing convention.
- Remove duplicated philosophy, stale caveats, generic boilerplate, and descriptions that are no
  longer true. Keep domain-specific warnings when they are justified.
- When README text describes UI behavior, welcome text, CLIs, or generated output, verify the real
  code/config that produces it before changing the docs.

## Centrally managed sources

- Apply this section only when the fleet has an explicit generation or synchronization mechanism.
- Treat its shared config or template repository as the source of truth for managed files.
- Inspect the manifest before editing targets. Use target repo changes only to verify what the
  authoritative source currently renders.
- Keep template names and folder layout boring and discoverable. Use one naming rule consistently,
  but allow exceptions when identical downstream filenames need distinguishable templates.
- Validate rendered variants, not only template text. For templated config, render representative
  repos and check whitespace-sensitive formats.
- Do not centrally manage files that are intentionally generated by standard tooling or updated by
  dependency automation unless the user explicitly wants that tradeoff.

## GitHub metadata

- For each repo, capture current metadata before proposing or applying changes:
  `gh repo view OWNER/REPO --json description,repositoryTopics,homepageUrl,isPrivate,url`.
- Descriptions should be concise taglines, not full README sentences. Avoid final punctuation in
  GitHub descriptions. Do not make descriptions longer only to mirror README wording.
- Avoid volatile descriptions such as lists of frequently changing tools or implementation details.
- Topics should be stable, lowercase slug-like terms. Prefer broad, durable topics over a long list
  of every dependency or tool.
- If the user asks for a proposal first, report a table with `repo`, `current`, `proposed`, and
  `changed`. Apply only after confirmation.
- Remote tag or release cleanup is destructive. Only perform it when the user explicitly asks, and
  verify before and after with `gh release list` and `git ls-remote --tags`.

## Validation

Use checks that match the touched surfaces:

Complete required project checks. Use non-mutating checks in read-only mode and scope any authorized
autofixes to preserve unrelated work. Once checks pass, repeat or broaden them only for new changes,
failures, or a specific unresolved concern.

- `git status -sb`, `git diff --check`, and targeted `git diff` reviews in every edited repo.
- JSON with `jq`; JSONC with a JSONC-aware parser or explicit trailing-comma/comment handling.
- YAML/TOML parsing for config files; `bash -n` and `shellcheck` for shell when available.
- Tool-native validation for shared config: linter config verification, formatter/test config
  parsing, container config rendering, workflow syntax checks, or package manager checks when
  applicable.
- `skills.sh.json` against `https://skills.sh/schemas/skills.sh.schema.json` when editing a skills
  repository.
- Explicit metadata assertions after GitHub edits: descriptions have no trailing punctuation and
  topics match `^[a-z0-9][a-z0-9-]*$`.

## Final report

Report only the high-signal result:

- repos touched and the class of cleanup performed;
- files changed and remote metadata changed;
- validation commands and their status;
- files or classes intentionally left alone and why;
- current git status, especially whether changes are unstaged or staged.
