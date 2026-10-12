# ADF editing details

Use the fetched page's actual node shapes. The
[ADF structure reference](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
describes common nodes; an individual editor may support only part of that schema and may add its
own attributes. Preserve existing editor-specific data.

## Markdown and other markup

Convert new content written in Markdown or another markup format to ADF rather than pasting it as
paragraph text, following the shapes the page already uses.

- Map headings, lists, quotes, tables, and fenced code to `heading`, `bulletList`, `orderedList`,
  `blockquote`, `table`, and `codeBlock` nodes, and inline formatting to `strong`, `em`, `strike`,
  `code`, and `link` marks. A `heading` needs `attrs.level` (1-6), and an `orderedList` that does
  not start at 1 needs `attrs.order`. A header row becomes `tableHeader` cells; every cell holds
  block content such as a `paragraph`. The first word of a fence's info string becomes the
  `codeBlock`'s `attrs.language`, following the language values neighboring `codeBlock`s use;
  without neighbors, use the fence's language name in lowercase.
- A thematic break becomes `rule`, and a task list becomes `taskList` with `taskItem` nodes; a
  `taskItem` holds inline content directly, without a `paragraph`, and needs `attrs.localId` and
  `attrs.state` (`TODO` or `DONE`); the `taskList` needs only its own `attrs.localId`.
- For a new link to a Confluence page, use the page URL without its trailing title segment
  (`.../spaces/KEY/pages/123`); Confluence drops that segment on save. Leave existing links as
  fetched.
- Every `text` node needs non-empty `text`. Represent an empty cell or line as a `paragraph` without
  `content` rather than an empty `text` node.
- ADF nests less than Markdown: a `blockquote` or `listItem` cannot contain a `heading`, `table`, or
  `blockquote`, so restructure such content instead of nesting it.
- Map a source line break to `hardBreak` only when it is explicit (`<br>`, a trailing backslash, or
  two trailing spaces); join soft-wrapped lines with a space.
- Per the ADF schema, a `code` mark combines only with `link` and `annotation` marks, so drop any
  other mark from code text; text inside a `codeBlock` carries no marks.
- An image becomes a `mediaSingle` holding a `media` node; include the `mediaSingle`'s
  `attrs.layout`, following neighboring images. A `file` media node refers to an uploaded
  attachment, which the helper does not create. An `external` media node takes `attrs.url`; check in
  the UI that it renders. If neither an existing attachment nor a rendering external image fits,
  keep the image as a link or ask the user.
- Search the new `text` nodes outside `code` marks and `codeBlock` content for leftover source
  syntax: `**`, `__`, `~~`, backticks, `](`, `![`, `<br>`, `[ ]`, `[x]`, HTML entities such as
  `&amp;`, backslash escapes, and a `>`, `#`, `-`, `*`, `|`, or a list number such as `1.` at the
  start of a paragraph.

## Mentions, cards, and dates

- A `mention` uses the verified Atlassian account ID in `attrs.id`. Preserve its existing text and
  attributes when unrelated to the edit. Plain `@Name` text is not a mention. Resolve a new account
  ID through an authorized user lookup rather than guessing it from a display name.
- A URL-backed `inlineCard` stores its target in `attrs.url`. Use the supplied or verified
  issue/page URL. A
  [data-backed card](https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/inlineCard/)
  uses `attrs.data` instead; `url` and `data` are mutually exclusive. Preserve the fetched card
  shape and follow its editor contract when changing representation. A link mark and a smart card
  are different node shapes.
- A `date` stores an epoch-millisecond timestamp string. For a date-only edit, use the intended
  calendar date at midnight UTC, following neighboring date nodes, rather than local midnight.

Retain existing `localId` and other identity attributes. Generate fresh IDs for new nodes only where
that node shape requires them, using the format accepted by the surrounding editor. Do not impose
one invented ID length on every node type.

## Tables and macros

Keep `tableCell` and `tableHeader` span attributes, cell order, table layout, and column widths.
Rows covered by a `rowspan` can omit the spanned column; reconstructing a visually rectangular table
can corrupt its structure. Inspect neighboring rows before changing a merged region.

Shape a new table like its neighbors. Without a `colwidth` array (one pixel width per spanned
column) on every cell, the Cloud editor gives every column the same width; `attrs.width` on the
`table` sets its overall width. A long value without spaces in a `code` mark cannot wrap at a word
boundary, so a narrow column breaks it mid-word. To keep such values whole, set `colwidth` on every
cell and give that column enough width for its longest value. When a cell lists several such values,
put each on its own line with `hardBreak` so the column needs only the width of the longest one.

Preserve macro nodes such as `extension`, `bodiedExtension`, `inlineExtension`, and
`multiBodiedExtension`, including their parameters, nested content, and IDs. Edit their internals
only when required by the request and supported by the macro's actual contract.

## Comment anchors and preservation checks

Preserve annotation marks and IDs on unchanged text; moving or deleting annotated text may move or
orphan its comment's anchor. The helper's CLI commands do not read comments and cannot prove that a
comment still targets the intended text. When editing annotated text:

1. Read the page's inline comments through the host's Confluence tool if its response includes
   `properties.inlineMarkerRef` and `resolutionStatus` and it can return comments of all four
   resolution statuses (`open`, `reopened`, `resolved`, `dangling`). Otherwise use the helper's
   client, which keeps its redirect and API-context checks. Scoped tokens also need
   `read:comment:confluence` (see [helper usage](helper-usage.md)). Do not put the token in a
   command argument. Request every resolution status explicitly, since the API's default is not
   documented.

   Run it with `python3 -B` so the import writes no bytecode into the skill directory.

   ```python
   import sys

   sys.path.insert(0, "SCRIPT_DIR")  # this skill's scripts directory
   from confluence_adf import load_client

   CONFIG = None  # or the MCP config path
   # Pass "SERVER_KEY" as a second argument when the commands use --mcp-server.
   client = load_client(CONFIG)
   statuses = "&".join(
       f"resolution-status={status}"
       for status in ("open", "reopened", "resolved", "dangling")
   )
   comments = client.call(f"pages/PAGE_ID/inline-comments?limit=250&{statuses}")
   ```

   Follow `_links.next` by passing only the part after `/api/v2/`; the link is site-relative, and
   the helper refuses it as given under a gateway context URL.

2. Match each comment's `properties.inlineMarkerRef` to an annotation mark's `attrs.id`, and note
   its `resolutionStatus`. The marks in `base.json`, not the fetched comments, decide what to keep:
   a comment missing from the fetch still has an anchor to preserve.
3. For every `annotation` mark `attrs.id` in the `base.json` nodes being edited, except ids whose
   fetched comment is `dangling`, find the annotated text (the text of the `base.json` nodes
   carrying that `attrs.id`) in the content that replaced it and apply the mark (same `attrs.id` and
   `annotationType`) to exactly that substring, splitting text nodes if needed. Resolved comments
   keep their marks too. If the text appears more than once there, use the occurrence that matches
   the original context; when none clearly does, the text no longer appears, or it now sits in a
   `codeBlock`, leave the mark out and report it.
4. Before publishing, list in the final report every `annotation` `attrs.id` present in `base.json`
   but absent from `new.json`, whether or not a comment was fetched for it, with its
   `resolutionStatus` when known. If the helper's verification fails or another tool writes the
   page, repeat the check on a fresh `get` of the stored page. A `dangling` status confirms the same
   loss once Confluence has updated it.

Keep comments outside the authorized edit untouched.

Compare changed JSON paths before publication and account for each change. Equal mention, macro, or
merged-cell counts cannot prove preservation: one node may replace another with the same type.
Assert equality for unaffected subtrees, including attributes and marks, and keep node order
significant. The helper's post-write comparison checks that the stored ADF matches the prepared
document (see [helper usage](helper-usage.md) for the page-link title exception), not that the
prepared document meets the user's requested scope.
