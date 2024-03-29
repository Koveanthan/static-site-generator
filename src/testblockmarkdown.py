import unittest

from blockmarkdown import (
    block_to_block_type,
    block_type_code,
    block_type_unordered_list,
    markdown_to_block,
    markdown_to_html,
)


class TestMarkBlockDown(unittest.TestCase):


    def test_markdown_to_block(self):
        self.assertEqual(
            markdown_to_block(
                "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n\n* This is a list\n* with items"
            ),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("```This is a quote\nfrom\nRobert D Wilde```"),
            block_type_code,
        )
        self.assertEqual(
            block_to_block_type("* This is a line\n*This is also a line"),
            block_type_unordered_list,
        )

    def test_block_to_markdown(self):
        # self.maxDiff = None
        self.assertEqual(
            markdown_to_html(
                "# This is bolded paragraph\n\n## This is another paragraph with italic text and code here\n\n```This is the same paragraph on a new line```\n\n"
            ),
            "<div><h1>This is bolded paragraph</h1><h2>This is another paragraph with italic text and code here</h2><code>This is the same paragraph on a new line</code></div>",
        )
        self.assertEqual(
            markdown_to_html(
                "# This is **bolded** paragraph\n\n## This is another paragraph with *italic* text and `code` here\n\n```This is the same paragraph on a new line```\n\n\n* This is a list\n* with items"
            ),
            "<div><h1>This is <b>bolded</b> paragraph</h1><h2>This is another paragraph with <i>italic</i> text and <blockquote>code</blockquote> here</h2><code>This is the same paragraph on a new line</code><ul><li>This is a list</li><li>with items</li></ul></div>",
        )
