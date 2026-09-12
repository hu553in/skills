# Managed sources

Use this guidance only when an explicit generation or synchronization mechanism manages fleet files.

The shared config or template repository is authoritative. Inspect its manifest to establish which
files and repositories it owns before editing targets. Edit the authoritative source first when
authorized; patch target copies only when explicitly requested or no central update mechanism
exists. If the source is outside the authorized scope, report the needed source change rather than
bypassing ownership. Target changes serve to verify what the source renders, not as a substitute for
updating it.

Preserve discoverable template names and layout with one consistent naming rule. Allow exceptions
when identical downstream filenames need distinguishable templates. Do not centralize files that
standard tooling generates or dependency automation updates unless the user explicitly accepts that
tradeoff.

Completion requires checking rendered variants, not just template text. Render representative
repositories for affected variants using the existing mechanism, checking whitespace-sensitive
formats and affected downstream contracts. Keep generation within authorized paths; narrow a broad
sync or seek authorization before it writes elsewhere. Report variants that could not be verified.
