import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check


OPTS = {
    "aitone": True,
    "cjk_space": True,
    "sentence": True,
    "errors_only": False,
    "quiet": True,
}


class CheckerTest(unittest.TestCase):
    def test_readme_good(self):
        path = Path(__file__).parent / "tests" / "readme-good.md"
        self.assertEqual(check.check_file(str(path), OPTS), [])

    def test_readme_bad(self):
        path = Path(__file__).parent / "tests" / "readme-bad.md"
        rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
        self.assertTrue(
            {
                "project-title-case",
                "project-tree-language",
                "project-tree-common",
                "project-tree-filename",
                "project-tree-align",
                "project-tree-order",
                "license-link",
                "license-wording",
            }.issubset(rules)
        )

    def test_command_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "启动.command"
            path.write_text("#!/bin/bash\n", encoding="utf-8")
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertIn("command-filename", rules)
            self.assertIn("path-filename-ascii", rules)


if __name__ == "__main__":
    unittest.main()
