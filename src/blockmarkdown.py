import re

from htmlnode import (
    LeafNode,
    ParentNode,
    html_tag_blockquote,
    html_tag_code,
    html_tag_div,
    html_tag_h1,
    html_tag_h2,
    html_tag_h3,
    html_tag_h4,
    html_tag_h5,
    html_tag_h6,
    html_tag_list,
    html_tag_paragraph,
    html_tag_unordered_list,
)
from inlinemarkdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_quote = "quote"


def markdown_to_block(markdown):
    blocks = []
    split_to_lines = markdown.split("\n")

    block = ""
    for line in split_to_lines:
        line = line.strip()
        if line == "":
            if not block == "":
                blocks.append(block)
                block = ""
        else:
            if block == "":
                block += line
            else:
                block += "\n" + line

    if not block == "":
        blocks.append(block)

    return blocks


def is_heading_block(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if not re.match(r"^#{1,6}\s", line):
            return False

    return True


def is_quote_block(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if not re.match(r"^>", line):
            return False

    return True


def is_ol_block(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if not re.match(r"^[0-9]+\.", line):
            return False

    return True


def is_ul_block(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if not re.match(r"^[*-]", line):
            return False

    return True


def is_code_block(markdown):
    lines = markdown.split("\n")

    if re.match(r"^```", lines[0]) and re.search(r"```$", lines[-1]):
        return True

    return False


def block_to_block_type(markdown):
    markdown = markdown.strip()
    if is_quote_block(markdown):
        return block_type_quote
    elif is_ol_block(markdown):
        return block_type_ordered_list
    elif is_ul_block(markdown):
        return block_type_unordered_list
    elif is_code_block(markdown):
        return block_type_code
    elif is_heading_block(markdown):
        return block_type_heading
    return block_type_paragraph


def text_to_htmlnodes(text):
    child_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        child_nodes.append(text_node.to_html_node())
    return child_nodes


def block_quote_to_html(block_text):
    split_lines = block_text.split("\n")
    html_text = ""

    for line in split_lines:
        html_text += line.split("> ")[1]

    return ParentNode(html_tag_blockquote, text_to_htmlnodes(html_text))


def block_ul_to_html(block_text):
    split_lines = block_text.split("\n")

    ul = ParentNode(html_tag_unordered_list, [])
    for line in split_lines:
        if line.startswith("* "):
            ul.add_child(
                ParentNode(html_tag_list, text_to_htmlnodes(line.split("* ")[1]))
            )
        elif line.startswith("- "):
            ul.add_child(
                ParentNode(html_tag_list, text_to_htmlnodes(line.split("- ")[1]))
            )

    return ul


def block_ol_to_html(block_text):
    split_lines = block_text.split("\n")

    ol = ParentNode(html_tag_unordered_list)
    for line in split_lines:
        ol.add_child(
            ParentNode(
                html_tag_list, text_to_htmlnodes(re.split(r"^[0-9]+\.\s", line)[1])
            )
        )

    return ol


def block_code_to_html(block_text):
    html_text = re.split(r"```$", re.split(r"^```", block_text)[1])[0]
    return ParentNode(html_tag_code, text_to_htmlnodes(html_text))


def block_heading_to_html(block_text):
    if re.match(r"^#\s", block_text):
        return ParentNode(html_tag_h1, text_to_htmlnodes(block_text.split("# ")[1]))
    elif re.match(r"^##\s", block_text):
        return ParentNode(html_tag_h2, text_to_htmlnodes(block_text.split("## ")[1]))
    elif re.match(r"^###\s", block_text):
        return ParentNode(html_tag_h3, text_to_htmlnodes(block_text.split("### ")[1]))
    elif re.match(r"^####\s", block_text):
        return ParentNode(html_tag_h4, text_to_htmlnodes(block_text.split("#### ")[1]))
    elif re.match(r"^#####\s", block_text):
        return ParentNode(html_tag_h5, text_to_htmlnodes(block_text.split("##### ")[1]))
    else:
        return ParentNode(
            html_tag_h6, text_to_htmlnodes(block_text.split("###### ")[1])
        )


def block_paragraph_to_html(block_text):
    return ParentNode(html_tag_paragraph, text_to_htmlnodes(block_text))


def markdown_to_html(markdown):
    blocks = markdown_to_block(markdown)
    div = ParentNode(html_tag_div)

    for block in blocks:
        if is_code_block(block):
            div.add_child(block_code_to_html(block))
        elif is_quote_block(block):
            div.add_child(block_quote_to_html(block))
        elif is_heading_block(block):
            div.add_child(block_heading_to_html(block))
        elif is_ol_block(block):
            div.add_child(block_ol_to_html(block))
        elif is_ul_block(block):
            div.add_child(block_ul_to_html(block))
        else:
            div.add_child(block_paragraph_to_html(block))

    return div.to_html()
