import unittest
from unittest.mock import patch

import util


class ShieldPathTextTest(unittest.TestCase):
    def test_static_badge_path_syntax(self) -> None:
        self.assertEqual(util.shield_path_text("AT_arc222_f"), "AT__arc222__f")
        self.assertEqual(util.shield_path_text("A-B C"), "A--B_C")

    def test_render_escapes_only_badge_image_pid(self) -> None:
        config = {"site": {"blog_base_url": "https://lailai.one"}}
        with patch.object(util, "load_config", return_value=config):
            content = util.render_luogu_md("AT_arc222_f", "## 参考代码\n")

        self.assertIn("/badge/Luogu-AT__arc222__f-blue", content)
        self.assertIn("/problem/AT_arc222_f", content)
        self.assertIn("/blog/solution/AT_arc222_f", content)


class ClassifyTest(unittest.TestCase):
    def test_ignores_transport_newline(self) -> None:
        self.assertEqual(util.classify("badge\nbody\n", "badge\r\nbody"), "identical")

    def test_detects_badge_difference(self) -> None:
        self.assertEqual(util.classify("badge-a\n## 正文", "badge-b\n## 正文"), "substantive")


if __name__ == "__main__":
    unittest.main()
