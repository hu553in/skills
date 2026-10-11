# ADF editing details

Use the fetched page's actual node shapes. The
[ADF structure reference](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
describes common nodes; an individual editor may support only part of that schema and may add its
own attributes. Preserve existing editor-specific data.

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

Preserve macro nodes such as `extension`, `bodiedExtension`, `inlineExtension`, and
`multiBodiedExtension`, including their parameters, nested content, and IDs. Edit their internals
only when required by the request and supported by the macro's actual contract.

## Comment anchors and preservation checks

Preserve annotation marks and IDs on unchanged text. When editing annotated text, inspect its inline
comment in the page UI; moving or deleting the text may move or orphan the anchor. The helper does
not fetch separate comment resources and cannot prove that a comment still targets the intended
text. Keep comments outside the authorized edit untouched.

Compare changed JSON paths before publication and account for each change. Equal mention, macro, or
merged-cell counts cannot prove preservation: one node may replace another with the same type.
Assert equality for unaffected subtrees, including attributes and marks, and keep node order
significant. The helper's post-write comparison checks that the stored ADF equals the prepared
document, not that the prepared document itself meets the user's requested scope.
