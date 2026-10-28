import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.release_version import release_version


class ReleaseVersionTests(unittest.TestCase):
    def test_stable_tags(self):
        for tag, expected in {
            "0.0.0": "0.0.0",
            "1.2.3": "1.2.3",
            "v1.2.3": "1.2.3",
            "v0.10.20": "0.10.20",
            "12.345.6789": "12.345.6789",
        }.items():
            with self.subTest(tag=tag):
                self.assertEqual(release_version(tag), expected)

    def test_labels_and_non_semantic_tags_are_rejected(self):
        for tag in (
            "", "main", "1", "1.2", "1.2.3.4", "v", "vv1.2.3", "V1.2.3",
            "release-1.2.3", "01.2.3", "1.02.3", "1.2.03", "v01.2.3",
            "1.2.3-alpha", "v1.2.3-beta.1", "1.2.3-rc.1", "v1.2.3-rc.1",
            "1.2.3+build.4", "v1.2.3+build.4", "1.2.3-rc.1+build.4",
            "1.2.3-label", "1.2.3foo", "1.2.3-", "1.2.3+",
            " 1.2.3", "1.2.3 ", "1.2.3\n", "1.2.3\nversion=4.5.6", "١.2.3",
        ):
            with self.subTest(tag=tag):
                self.assertIsNone(release_version(tag))

    def test_github_output_and_branch_guard(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "release_version.py"
        for ref_type, tag, expected in (
            ("tag", "v1.2.3", "version=1.2.3\n"),
            ("tag", "1.2.3", "version=1.2.3\n"),
            ("tag", "v1.2.3-rc.1", "version=\n"),
            ("tag", "1.2.3+build", "version=\n"),
            ("branch", "1.2.3", "version=\n"),
        ):
            with self.subTest(ref_type=ref_type, tag=tag), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "output"
                subprocess.run(
                    [sys.executable, str(script)],
                    env={
                        **os.environ,
                        "GITHUB_REF_TYPE": ref_type,
                        "GITHUB_REF_NAME": tag,
                        "GITHUB_OUTPUT": str(output),
                    },
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(output.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
