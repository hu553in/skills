---
name: repo-fleet-standardization
description: Audit or standardize docs, config, tooling, and metadata across related repositories.
---

# Repo fleet standardization

Audits and proposals are read-only. Apply requested fixes in the worktree. Preserve application
code, the index, and unrelated changes. Commit, alter Git history, or change remote state only with
explicit authorization for that operation.

## 1. Establish coverage

Record the repositories, refs, exclusions, and existing decisions. Include linked worktrees by
request. Read each repository's instructions and status. For a narrow request, follow the named
files and their consumers.

For a full pass, inventory tracked and unignored new paths with
`git ls-files --cached --others --exclude-standard -z`. Include hidden and nested files. During diff
review, read staged and unstaged diffs separately, including deletions and renames. Use the
requested base for committed changes.

Assign each path a file type or a reason for exclusion. Cover docs and demos, Git config, ignore
rules, hooks, governance, dependencies, tool and test config, scripts, build and packaging, CI and
release, and deployment. Check for expected files that are missing. Track each repository and file
type as checked, not applicable, blocked, or excluded. Mark a cell checked only after inspecting
every in-scope path in it. Record evidence or a reason and reconcile the matrix with the inventory
before closing the pass.

## 2. Compare the fleet

Compare repositories by file type and purpose. For each finding, check every applicable repository,
including equivalents with different names and indirect callers. Record a fix, a justified
exception, or an unresolved issue for every occurrence. Carry agreed exceptions into repeat passes.

- When a shared source generates or synchronizes files across repositories, read
  [Managed sources](references/managed-sources.md).
- For GitHub metadata, settings, rulesets, tags, or releases, read
  [GitHub metadata](references/github-metadata.md).

## 3. Make authorized fixes

Standardize where it reduces maintenance or improves a user task. Before removing a tool or job,
identify and preserve the behavior users and automation rely on. Prefer built-in commands that cover
the required formats and outputs. Keep custom behavior that covers a demonstrated gap. Move slow
hook checks to CI only when CI still runs them. Remove obsolete calls, setup, config, dependency
entries, and docs together.

Check dependency declarations against lockfiles and honor existing version policy. Check for new
releases and do standalone lockfile maintenance only when requested. Update affected lockfiles when
changing manifests.

Derive README and demo commands from supported entry points. Fix stale claims and preserve
intentional badges and relevant warnings. Keep internal release-age flags and their
environment-variable equivalents in config or automation. Use neutral placeholders for private
values.

## 4. Verify and report

Use project checks and exercise the changed command or inspect the artifact when behavior changes.
For a changed shared CI contract, resolve each caller's workflow ref and check the new setup and any
mixed versions that can run during rollout. Record any necessary rollout order. Keep secrets out of
evidence and reports.

Review the final diff and any affected callers. Reuse previous check results only when inputs and
relevant conditions still match.

Report findings or fixes, justified exceptions, and any coverage gaps. Identify the version checked
and label the evidence as inspection, local execution, artifact verification, or CI for a commit
SHA. Include Git status for edited repositories. Link a large matrix as a temporary report and add
it to a repository only on request.
