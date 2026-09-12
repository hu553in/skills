---
name: staged-code-review
description:
  Review staged Git changes before committing. Read-only by default; fix findings when asked,
  leaving fixes unstaged.
---

# Staged code review

Review the staged diff within the user's scope, including affected contracts and consumers. Derive
tools and conventions from the workspace; do not assume a stack or product. A full review covers all
staged changes, not a sample.

## Mode and boundaries

- Default to read-only. Review-and-fix requires authorization to fix findings; a request to keep
  reviewing does not grant it by itself. Existing authorization persists for the agreed task until
  completed or revoked. Explicit read-only or proposal-only instructions take precedence.
- Preserve the index: do not stage, unstage, reset, commit, push, or rewrite history without an
  explicit request. Leave fixes and authorized generated output unstaged.
- Preserve unrelated user work. Ask only when a necessary fix cannot be isolated safely or a
  material product, policy, access, or external-system question cannot be resolved from evidence.
  Continue independent work rather than stopping the whole review.

## Scope and evidence

Use `git diff --cached` as the source of the staged patch. Inspect status and unstaged differences
to distinguish the patch from the combined worktree; retain enough context to notice a changed
review scope. Include whitespace and conflict-marker issues from `git diff --cached --check` without
abandoning the review. If nothing is staged, say so instead of substituting unstaged work.

Read the full in-scope diff and the surrounding code, contracts, and callers needed to judge it. Use
code navigation or text search as appropriate; do not require a whole-repo map for a narrow change.
Use [the review checklist](references/review-checklist.md) for relevant risk categories. For a full
review, consider every applicable category; a category is not a requirement to inspect unrelated
parts of the project. Its UI section applies when rendered behavior changes.

If the staged scope changes while reviewing, refresh it and continue. User staging or unstaging is
normal: do not investigate, revert, or touch the index in response. Mention a material scope change
in the handoff.

## Review and fixes

Report evidence-backed issues, not speculative hardening or optional churn. In read-only mode,
provide concrete file and line references. In review-and-fix mode, resolve actionable in-scope
findings at their root cause using existing conventions, then review the affected relationships and
final combined diff. Do not stop after the first fix to request permission already granted.

Delegate independent parts of substantial reviews when worthwhile and available, with the same scope
and index boundaries. Reconcile findings before accepting them.

## Validation and completion

Use established checks that address the changed contract and risk, including required project
checks. Use non-mutating checks in read-only mode; prefer a project autofix command only when its
edits are authorized and scoped. Review any generated changes before finishing. For unsafe automated
changes to hashing, randomness, or arithmetic, use independent expected results, boundary cases, or
a trusted reference implementation appropriate to the algorithm's risk.

Checks on the worktree validate that state, not necessarily the staged snapshot. If unstaged changes
could mask a staged defect, verify the staged state separately when feasible without changing the
user's index or worktree; otherwise report the limit. Do not require isolation when the difference
is irrelevant.

Check output as well as exit status. Do not claim unexecuted checks passed. After a check passes,
repeat it only for a new change, failure, or unresolved concern. Continue independent review if a
check cannot run and report why.

Finish when the requested scope is covered, authorized fixes are complete, and relevant validation
is complete or its genuine limits are reported. Do not claim perfection or expand into unrelated
improvements. An explicitly requested new full pass covers the full scope again.

Report findings first in read-only mode, or fixes in review-and-fix mode, followed by executed
validation, the state validated, and any real remaining risks. Confirm that new fixes were left
unstaged; avoid a long recap when the pass is empty.
