---
name: repo-fleet-standardization
description: >-
  Audit or standardize docs, config, tooling, and metadata across related repositories, without
  editing application code. Use for fleet-wide consistency work.
---

# Repo fleet standardization

Make the requested surfaces match each repository's real behavior and shared conventions. Preserve
justified differences; consistency does not mean making every repository identical.

## Scope and authorization

- Default to read-only for checks, audits, and proposals. Clear instructions to apply, fix, or clean
  up authorize the described edits within the agreed scope. A proposal-first request ends at the
  proposal until approved.
- Do not edit application code. Inspect it only to verify docs or metadata claims. Honor excluded
  repositories, file classes, and parent-owned governance or agent files.
- Read applicable repository and agent instructions before working in each repository. Explicit user
  instructions take precedence over skill defaults; if a rule blocks requested work, link and quote
  it and explain its application.
- Remote changes need independent authorization for the specific operation and scope; permission for
  local cleanup does not authorize GitHub edits or destructive tag/release cleanup.
- Never stage, unstage, commit, push, reset, rewrite history, or use destructive checkout/restore
  commands without an explicit request for that operation. Make authorized edits in the worktree.
- Check status and staged/unstaged changes before editing; preserve user-owned work and the index.
  User staging or unstaging during the task is expected: do not investigate or normalize it.
  Continue and mention observed changes in the report. Review uncommitted work where it exists; use
  isolation only when needed and able to include the intended scope.
- Authorization persists until completed or revoked, but does not extend to a new repository class,
  destructive operation, or different remote mutation. Continue independent authorized work while a
  remaining scope decision is unresolved; do not ask again for granted permission.
- Writes include formatters, generators, synchronization, file moves/deletions, and API commands
  that mutate remote state. Determine authorization from actual effects; read-only API queries are
  not writes. Narrow commands that could modify unrelated files, or ask before running them.

## Establish coverage

Identify the requested repository set and applicable file classes from actual files. For broad fleet
audits, account for stack, runtime, deployment, shared-source, metadata-only, and one-off roles.
Compare applicable siblings, including missing surfaces, rather than imposing a universal template.
For a narrow request, inspect only the surfaces and relationships needed to settle it.

For a full matrix audit, track each repository against its applicable areas as checked, not
applicable, or blocked, with supporting evidence or a reason. Include this compact coverage matrix
in the chat report so omissions remain visible. Create or update a persistent repository file for
the matrix only when explicitly requested; narrow tasks do not require a matrix.

Useful coverage areas, when in scope:

- Docs and READMEs: badges, commands, feature claims, warnings, and text duplicated in UI or output.
- Governance: licenses, contribution/security docs, and agent instructions, respecting exclusions
  and central ownership.
- Tooling: manifests, lockfiles, runtime versions, task runners, formatter/linter/test configs, and
  generated-file config.
- Infra: CI permissions, triggers, job wiring, container build/runtime config, deployment scripts,
  dependency automation, templates, and shared configuration. Do not expand into runtime services
  for their own sake.
- Examples: neutral placeholders, not leaked personal names, tokens, or private configuration. Do
  not expose secrets in findings.
- Metadata: descriptions, topics, homepages, visibility, releases, tags, and `skills.sh` metadata.

Check updater ownership for each dependency declaration, not merely the presence of Renovate. When
dependencies are in scope, compare with current stable releases even for covered declarations.
Prefer upgrades, including majors, rather than waiting for the updater. Coordinate with existing
update PRs, keep related declarations consistent, and verify the result. Resolve fixable
incompatibilities within authorized scope; if an upgrade requires application-code changes, report
the needed work rather than violating this skill's boundary. Defer upgrades only for demonstrated
blockers that cannot be resolved within scope, explaining why. Propose automation for uncovered
declarations. Preserve intentional floating major action tags, internal reusable workflow branch
refs, and explicit user version constraints. Read-only audits propose upgrades without applying
them.

Read conditional guidance only when relevant:

- An explicit generation/synchronization mechanism manages files:
  [Managed sources](references/managed-sources.md). Establish ownership before target edits.
- GitHub metadata is in scope: [GitHub metadata](references/github-metadata.md). This includes
  proposal and destructive-cleanup safeguards; loading it does not authorize remote writes.

## Docs and consistency

Keep READMEs short and factual. Use sections readers need, such as install, config, run, test, lint,
deploy, maintenance, and references; keep order and sentence-case headings consistent across
comparable repos unless a strong local convention differs.

Derive commands from actual task runners or package scripts. Remove nonexistent commands and include
important supported ones. Verify claims about UI, CLIs, welcome text, or generated output against
their producing code/config. Preserve the purpose and user-selected content of badges and other
README signals. Correct broken URLs or renamed workflow references within authorized
standardization; removing a meaningful badge or changing what it represents requires explicit
authorization. Retain justified domain warnings. Remove stale caveats, duplicated philosophy,
boilerplate, and false claims rather than expanding prose.

## Completion and verification

An audit is complete when the declared repository/file-class scope has been covered, justified
differences are separated from drift, and findings or unknowns have evidence. A proposal-first task
stops there. Authorized cleanup continues until scoped findings are resolved or explicitly left
pending with a reason, and affected cross-file and sibling-repository relationships are consistent.
Do not stop at the first repository or finding in a full-fleet request.

After edits, review changed files and affected counterparts. Reopen cleared areas only for new
changes or evidence; an explicitly requested full pass covers the whole declared scope again.
Independent repositories/classes may be delegated when worthwhile, with shared exclusions and
authorization boundaries, non-overlapping edits, and reconciled conventions.

Complete required project checks and choose additional validation by the touched contract. Use
non-mutating checks in read-only work; scope authorized autofixes to protect unrelated changes.
Examples include:

- Status, `git diff --check`, and targeted diff review in edited repositories.
- JSON with `jq`, JSONC with a parser that supports comments/trailing commas, YAML/TOML parsing, and
  `bash -n` or `shellcheck` for shell changes.
- Native config validation, container rendering, workflow checks (including shared caller/input
  contracts), and package-manager checks where affected.
- Validate changed `skills.sh.json` against `https://skills.sh/schemas/skills.sh.schema.json`.

Stop validation when relevant checks pass and no specific concern remains; broaden or repeat only
for failures, new changes, or unresolved risk. Report unavailable checks or blocked scope instead of
implying verification or silently expanding authorization.

Finish with repositories/files and remote metadata changed, checks actually run and their results,
intentional exclusions or unresolved items, and current staged/unstaged status. For read-only work,
report findings instead of changes.
