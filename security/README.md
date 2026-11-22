# Trinity Guard v0.1 — self-managed integrity witness

Based on CHRONOS–FISM (origin, fail-closed), Docker #575 information-flow labeling, and Trinity GAP-F soundness distinctions. **This is a new GitHub-specific implementation, not a deployed MCP Gateway or complete proof checker.**

## What it actually does
- Lists every tracked path and denies unregistered or missing paths.
- Checks the contents of every locked file against a pinned Git object SHA-1.
- Denies tracked material under private/onedrive/secrets/archive/raw/unpublished, secret-key-like suffixes, and any unreviewed production certificate path.
- Runs nine independent failure-injection unit tests (tampered file, unapproved file, private path, fake certificate, missing file, invalid manifest, etc.).
- Keeps the TP01 proof lab, Trinity examples and security code immutable **relative to the committed manifest**.
- Runs with read-only GitHub Actions permissions and **no secrets**.

## HARD LIMITATION (do not misinterpret)
An actor with direct write permission can modify the in-repo manifest, workflows and guard in one commit or disable Actions, force-push or delete unprotected branches. Therefore **this is detection, not an immutable GitHub lock**. GitHub rulesets/branch protection and independently controlled witnessed backups are required for true write prevention. CODEOWNERS alone does not block commits.

## Changing a locked file legitimately
Use a new versioned path whenever possible. If a change is indispensable, update the manifest after review. Compare against an independent copy of the previous manifest and commit SHA, **stored outside the GitHub repository**. A manifest whose SHA matches itself is no security guarantee.

## External witness
Record the protected branch head commit SHA, pinned object hashes and downloaded archival ZIP in a separate account/device. Review unexpected GitHub activity in the repository's audit/security settings.

## Proof status
Passing this guard authorizes neither WTT nor TF-REG-1, nor an RH proof. It verifies content identity and public-file scope only; mathematical correctness must be established separately.
