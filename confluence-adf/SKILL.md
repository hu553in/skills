---
name: confluence-adf
description: >-
  Edit existing Confluence Cloud pages through their native ADF JSON, preserving unrelated rich
  content and checking page appearance and version conflicts. Use when updating a Cloud page with
  mentions, macros, merged cells, or comment anchors.
---

# Confluence ADF

Change the requested parts of an existing Cloud page using its original `atlas_doc_format` body.
Keep untouched nodes, attributes, marks, and page appearance. This workflow covers published pages
with native ADF, not page creation, legacy-editor conversion, or Confluence Data Center.

## Scope and source

- A request to edit or publish the specified page authorizes that change. A review or proposed edit
  ends with the proposal. Ask only when publication or its scope is not already authorized.
- Search tools and rendered, Markdown, or storage-format reads can help locate and understand a
  page. Use a direct ADF read as the editing baseline. A converted representation can flatten
  mentions or lose editor metadata even when its visible text looks correct.
- Use a write tool only when its contract supports the original ADF and version checks. The bundled
  helper uses REST v2 and checks appearance before and after the update. Do not rebuild a rich page
  from a search or converted tool response.
- Publishing the current version can merge into or overwrite an unpublished draft. Check for pending
  collaborative edits before publishing; resolve a divergent draft with its owner. The helper
  rejects an accessible divergent draft, but cannot lock drafts or appearance properties.

## Read and prepare

Read [helper usage and credentials](references/helper-usage.md) before running the script. Resolve
`scripts/confluence_adf.py` relative to this `SKILL.md`, regardless of the agent's installation
path. Use a session scratch directory outside published or committed content; snapshots contain page
data.

1. Run `get PAGE_ID base.json`. Confirm the site, page ID, title, and requested edit against the
   saved snapshot. Keep `base.json` unchanged for conflict detection and recovery.
2. Load `base.json["adf"]`, change only the requested nodes, and save the complete ADF document as
   `new.json`. Preserve unknown nodes and attributes rather than normalizing or recreating them.
   Before publication, compare the actual changed paths and assert that unaffected content is equal
   to the baseline. Read [ADF editing details](references/adf-editing.md) when changing mentions,
   cards, dates, tables, macros, or text with comment annotations.
3. Review the resulting diff against the request. For a proposal, return the proposed change here.
   For an authorized publication, continue through verification.

## Publish and verify

1. Run `put PAGE_ID base.json new.json "Describe the requested change"`. The helper checks the
   snapshot's site and page ID, rereads the published page and appearance, and uses the next page
   version. An unchanged ADF produces no write. A stale baseline requires a fresh read and a rebuilt
   edit. For HTTP 409, inspect version conflicts and any page approval requirements; do not force an
   overwrite or bypass approval.
2. A successful `put` rereads and verifies the stored ADF, title, version, and appearance. Run
   `verify PAGE_ID base.json new.json` for a separate check or after an ambiguous write result.
   Verification ignores mark ordering only. Node counts are diagnostics, not proof of preservation.
3. Inspect the affected page in the UI when rendered behavior matters, including edited mentions,
   table spans, macros, comment anchors, and width. JSON equality does not prove that a macro
   renders or that an inline comment still targets the intended text. Report when UI checks are
   unavailable.

On a timeout or failed post-write check, read the page before retrying. Publication may already have
succeeded. Report the mismatch and retain the baseline; do not automatically restore an old body or
rewrite properties over newer work. Page history can restore a prior body when authorized, but page
appearance is a separate property and needs its own recovery check.

Finish with the page link, saved version, requested changes, actual verification results, and any
remaining mismatch. Do not claim comments or rendered content were verified from counts alone.
