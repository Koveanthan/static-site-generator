import traceback

html_tag_paragraph = "p"
html_tag_anchor = "a"
html_tag_image = "img"
html_tag_bold = "b"
html_tag_italic = "i"
html_tag_blockquote = "blockquote"
html_tag_raw = "raw"
html_tag_ordered_list = "ol"
html_tag_unordered_list = "ul"
html_tag_list = "li"
html_tag_div = "div"
html_tag_h1 = "h1"
html_tag_h2 = "h2"
html_tag_h3 = "h3"
html_tag_h4 = "h4"
html_tag_h5 = "h5"
html_tag_h6 = "h6"
html_tag_code = "code"

allowed_html_tags = {
    html_tag_paragraph,
    html_tag_anchor,
    html_tag_italic,
    html_tag_image,
    html_tag_bold,
    html_tag_blockquote,
    html_tag_raw,
    html_tag_ordered_list,
    html_tag_unordered_list,
    html_tag_list,
    html_tag_div,
    html_tag_h1,
    html_tag_h2,
    html_tag_h3,
    html_tag_h4,
    html_tag_h5,
    html_tag_h6,
    html_tag_code,
}


def is_allowed_html_tag(tag):
    if tag in allowed_html_tags:
        return True
    return False


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        tag = html_tag_raw if tag is None else tag
        if is_allowed_html_tag(tag):
            self.tag = tag
        else:
            raise ValueError(f"HTML tag  {tag} is not supported")

        self.value = value
        self.children = children

        if props is None:
            props = {}
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result = ""
        for key in self.props:
            result += f' {key}="{self.props[key]}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None, child=None):
        if value is None:
            raise ValueError("Value cannot be None")
        if child is not None:
            raise ValueError("Child cannot have value")

        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is html_tag_raw:
            return self.value
        elif self.tag is html_tag_image:
            return f"<{self.tag}{self.props_to_html()}/>"
        # TODO: Should we also check for the img to have a "" value?
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children=None,  props=None, value=None):
        if value is not None:
            return ValueError("Parent node cannot have value")

        if tag is None:
            return ValueError("Parent node should have a tag")

        if children is None:
            children = []

        super().__init__(tag, value, children, props)

    def add_child(self, child):
        self.children.append(child)

    def to_html(self):
        start_tag = f"<{self.tag}{self.props_to_html()}>"
        end_tag = f"</{self.tag}>"
        content = ""
        for child in self.children:
            content += child.to_html()
        return start_tag + content + end_tag
