# Review checklist

Look for all relevant classes of issues, even when the staged diff looks locally correct. Apply the
checklist to the workspace in front of you; do not force irrelevant stack-specific checks.

- Correctness bugs, behavioral regressions, race conditions, broken error paths, and edge cases.
- Changed algorithmic code (hashing, randomness, arithmetic) without independent verification
  appropriate to its risk: expected results, boundary cases, or a trusted reference implementation.
  Eyeballed output is not equivalence.
- Missing or weak tests for the changed behavior, including negative paths and boundary cases. Avoid
  brittle tests that only assert incidental implementation details unless those details are the
  contract. Flag tests whose only assertion is that a deleted thing stays absent, and tests that
  exist only to move a coverage number.
- Tests that pass for the wrong reason: negative tests where the environment auto-injects config
  (env files, defaults) and turns "without X" falsely green, boundary tests placed on empty cases
  where no signal exists, and smoke tests that only check artifacts parse instead of asserting
  expected content.
- Meaningless tautological tests in any form: self-comparisons, expected results derived by copying
  the implementation, or assertions that only confirm their own fixtures or mocks. Report them in
  read-only reviews; remove them when fixes are authorized. Do not write replacements with the same
  flaw or remove meaningful contract, property, or round-trip tests that can detect real defects.
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
- Stale pinned versions in files the staged changes touch: verify updater ownership and coverage and
  compare dependencies, actions, and tools against current stable releases even when an updater owns
  them. Propose upgrades, including majors, and identify fixable incompatibilities rather than
  treating them as automatic blockers. Apply upgrades only within authorized scope, keeping related
  declarations consistent and validating the result. Explain any unresolved blocker. Report upgrade
  opportunities separately from defects unless there is a demonstrated correctness or security
  issue; the existence of a newer release alone does not make the staged change defective.
- Dependency opportunities: prefer existing capabilities or a suitable, well-maintained library over
  custom code even for a small reduction in implementation and maintenance, especially for server
  code and tooling outside the client bundle. Client-bundle inclusion alone is not a blocker; assess
  actual size and runtime impact. Retain custom code for concrete drawbacks such as incompatibility,
  security or licensing problems, poor maintenance, or disproportionate overhead, not merely to
  minimize dependency count. Before working around an installed dependency or adding another one,
  check its current official documentation, public API, and types when available; do not assume from
  memory that it lacks the required capability. Verify compatibility, license fit, and security
  impact before adding a dependency. Distinguish maintenance improvements from correctness defects
  and apply them only within authorized scope.
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
