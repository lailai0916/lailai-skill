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

    def test_cpp_hard_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main.cpp"
            path.write_text(
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "inline int f(vector<int>& a)\n"
                "{\n"
                "\tfor (int x = 0; x < (int)a.size(); x++)cout << a[x];\n"
                "\treturn true;\n"
                "}\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertTrue(
                {
                    "cpp-storage",
                    "cpp-size-cast",
                    "cpp-reference-space",
                    "cpp-loop-name",
                    "cpp-keyword-space",
                    "cpp-operator-space",
                    "cpp-bool",
                }.issubset(rules)
            )

    def test_cpp_exact_layout_const_and_declaration_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main.cpp"
            path.write_text(
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "\n"
                "const int N=100005,mod=998244353;\n"
                "int a[N];\n"
                "\n"
                "int main()\n"
                "{\n"
                "\tint n,sum=0;\n"
                "\tcin>>n;\n"
                "\tfor(int i=1;i<=n;i++)sum+=i;\n"
                "\tcout<<sum<<'\\n';\n"
                "\treturn 0;\n"
                "}\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertTrue(
                {
                    "cpp-blank-layout",
                    "cpp-const-line",
                    "cpp-declaration-order",
                }.issubset(rules)
            )
            path.write_text(
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "\n"
                "const int N=100005;\n"
                "const int a[2]={1,2};\n"
                "int main()\n"
                "{\n"
                "\treturn 0;\n"
                "}\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertNotIn("cpp-const-line", rules)
            self.assertNotIn("cpp-blank-layout", rules)

    def test_display_math_hard_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "math.md"
            path.write_text(
                "这句话没有用冒号引出。\n\n"
                "$$\n"
                "f(x)=\\begin{cases}\n"
                "$$\n\n"
                "另一个公式如下：\n\n"
                "$$\n"
                "\\begin{cases}\n"
                "1,&x>0\n"
                "0\\  & d=0\\text{ 且 }x\\le0.\n"
                "\\end{cases}\n"
                "$$\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertTrue(
                {
                    "math-display-intro",
                    "math-display-terminal",
                    "math-environment-line",
                    "math-environment-indent",
                    "math-environment-break",
                    "math-align-space",
                    "math-manual-space",
                    "math-structural-cjk",
                }.issubset(rules)
            )


if __name__ == "__main__":
    unittest.main()
