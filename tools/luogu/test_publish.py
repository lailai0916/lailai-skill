import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import publish


class DiffOnlyTest(unittest.TestCase):
    @patch.object(publish, "LuoguClient")
    def test_reports_badge_difference(self, client_class) -> None:
        client_class.return_value.get_article.return_value = {
            "content": "old-badge\n\n## 正文",
            "contentFull": True,
        }
        source = {
            "pid": "AT_arc222_f",
            "lid": "1",
            "luogu_content": "new-badge\n\n## 正文",
        }

        output = io.StringIO()
        with redirect_stdout(output):
            result = publish.diff_only(source)

        self.assertEqual(result, 0)
        self.assertIn("分类: substantive", output.getvalue())
        self.assertIn("-old-badge", output.getvalue())
        self.assertIn("+new-badge", output.getvalue())


if __name__ == "__main__":
    unittest.main()
