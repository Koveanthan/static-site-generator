import unittest

from htmlnode import *
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_url_none_check(self):
        node1 = TextNode("This is a test node", "bold")
        node2 = TextNode("This is a test node", "bold", None)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a test node2", "bold")
        node2 = TextNode("This is a test node", "bold")
        self.assertNotEqual(node1, node2)

    def test_text_to_html(self):
        node1 = TextNode("This is a text node", text_type_bold, "http://google.com")
        node2 = TextNode("This is a text node", text_type_link, "http://google.com")
        self.assertEqual(
            node1.to_html_node(),
            HTMLNode(html_tag_bold, "This is a text node"),
        )
        self.assertEqual(
            node2.to_html_node(),
            HTMLNode(
                html_tag_anchor,
                "This is a text node",
                None,
                {"href": "http://google.com"},
            ),
        )


if __name__ == "__main__":
    unittest.main()
