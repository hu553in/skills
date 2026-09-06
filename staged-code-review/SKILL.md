---
name: staged-code-review
description: >-
  Review staged Git changes within the requested scope, fix actionable issues when authorized, and
  leave all new fixes unstaged. Use when the user asks for full review of staged changes, pre-commit
  review, release-prep review of staged changes, or similar staged-review requests covering
  correctness, tests, architecture, consistency, performance, invariants, user experience,
  documentation, and cleanup while preserving the staged index.
---

# Staged code review

## Overview

Review staged changes as the primary scope, resolve actionable issues when authorized, and verify
the final result. A full review covers all staged changes; honor narrower user boundaries. Keep the
workflow portable: derive tools, conventions, and validation from the current workspace instead of
assuming a stack, file layout, product domain, absolute path, or implementation detail. Preserve the
user's staged index exactly: never stage, unstage, reset, or otherwise rewrite staged entries unless
the user explicitly asks.

## Request mode

- Default to read-only mode for staged reviews, including full reviews. Report findings with
  concrete file and line references without editing files.
- Use review-and-fix mode when the user asks to fix findings or explicitly authorizes edits.
  Requests for another pass or to keep reviewing do not grant edit permission by themselves.
  Explicit read-only or proposal-only instructions override earlier edit authorization.
- Explicit user instructions take precedence over this skill's defaults. Authorization persists
  within the agreed task until completed or revoked; never infer permission for index or history
  mutations from a review request alone.
- Resolve routine choices independently and continue authorized work. If an instruction blocks
  completion, link and quote it, explain why it applies, and complete independent work first.

## Starting state

1. Read applicable repository, workspace, and agent instruction files.
2. Inspect Git state before analysis:
   - `git status -sb`
   - `git diff --cached --name-status`
   - `git diff --cached --stat`
   - `git diff --name-status`
   - `git diff --cached --check`
3. Treat `git diff --cached` as the source of staged changes and apply any narrower user scope. Keep
   the initial staged name/status and stat in mind so the final report can say whether the staged
   scope changed during the review. If `git diff --cached --check` reports whitespace or
   conflict-marker issues, keep the output as review findings instead of abandoning the pass.
4. Treat unstaged user changes as separate context. Do not overwrite them; the ask-before-clobbering
   rule is in Index safety.
5. Stop early only when there are no staged changes, and say that clearly.

## Review loop

Perform a complete review of the requested scope, then revisit areas affected by fixes:

1. Read the full staged diff within the requested scope and the surrounding code needed to
   understand it, not only isolated changed lines.
2. Discover related surfaces with the best tools available in the workspace. Prefer semantic code
   indexes or language-aware navigation when available; use text search for literals, config,
   documentation, and generated artifacts. Do not assume any particular framework or directory
   structure.
3. Check consistency across every behavior, interface, data shape, UI surface, configuration, and
   document touched or implied by the staged changes.
4. In review-and-fix mode, fix each issue with the smallest change that follows the workspace's
   existing conventions and removes the root cause. In read-only mode, report it without edits.
5. Keep every fix unstaged. Use `git status -sb`, `git diff --cached`, and `git diff` after edits to
   track the current staged scope and understand the combined end state.
6. If the staged diff changes mid-review, that is usually the user staging or unstaging while you
   work, including fixes you just made; it is expected, not corruption. Do not stop, investigate,
   revert, or otherwise touch the index in response. Refresh the review scope, continue, and mention
   the change in the final report.
7. Run the workspace's established validation commands. Prefer existing task runners, CI-equivalent
   checks, linters, formatters, and tests over ad hoc commands.
8. Check the final diff for consistency and verify affected behavior and dependencies. Reopen
   cleared areas only when a change or new evidence affects them. Finish when the requested scope is
   covered, authorized fixes are complete, and required checks are complete. In read-only mode,
   report findings; report blockers for any authorized fix that cannot be completed. Do not extend
   the task to speculative hardening or optional improvements.

For substantial reviews, delegate independent areas when tools are available and coordination saves
work. Preserve the same scope and index boundaries for every agent and reconcile findings centrally.

## Review checklist

Look for all relevant classes of issues, even when the staged diff looks locally correct. Apply the
checklist to the workspace in front of you; do not force irrelevant stack-specific checks.

- Correctness bugs, behavioral regressions, race conditions, broken error paths, and edge cases.
- Changed algorithmic code (hashing, randomness, arithmetic) not verified against a reference
  implementation; eyeballed output is not equivalence.
- Missing or weak tests for the changed behavior, including negative paths and boundary cases. Avoid
  brittle tests that only assert incidental implementation details unless those details are the
  contract. Flag tests whose only assertion is that a deleted thing stays absent, and tests that
  exist only to move a coverage number.
- Tests that pass for the wrong reason: negative tests where the environment auto-injects config
  (env files, defaults) and turns "without X" falsely green, boundary tests placed on empty cases
  where no signal exists, and smoke tests that only check artifacts parse instead of asserting
  expected content.
- Inconsistent style, naming, terminology, localization, layering, ownership, separation of
  concerns, public interfaces, or error handling.
- Overcomplicated code, duplicated logic, unnecessary abstractions, dead paths introduced by the
  change, and places where a simpler existing construct is enough.
- Unfinished scaffolding that displaces working end-to-end behavior, or a knowingly disposable
  stopgap that only works for now and is meant to be replaced later.
- Obsolete paths preserved through compatibility layers, fallbacks, or migration paths unless
  required by an explicit public contract, existing persisted data, a staged rollout, or a user
  requirement.
- Architecture drift from patterns already used in the workspace. Propose concrete best-practice or
  architectural improvements even when they require refactoring, but require a demonstrated benefit
  rather than churn for its own sake.
- Unhardened invariants: missing validation, authorization, constraints, lifecycle guards, state
  transitions, transaction boundaries, type narrowing, feature flags, configuration defaults, or
  equivalent safeguards.
- Data and storage issues where applicable: migrations, schemas, indexes, triggers, seeds, fixtures,
  serialization, cleanup behavior, retention behavior, and compatibility with existing data.
- Performance problems, unnecessary network or disk work, inefficient data access, excessive
  rendering, cache invalidation mistakes, repeated computation, or missing resource bounds.
- Security and data-integrity issues, especially authorization, secrets, injection surfaces, unsafe
  deserialization, path handling, migration compatibility, and sensitive logging.
- Stale pinned versions in files the staged changes touch: verify updater ownership and coverage
  first. Compare dependencies, actions, and tools against current upstream releases only when no
  updater owns them; internal consistency review cannot catch uncovered staleness.
- Dependency mistakes: custom code where an existing dependency should be reused, or a lightweight
  well-maintained dependency would materially reduce complexity. Before working around an installed
  dependency or adding another one, check its current official documentation, public API, and types
  when available; do not assume from memory that it lacks the required capability. Verify
  compatibility, license fit, and security impact before adding a dependency, and add it only when
  the gain is concrete.
- Deletion, rename, or move fallout: stale imports, routes, exports, registrations, docs, generated
  wiring, permissions, fixtures, snapshots, and packaging references.
- UI and design mismatches where UI exists: spacing, typography, color, interaction states, loading
  and empty states, accessibility, desktop layouts, and responsive behavior down to the smallest
  supported width.
- Comment problems: narration of what the code does, notes addressed to the reviewer, comments the
  change left stale, group comments orphaned by reordering, and magic values without a comment
  naming the constraint that produced them.
- Documentation, config, deploy, migration, and generated-code drift caused by the staged changes.
  Treat doc examples and example configs as code: they must parse and run against the changed
  implementation, with shown defaults identical to it.

## UI verification

When staged changes affect UI and the workspace can be run locally, inspect the real rendered
result. Use the existing dev command or preview workflow, then verify representative desktop and
mobile widths with available browser or screenshot tools. Verify against a fresh or cache-busted
load; a cached page shows stale output and falsifies the check in both directions. Check for
overlap, clipped text, layout jumps, inconsistent tokens, broken hover/focus/disabled states, and
responsive regressions. When edits are authorized, fix visual problems and recheck affected states.
When available, inspect runtime logs or browser console output before claiming the UI is clean.

## Validation

- Use the strongest existing validation path that is practical for the changed scope.
- When the workspace defines one command that runs all its checks with autofixes, prefer it over
  running individual tools and fixing their output by hand only when its edits are authorized and
  scoped. Use non-mutating checks for read-only reviews and preserve unrelated user work.
- Treat tool output defensively: validate content, not only exit codes; some tools print errors to
  stdout and exit zero.
- Scale checks to the changed behavior and risk, including required project checks. After they pass,
  repeat or broaden them only for new changes, failures, or a specific unresolved concern.
- Do not claim a check passed unless it actually ran.
- Distinguish the staged snapshot from the combined worktree. Checks run in the worktree validate
  that state, not necessarily the staged snapshot. If unstaged changes could mask a staged defect,
  verify the staged version separately when feasible without changing the user's index or worktree;
  otherwise report that limitation. Do not require isolation when the difference is irrelevant.
- If a check cannot run, report why and keep reviewing what can still be verified locally.

## Stop condition

Finish after covering the requested scope, checking the final diff and completing relevant
validation. Complete actionable in-scope fixes in review-and-fix mode; report findings in read-only
mode and genuine blockers or verification limits in either mode. Do not claim perfection. An
explicitly requested new full pass covers the full scope again. If a remaining question depends on
product, policy, access, credentials, or an external system that cannot be verified locally, report
it explicitly instead of guessing.

## Index safety

- Do not run `git add`, `git restore --staged`, `git reset`, `git checkout --`, or equivalent index
  mutations unless the user explicitly asks.
- Do not "clean up" unrelated unstaged work.
- If a formatter modifies files, leave those modifications unstaged and include them in the next
  review iteration. After any automated unsafe fix, treat touched bit-twiddling, hashing, and
  randomness code as broken until verified against a reference implementation.
- If a validation or generation command writes expected files, treat those writes as unstaged fixes
  and review them before finishing.
- If a fix must touch a file that already has unrelated unstaged user edits, avoid clobbering those
  edits. Ask when the safe edit cannot be isolated.

## Final response

Report:

- findings first in read-only mode, or what was fixed in review-and-fix mode, grouped by concern;
- which validation commands ran and whether they passed;
- whether any checks could not be run;
- which state was validated, whether new fixes were left unstaged, and whether the staged scope
  changed during the review (the user staging or unstaging mid-review is normal and only needs a
  mention);
- any remaining risks only when they are real and actionable.
