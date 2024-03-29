import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    html_tag_anchor,
    html_tag_blockquote,
    html_tag_bold,
    html_tag_image,
    html_tag_italic,
    html_tag_paragraph,
    html_tag_raw,
    html_tag_div
)

from contextlib import redirect_stdout
import sys


class HTMLNodeTest(unittest.TestCase):
    def test_tag_not_defined(self):
        # print(f"__main__ {__name__}")
        self.assertRaises(ValueError, lambda: HTMLNode("h11"))

    def test_empty_param(self):
        self.assertEqual(
            HTMLNode(html_tag_bold, "text"), HTMLNode(
                html_tag_bold, "text", None, {})
        )

    def test_props_format(self):
        node = HTMLNode(
            html_tag_paragraph, "value", None, {
                "font": "Verdana", "font-size": "12px"}
        )
        self.assertEqual(node.props_to_html(),
                         ' font="Verdana" font-size="12px"')


class TestLeafNode(unittest.TestCase):
    def test_raw_value(self):
        # print("This is a print statememt in leaf node")
        self.assertEqual(
            LeafNode(value="This is a raw value").to_html(
            ), "This is a raw value"
        )

    def test_no_child(self):
        self.assertRaises(ValueError, lambda: LeafNode(child="p"))

    def test_html(self):
        self.assertEqual(
            LeafNode(
                html_tag_paragraph,
                "This is a paragraph",
                {"font-size": "12px", "font-family": "Verdana"},
            ).to_html(),
            '<p font-size="12px" font-family="Verdana">This is a paragraph</p>',
        )

    def test_html_image(self):
        self.assertEqual(
            LeafNode(
                html_tag_image,
                "",
                {
                    "src": "http://www.images.com",
                    "alt": "Image downloaded from images.com",
                },
            ).to_html(),
            '<img src="http://www.images.com" alt="Image downloaded from images.com"/>',
        )


class TestParentNode(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(
            ParentNode(
                html_tag_paragraph,
                [
                    LeafNode(html_tag_raw, "This is a "),
                    LeafNode(html_tag_bold, "bold "),
                    LeafNode(html_tag_italic, "italic text"),
                ],
                {"id": "para_id", "custom": "custom"},
            ).to_html(),
            '<p id="para_id" custom="custom">This is a <b>bold </b><i>italic text</i></p>',
        )

# with redirect_stdout(sys.stdout):
#     print(f"Stdout redirected to sysout {__name__}")
