# GitHub metadata

Use this guidance when repository metadata, tags, or releases are in scope. Reads and proposals do
not authorize remote changes. Obtain independent authorization for the specific remote operation;
local cleanup approval is not enough.

Capture current metadata for each scoped repository before proposing or applying changes:

```sh
gh repo view OWNER/REPO --json description,repositoryTopics,homepageUrl,isPrivate,url
```

- Descriptions are concise taglines without final punctuation, not full README sentences. Avoid
  volatile tool lists or implementation details; do not lengthen them just to mirror a README.
- Topics are stable, lowercase slug-like terms. Prefer broad, durable topics over every dependency.
- Preserve homepage and visibility unless changes to those fields are explicitly authorized.
- For proposal-first requests, provide a table with `repo`, `current`, `proposed`, and `changed`,
  then stop until confirmation.

Apply only approved fields and repositories. Verify remote state afterward: descriptions have no
trailing punctuation, topics match `^[a-z0-9][a-z0-9-]*$`, and the resulting values match the
approved change. Report failures or unverified state, not success inferred from a write command's
exit code.

## Tags and releases

Tag or release cleanup is destructive and requires an explicit request for that operation. Do not
infer it from metadata or local release-config cleanup. Verify the relevant state before and after
using `gh release list` and `git ls-remote --tags` against the intended repository/remote. Limit
deletion to authorized targets; stop for a scope decision if targets are ambiguous or state differs
from what was approved. Report what changed and what remains.
