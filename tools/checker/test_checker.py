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
                "readme-centered-header",
                "readme-required-badges",
                "readme-language-separator",
                "readme-language-current",
                "project-tree-language",
                "project-tree-common",
                "project-tree-filename",
                "project-tree-align",
                "project-tree-order",
                "license-link",
                "license-wording",
            }.issubset(rules)
        )

    def test_readme_language_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text(
                '<p><strong>English</strong> · '
                '<a href="README.zh-Hans.md">简体中文</a></p>\n',
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(readme), OPTS)}
            self.assertFalse(any(rule.startswith("readme-language-") for rule in rules))

            readme_zh = Path(directory) / "README.zh-Hans.md"
            readme_zh.write_text(
                '<p><a href="README.md">English</a> · '
                '<strong>简体中文</strong></p>\n',
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(readme_zh), OPTS)}
            self.assertFalse(any(rule.startswith("readme-language-") for rule in rules))

            readme.write_text(
                '<p><strong>English</strong> · 简体中文</p>\n',
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(readme), OPTS)}
            self.assertIn("readme-language-links", rules)

    def test_command_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "启动.command"
            path.write_text("#!/bin/bash\n", encoding="utf-8")
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertIn("command-filename", rules)
            self.assertIn("path-filename-ascii", rules)

    def test_project_title_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(
                '<div align="center">\n  <h1>lailai-template</h1>\n</div>\n',
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertNotIn("project-title-case", rules)


if __name__ == "__main__":
    unittest.main()
