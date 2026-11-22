# GitHub security and research provenance

The repository is **PUBLIC**. Do not upload private OneDrive documents, personal data, secrets, or unpublished source material without explicit publication approval.

Recommended repository controls (configure as owner in GitHub Settings):
1. Ruleset/branch protection on `main` and `research/tp01-kw-formcore`; disallow force pushes and deletion.
2. Require pull requests and passing Lean/Trinity checks before merging; do not grant bypass to third-party automation accounts.
3. Use least-privilege credentials: read-only for reviewing agents; narrow write scope for approved changes.
4. Require two-factor authentication; audit installed GitHub Apps and granted repository permissions.
5. Maintain an **independent offline/exported copy**; Git history is not a backup against destructive administrators, force pushes or account compromise.
6. Preserve historical checkpoints as immutable tagged releases with checksums, only after full verification.

Current limitation: the connected GitHub tool can prepare branches and pull requests, but has **no enabled administrative action to activate branch protection**. A branch being named `research/...` or a draft PR does NOT by itself protect files.
