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
    def test_sentence_length_is_advisory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "long-sentence.md"
            path.write_text("这是一句用于验证长句只产生建议而不会成为错误的中文句子，它会故意超过六十个字符，但内容仍然保持完整，并继续补充少量文字以越过原有阈值。\n", encoding="utf-8")
            issues = check.check_file(str(path), OPTS)
            self.assertTrue(any(issue.rule == "sentence-length" for issue in issues))
            self.assertFalse(any(issue.level == "ERROR" for issue in issues))

    def test_laiism_brand_is_lowercase(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            for title in ("laiism", "laiism".capitalize(), "laiism".upper()):
                path.write_text(
                    '<div align="center">\n  <h1>{}</h1>\n</div>\n'.format(title),
                    encoding="utf-8",
                )
                rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
                self.assertEqual("project-brand-case" in rules, title != "laiism")
            path = Path(directory) / "note.md"
            path.write_text("About " + "laiism".capitalize() + ".\n", encoding="utf-8")
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertIn("project-brand-case", rules)

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

    def test_cpp_constant_names_and_c_io(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main.cpp"
            path.write_text(
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "\n"
                "const int INF=0x3f3f3f3f;\n"
                "const int MOD=998244353;\n"
                "int main()\n"
                "{\n"
                "\tint x=getchar_unlocked();\n"
                "\tfwrite(&x,sizeof x,1,stdout);\n"
                "\treturn 0;\n"
                "}\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertTrue({"cpp-constant-name", "cpp-c-io"}.issubset(rules))

    def test_cpp_personal_idiom_names(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main.cpp"
            path.write_text(
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "\n"
                "long long qpow(long long x,long long y){return 1;}\n"
                "struct Fenwick{};\n"
                "int main()\n"
                "{\n"
                "\treturn 0;\n"
                "}\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertIn("cpp-personal-idiom", rules)

    def test_cpp_newline_string_does_not_cross_literal_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "main.cpp"
            path.write_text(
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "\n"
                "int main()\n"
                "{\n"
                "\tcout<<\"YES\"<<'\\n';\n"
                "\treturn 0;\n"
                "}\n",
                encoding="utf-8",
            )
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertNotIn("cpp-newline-in-str", rules)
            path.write_text(path.read_text(encoding="utf-8").replace("<<'\\n'", "<<\"\\n\""), encoding="utf-8")
            rules = {issue.rule for issue in check.check_file(str(path), OPTS)}
            self.assertIn("cpp-newline-in-str", rules)

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
