# Helper usage

The helper requires Python 3.10 or newer and uses only its standard library. Resolve the script from
the installed skill directory. The examples below assume that directory is the current directory.
Replace `123456` with the requested page's content ID, not its title or a URL.

## Credentials

Use an existing authorized account with page read/update permissions. Supply `CONFLUENCE_URL`,
`CONFLUENCE_USERNAME`, and `CONFLUENCE_API_TOKEN` together through the process environment.
`CONFLUENCE_USERNAME` is the account email. `CONFLUENCE_URL` is the HTTPS Cloud context URL, such as
`https://example.atlassian.net/wiki`; a site-root URL also works. For a scoped token, use its
required API gateway context URL, such as `https://api.atlassian.com/ex/confluence/CLOUD_ID/wiki`,
with the required page read/write scopes. A separate inline-comment read with the same scoped token
also needs `read:comment:confluence`.

When credentials already belong to a local MCP server, pass its JSON configuration explicitly:

```sh
python3 scripts/confluence_adf.py --mcp-config ~/.claude.json get 123456 /tmp/base.json
```

This reads `mcpServers.atlassian.env`. Add `--mcp-server SERVER_KEY` before the subcommand for
another server key. A configured environment takes precedence; a partial environment fails instead
of mixing credentials from different sources. Pass the same credential options to every command. No
configuration is read on import or `--help`.

Use the host's existing secret mechanism. Keep tokens out of chat, command arguments, generated
scripts, and committed files. The helper prints neither authentication values nor raw error bodies.

## Certificate errors

The helper's certificate verification error names OpenSSL's reason and the usual fix. The system
bundle for `SSL_CERT_FILE` is `/etc/ssl/cert.pem` on macOS and `/etc/ssl/certs/ca-certificates.crt`
(from the `ca-certificates` package) on Debian-based Linux. On python.org builds for macOS,
`Install Certificates.command` changes the CA store of that Python installation for every program
that uses it, so leave it to the user. "self-signed certificate in certificate chain" (older OpenSSL
omits the hyphen) usually means a TLS-inspecting proxy: use a bundle that includes the CA the user's
organization distributes. Never trust a certificate exported from the failing connection, and do not
disable verification.

## Commands

Use a fresh scratch directory for each edit. `get` refuses to overwrite an existing snapshot.

```sh
python3 scripts/confluence_adf.py get 123456 /tmp/edit-session/base.json
python3 scripts/confluence_adf.py put 123456 /tmp/edit-session/base.json /tmp/edit-session/new.json "Update the requested section"
python3 scripts/confluence_adf.py verify 123456 /tmp/edit-session/base.json /tmp/edit-session/new.json
```

Create the scratch directory first. `get` saves the site, page ID, title, status, published version,
native ADF, and appearance property values and versions. `put` and `verify` accept a complete ADF
document or a JSON object containing it under `adf` as the new file. Use the original snapshot as
the baseline; older snapshots without site identity need a fresh `get`.

`put` rejects a changed baseline or an accessible divergent draft, preserves the current title, and
submits the next published version. If the draft read fails, it stops before publication rather than
interpreting a missing or inaccessible response as proof that no draft exists. Opening a page in the
Cloud editor can leave a draft with `_parentId` and `_referencedContentId` added inside a macro's
`attrs.parameters.macroParams` and `__confluenceMetadata` added to a `link` mark or an `inlineCard`,
`blockCard` or `embedCard` node; a draft that differs only in those attributes holds no pending edit
and does not block. A draft with another title, or with other content, blocks publication. The error
names a title change or lists the differing JSON paths.

`put` rereads and verifies the saved page after writing, even when the successful PUT response body
is incomplete. `verify` performs the same checks without publishing. A mismatch returns a nonzero
exit status. An extra page version also fails, even when its body happens to match, because a later
edit cannot be attributed to this write.

ADF comparisons ignore mark order and keep node order, attributes, IDs, and marks significant, with
two exceptions: the draft check drops the editor metadata above, and the post-write check accepts
the stored page either as sent or with the final title segment dropped from every `link` mark's page
URL (`.../spaces/KEY/pages/123/Page+title` saved as `.../spaces/KEY/pages/123`). A stored link that
gains or changes a title still fails. So does a save that drops titles from only some links.

When the stored ADF matches neither the sent document nor its title-stripped form, `put` and
`verify` list the paths from whichever of those two comparisons has fewer entries. Draft and
verification reports show up to five paths, then `...`, without content. Keys are escaped as in JSON
Pointer (`~1` for `/`, `~0` for `~`) and as JSON strings. Macro paths stop at `attrs/parameters`,
mark indexes follow sorted mark order, not the file's order, and a `(length a -> b)` entry hides any
differences beneath that list.

When `put` or `verify` reports a stored ADF mismatch and every listed path, ignoring a trailing
`...`, ends in `/marks/N/attrs/href`, `get` the page into a new file and compare it locally with
`python3 -B`, not with the truncated report:

```python
import sys

sys.path.insert(0, "SCRIPT_DIR")  # this skill's scripts directory
from confluence_adf import differences, read_adf, without_page_link_titles

sent, stored = read_adf("new.json"), read_adf("stored.json")
dropped = differences(sent, stored)
kept = differences(without_page_link_titles(sent), stored)
```

Treat the stored ADF as matching only when every path in both lists ends in `/marks/N/attrs/href`,
no path appears in both lists, the title, version, and appearance checks passed, and `stored.json`
records the version the helper reported. A path in both lists is a link whose stored URL matches
neither form. State in the final report that the helper's check failed and what the local comparison
accepted.

The helper validates the document envelope, not every editor-specific node. Keep unfamiliar content
unchanged and use the service's validation for supported nodes.

The page body, appearance properties, and collaborative draft are separate server state. Version
conflicts protect the published body; they do not provide an atomic lock over all three. Appearance
drift is detected, not automatically repaired. On uncertain write results, read before retrying.

## API references

- [Page read and update API](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/):
  native body format, next-version updates, conflicts, and draft reconciliation.
- [Page content properties](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-content-properties/):
  appearance snapshots and pagination.
- [Basic authentication](https://developer.atlassian.com/cloud/confluence/basic-auth-for-rest-apis/):
  existing account email and API token authentication.
- [Scoped API tokens](https://support.atlassian.com/confluence/kb/scoped-api-tokens-in-confluence-cloud/):
  gateway context URLs and token scopes.
