from htmlnode import (
    LeafNode,
    html_tag_anchor,
    html_tag_blockquote,
    html_tag_bold,
    html_tag_image,
    html_tag_italic,
    html_tag_raw,
)

text_type_bold = "bold"
text_type_italic = "italic"
text_type_link = "link"
text_type_image = "image"
text_type_text = "text"
text_type_code = "code"

allowed_text_type = [
    text_type_bold,
    text_type_italic,
    text_type_text,
    text_type_image,
    text_type_code,
    text_type_link
]


def isAllowedTextType(text_type):
    return text_type in allowed_text_type


class TextNode:
    def __init__(self, text, text_type=text_type_text, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html_node(self):
        if self.text_type is text_type_text:
            return LeafNode(html_tag_raw, self.text)
        elif self.text_type is text_type_bold:
            return LeafNode(html_tag_bold, self.text)
        elif self.text_type is text_type_italic:
            return LeafNode(html_tag_italic, self.text)
        elif self.text_type is text_type_link:
            return LeafNode(html_tag_anchor, self.text, {"href": self.url})
        elif self.text_type is text_type_code:
            return LeafNode(html_tag_blockquote, self.text)
        elif self.text_type is text_type_image:
            return LeafNode(
                html_tag_image, "", {"src": self.url, "alt": self.text}
            )

        raise ValueError(f"Text Node {self} has no equivalent html tag")

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


