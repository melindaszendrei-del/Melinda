#!/usr/bin/env python3
"""Trinity Guard v0.1 — read-only integrity and publication-scope verifier.

IMPORTANT: detects unauthorized drift only when GitHub Actions actually runs
this code. It cannot stop direct pushes/deletions without GitHub rulesets.
A writer could alter this script + in-repo manifest together; keep an
independent witness copy of manifest and commit SHA outside the repository.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MANIFEST_PATH = "security/guard_manifest.json"
BAD_PREFIXES = ("private/", "onedrive/", "secrets/", "archive/raw/", "unpublished/")
BAD_SUFFIXES = (".env", ".pem", ".key", ".p12", ".pfx", ".zip", ".7z", ".tar", ".docx", ".pdf")
CERTIFICATE_PREFIX = "research/trinity/certificates/"
SHA1 = re.compile(r"^[0-9a-f]{40}$")


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def check(repo: Path, manifest_file: Path | None = None) -> list[str]:
    """Fail closed on missing manifest, unapproved paths and blob mismatches."""
    repo = repo.resolve()
    manifest_file = manifest_file or (repo / MANIFEST_PATH)
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"MANIFEST_UNREADABLE: {exc}"]
    if manifest.get("schema") != 1 or manifest.get("hash_algorithm") != "git-blob-sha1":
        return ["MANIFEST_SCHEMA_INVALID"]
    locks = manifest.get("locked_blobs")
    if not isinstance(locks, dict) or not locks:
        return ["MANIFEST_LOCKS_INVALID"]
    if not all(isinstance(p, str) and isinstance(h, str) and SHA1.fullmatch(h) for p, h in locks.items()):
        return ["MANIFEST_ENTRY_INVALID"]
    if MANIFEST_PATH in locks:
        return ["MANIFEST_SELF_HASH_FORBIDDEN"]
    try:
        tracked = set(p.decode("utf-8") for p in git(repo, "ls-files", "-z").split(b"\0") if p)
    except (UnicodeError, subprocess.CalledProcessError) as exc:
        return [f"GIT_TRACKING_UNAVAILABLE: {exc}"]
    permitted = set(locks) | {MANIFEST_PATH}
    for p in sorted(tracked - permitted):
        errors.append(f"UNAPPROVED_TRACKED_FILE: {p}")
    for p in sorted(permitted - tracked):
        errors.append(f"LOCKED_FILE_MISSING: {p}")
    for path in sorted(tracked):
        norm = path.lower()
        if path.startswith("/") or ".." in Path(path).parts or "\\" in path:
            errors.append(f"UNSAFE_PATH: {path}")
        if norm.startswith(BAD_PREFIXES) or norm.endswith(BAD_SUFFIXES):
            errors.append(f"PRIVATE_OR_BINARY_PUBLICATION_BLOCKED: {path}")
        if norm.startswith(CERTIFICATE_PREFIX):
            errors.append(f"PRODUCTION_CERTIFICATE_NOT_AUTHORIZED: {path}")
        fp = repo / path
        if fp.is_symlink() or not fp.is_file():
            errors.append(f"NONREGULAR_FILE: {path}")
        if path in locks and fp.is_file() and not fp.is_symlink():
            try:
                actual = git(repo, "hash-object", "--no-filters", "--", path).decode("ascii").strip()
            except (UnicodeError, subprocess.CalledProcessError) as exc:
                errors.append(f"HASH_UNAVAILABLE: {path}: {exc}")
                continue
            if actual != locks[path]:
                errors.append(f"INTEGRITY_DRIFT: {path} expected={locks[path]} actual={actual}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--manifest", type=Path)
    args = p.parse_args()
    issues = check(args.repo, args.manifest)
    if issues:
        print("TRINITY_GUARD: DENY (CI/report only; NOT server-side protection)")
        for issue in issues:
            print(" -", issue)
        return 1
    print("TRINITY_GUARD: PASS (locked Git blobs match this in-repo manifest)")
    print("This is an integrity witness; it does NOT enforce GitHub write permissions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
