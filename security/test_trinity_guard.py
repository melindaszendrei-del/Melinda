"""Regression tests for Trinity Guard integrity witness, no network required."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from trinity_guard import check, MANIFEST_PATH


def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], stderr=subprocess.PIPE).decode().strip()


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "user.name", "Fixture")
        (self.root / "security").mkdir()
        (self.root / "README.md").write_text("Public fixture\n", encoding="utf-8")
        h = git(self.root, "hash-object", "--no-filters", "README.md")
        (self.root / MANIFEST_PATH).write_text(json.dumps({
            "schema": 1, "hash_algorithm": "git-blob-sha1", "locked_blobs": {"README.md": h}
        }), encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "fixture")

    def tearDown(self):
        self.t.cleanup()

    def test_good(self):
        self.assertEqual(check(self.root), [])

    def test_modified_content_rejected(self):
        (self.root / "README.md").write_text("tampered\n")
        self.assertTrue(any("INTEGRITY_DRIFT" in v for v in check(self.root)))

    def test_unapproved_path_rejected(self):
        (self.root / "unexpected.txt").write_text("unknown")
        git(self.root, "add", "unexpected.txt")
        self.assertTrue(any("UNAPPROVED" in v for v in check(self.root)))

    def test_private_path_rejected(self):
        (self.root / "private").mkdir()
        (self.root / "private" / "notes.txt").write_text("restricted")
        git(self.root, "add", "private/notes.txt")
        self.assertTrue(any("PRIVATE_OR_BINARY" in v for v in check(self.root)))

    def test_certificate_claim_rejected(self):
        folder = self.root / "research" / "trinity" / "certificates"
        folder.mkdir(parents=True)
        (folder / "unverified.json").write_text('{"issuedStatus":"PASS"}')
        git(self.root, "add", "research/trinity/certificates/unverified.json")
        self.assertTrue(any("PRODUCTION_CERTIFICATE_NOT_AUTHORIZED" in v for v in check(self.root)))

    def test_missing_locked_file_rejected(self):
        (self.root / "README.md").unlink()
        self.assertTrue(any("LOCKED_FILE_MISSING" in v for v in check(self.root))
                     or any("NONREGULAR_FILE" in v for v in check(self.root)))

    def test_deleted_manifest_rejected(self):
        (self.root / MANIFEST_PATH).unlink()
        self.assertTrue(any("MANIFEST_UNREADABLE" in v for v in check(self.root)))

    def test_invalid_manifest_rejected(self):
        (self.root / MANIFEST_PATH).write_text('{"schema":1,"hash_algorithm":"sha256","locked_blobs":{}}')
        self.assertTrue(any("MANIFEST_SCHEMA_INVALID" in v for v in check(self.root)))

    def test_self_hash_rejected(self):
        manifest = json.loads((self.root / MANIFEST_PATH).read_text())
        manifest["locked_blobs"][MANIFEST_PATH] = "0" * 40
        (self.root / MANIFEST_PATH).write_text(json.dumps(manifest))
        self.assertTrue(any("MANIFEST_SELF_HASH_FORBIDDEN" in v for v in check(self.root)))


if __name__ == "__main__":
    unittest.main()
