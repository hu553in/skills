---
name: staged-code-review
description: >-
  Perform an exhaustive iterative code review of all staged Git changes, fix every actionable issue
  found, and leave all new fixes unstaged. Use when the user asks for full review of staged changes,
  pre-commit review, release-prep review of staged changes, or similar staged-review requests
  covering correctness, tests, architecture, consistency, performance, invariants, user experience,
  documentation, and cleanup while preserving the staged index.
---

# Staged code review

## Overview

Review staged changes as the primary scope, fix every actionable issue, and repeat until a full pass
finds nothing else to improve. Keep the workflow portable: derive tools, conventions, and validation
from the current workspace instead of assuming a stack, file layout, product domain, absolute path,
or implementation detail. Preserve the user's staged index exactly: never stage, unstage, reset, or
otherwise rewrite staged entries unless the user explicitly asks.

## Request mode

- Default to review-and-fix mode when the user asks for a full staged review, asks to fix findings,
  or asks to keep going until no actionable issues remain.
- If the user explicitly asks for read-only review, proposal-only output, or "do not change
  anything", do not edit files. Report findings with concrete file and line references instead.
- Do not treat approval from an earlier turn as permission to stage, unstage, commit, push, reset,
  or perform any other index/history mutation in the current turn.

## Starting state

1. Read applicable repository, workspace, and agent instruction files.
2. Inspect Git state before analysis:
   - `git status -sb`
   - `git diff --cached --name-status`
   - `git diff --cached --stat`
   - `git diff --name-status`
   - `git diff --cached --check`
3. Treat `git diff --cached` as the authoritative staged review scope. Keep the initial staged
   name/status and stat in mind so the final pass can confirm the staged index stayed unchanged. If
   `git diff --cached --check` reports whitespace or conflict-marker issues, keep the output as
   review findings instead of abandoning the pass.
4. Treat unstaged user changes as separate context. Do not overwrite them. If pre-existing unstaged
   changes overlap the staged files and make safe fixes ambiguous, ask before editing those files.
5. Stop early only when there are no staged changes, and say that clearly.

## Review loop

Repeat this loop until a complete iteration finds no actionable issues:

1. Read the full staged diff and the surrounding files, not only the changed hunks.
2. Discover related surfaces with the best tools available in the workspace. Prefer semantic code
   indexes or language-aware navigation when available; use text search for literals, config,
   documentation, and generated artifacts. Do not assume any particular framework or directory
   structure.
3. Check consistency across every behavior, interface, data shape, UI surface, configuration, and
   document touched or implied by the staged changes.
4. Fix each issue with the smallest change that follows the workspace's existing conventions and
   removes the root cause.
5. Keep every fix unstaged. Use `git status -sb`, `git diff --cached`, and `git diff` after edits to
   confirm the index remained unchanged and to understand the combined end state.
6. If any command unexpectedly changes the staged diff, stop immediately and report the index
   mutation instead of trying to repair it silently.
7. Run the workspace's established validation commands. Prefer existing task runners, CI-equivalent
   checks, linters, formatters, and tests over ad hoc commands.
8. Re-read the staged diff plus the new unstaged fixes. Continue the loop until there are no bugs,
   no missing hardening, no style mismatches, no weak tests, and no useful simplifications left.

## Review checklist

Look for all relevant classes of issues, even when the staged diff looks locally correct. Apply the
checklist to the workspace in front of you; do not force irrelevant stack-specific checks.

- Correctness bugs, behavioral regressions, race conditions, broken error paths, and edge cases.
- Missing or weak tests for the changed behavior, including negative paths and boundary cases. Avoid
  brittle tests that only assert incidental implementation details unless those details are the
  contract.
- Inconsistent style, naming, terminology, localization, layering, ownership, public interfaces, or
  error handling.
- Overcomplicated code, duplicated logic, unnecessary abstractions, dead paths introduced by the
  change, and places where a simpler existing construct is enough.
- Architecture drift from patterns already used in the workspace.
- Unhardened invariants: missing validation, authorization, constraints, lifecycle guards, state
  transitions, transaction boundaries, type narrowing, feature flags, configuration defaults, or
  equivalent safeguards.
- Data and storage issues where applicable: migrations, schemas, indexes, triggers, seeds, fixtures,
  serialization, cleanup behavior, retention behavior, and compatibility with existing data.
- Performance problems, unnecessary network or disk work, inefficient data access, excessive
  rendering, cache invalidation mistakes, repeated computation, or missing resource bounds.
- Security and data-integrity issues, especially authorization, secrets, injection surfaces, unsafe
  deserialization, path handling, migration compatibility, and sensitive logging.
- Dependency mistakes: custom code where an existing dependency should be reused, or a lightweight
  well-maintained dependency would materially reduce complexity. Before adding a new dependency,
  verify current docs, compatibility, license fit, and security impact, then add it only when the
  gain is concrete.
- Deletion, rename, or move fallout: stale imports, routes, exports, registrations, docs, generated
  wiring, permissions, fixtures, snapshots, and packaging references.
- UI and design mismatches where UI exists: spacing, typography, color, interaction states, loading
  and empty states, accessibility, desktop layouts, and responsive behavior down to the smallest
  supported width.
- Documentation, config, deploy, migration, and generated-code drift caused by the staged changes.

## UI verification

When staged changes affect UI and the workspace can be run locally, inspect the real rendered
result. Use the existing dev command or preview workflow, then verify representative desktop and
mobile widths with available browser or screenshot tools. Check for overlap, clipped text, layout
jumps, inconsistent tokens, broken hover/focus/disabled states, and responsive regressions. Fix
visual problems and repeat the rendered check. When available, inspect runtime logs or browser
console output before claiming the UI is clean.

## Validation

- Use the strongest existing validation path that is practical for the changed scope.
- Prefer targeted checks during iteration and a broader check before finishing when feasible.
- Do not claim a check passed unless it actually ran.
- If a check cannot run, report why and keep reviewing what can still be verified locally.

## Stop condition

Stop only after one full clean pass over the staged diff plus any new unstaged fixes finds no
actionable issues. If a remaining question depends on product, policy, access, credentials, or an
external system that cannot be verified locally, report it explicitly instead of guessing.

## Index safety

- Do not run `git add`, `git restore --staged`, `git reset`, `git checkout --`, or equivalent index
  mutations unless the user explicitly asks.
- Do not "clean up" unrelated unstaged work.
- If a formatter modifies files, leave those modifications unstaged and include them in the next
  review iteration.
- If a validation or generation command writes expected files, treat those writes as unstaged fixes
  and review them before finishing.
- If a fix must touch a file that already has unrelated unstaged user edits, avoid clobbering those
  edits. Ask when the safe edit cannot be isolated.

## Final response

Report:

- what was fixed, grouped by file or concern;
- which validation commands ran and whether they passed;
- whether any checks could not be run;
- that new fixes were left unstaged and the original staged index was not modified;
- any remaining risks only when they are real and actionable.
