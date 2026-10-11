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
with the required page read/write scopes.

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
interpreting a missing or inaccessible response as proof that no draft exists. It rereads and
verifies the saved page after writing, even when the successful PUT response body is incomplete.
`verify` performs the same checks without publishing. A mismatch returns a nonzero exit status. An
extra page version also fails, even when its body happens to match, because a later edit cannot be
attributed to this write.

ADF checks ignore mark order but preserve node order, attributes, IDs, and marks themselves. The
helper validates the document envelope, not every editor-specific node. Keep unfamiliar content
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
