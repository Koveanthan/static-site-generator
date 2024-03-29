import unittest

from inlinemarkdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_delimiter(self):
        nodes1 = split_nodes_delimiter(
            [TextNode("'Code': This is a 'code'", text_type_text)
             ], "'", text_type_code
        )
        self.assertEqual(
            nodes1,
            [
                TextNode("Code", text_type_code),
                TextNode(": This is a ", text_type_text),
                TextNode("code", text_type_code),
            ],
        )

        nodes2 = split_nodes_delimiter(
            [TextNode("Code: This is a code", text_type_text)
             ], "'", text_type_code
        )
        self.assertEqual(
            nodes2,
            [
                TextNode("Code: This is a code", text_type_text),
            ],
        )

    def test_extract_images(self):
        self.assertEqual(
            extract_markdown_images(
                "This is a text with two images - \
                ![Google](http://www.google.com) and \
                ![Yahoo](http://yahoo.com)"
            ),
            (("Google", "http://www.google.com"), ("Yahoo", "http://yahoo.com")),
        )

    def test_extract_links(self):
        self.assertEqual(
            extract_markdown_links(
                "This is a text with two images - \
                [Google Link](http://www.google.com) and \
                [Yahoo Link](http://yahoo.com)"
            ),
            (
                ("Google Link", "http://www.google.com"),
                ("Yahoo Link", "http://yahoo.com"),
            ),
        )

    def test_split_links(self):
        node1 = split_nodes_links(
            [TextNode("This is a links - http://www.google.com test", text_type_text)]
        )
        node2 = split_nodes_links(
            [
                TextNode(
                    "This is a [links](http://www.google.com) test [end](http://www.end.com)",
                    text_type_text,
                )
            ]
        )

        self.assertEqual(
            node1,
            [
                TextNode("This is a links - http://www.google.com test", text_type_text),
            ],
        )
        self.assertEqual(
            node2,
            [
                TextNode("This is a ", text_type_text),
                TextNode("links", text_type_link, "http://www.google.com"),
                TextNode(" test ", text_type_text),
                TextNode("end", text_type_link, "http://www.end.com"),
            ],
        )

    def test_split_images(self):
        node1 = split_nodes_images(
            [
                TextNode(
                    "This is a images - http://www.google.com test", text_type_text
                )
            ]
        )
        node2 = split_nodes_images(
            [
                TextNode(
                    "This is a ![images](http://www.google.com) test ![end](http://www.end.com)",
                    text_type_text,
                )
            ]
        )

        self.assertEqual(
            node1,
            [
                TextNode("This is a images - http://www.google.com test", text_type_text),
            ],
        )
        self.assertEqual(
            node2,
            [
                TextNode("This is a ", text_type_text),
                TextNode("images", text_type_image, "http://www.google.com"),
                TextNode(" test ", text_type_text),
                TextNode("end", text_type_image, "http://www.end.com"),
            ],
        )


def test_text_to_node(self):
    self.assertEqual(
        text_to_textnodes(
            "This is a **bold text* plus an *italic text* with `code`. Now finally there are ![images](http://images.com) and [links to read](http://linkstoread.com)"
        ),
        [
            TextNode("This is a ", text_type_text),
            TextNode("bold text", text_type_bold),
            TextNode(" plus an ", text_type_text),
            TextNode("italic text", text_type_italic),
            TextNode(" with ", text_type_code),
            TextNode("code", text_type_code),
            TextNode(". Now finally there are ", text_type_text),
            TextNode("images", text_type_image, "http://images.com"),
            TextNode(" and ", text_type_text),
            TextNode("links to read", text_type_link,
                     "http://linkstoread.com"),
        ],
    )
