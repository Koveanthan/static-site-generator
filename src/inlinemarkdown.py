import re


from textnode import (
    TextNode,
    isAllowedTextType,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)

markdown_delimiters = {
    text_type_bold: "**",
    text_type_italic: "*",
    text_type_code: "`",
    text_type_image: "![]()",
    text_type_link: "[]()",
}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:

        if old_node.text_type is not text_type_text and isAllowedTextType(
            old_node.text_type
        ):
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("Invalid markdown syntax")

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if not i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], text_type))
            else:
                new_nodes.append(TextNode(split_text[i], text_type_text))

    return new_nodes


def extract_markdown_images(text):
    result = ()
    matches = re.findall(r"\!\[[\w\s]+\]\([\w:/.-_]+\)", text)

    for i in range(len(matches)):
        alt_text = matches[i].split("![")[1].split("]")[0]
        src_link = matches[i].split("(")[1].split(")")[0]
        result += ((alt_text, src_link),)

    return result


def extract_markdown_links(text):
    result = ()
    matches = re.findall(r"(?<!!)\[[\w\s]+\]\([\w:/.-_]+\)", text)

    for i in range(len(matches)):
        value = matches[i].split("[")[1].split("]")[0]
        href = matches[i].split("(")[1].split(")")[0]
        result += ((value, href),)

    return result


def append_if_not_empty(node_list, node_text, node_type, node_url=None):
    if node_text == "":
        return

    node_list.append(TextNode(node_text, node_type, node_url))


def split_nodes_images(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not text_type_text and isAllowedTextType(
            old_node.text_type
        ):
            new_nodes.append(old_node)
            continue

        links = extract_markdown_images(old_node.text)
        links_count = len(links)

        if links_count > 0:
            for link in links:
                split_text = old_node.text.split(f"![{link[0]}]({link[1]})", 1)

                append_if_not_empty(new_nodes, split_text[0], text_type_text)
                append_if_not_empty(new_nodes, link[0], text_type_image, link[1])

                if links_count == len(split_text) - 1:
                    append_if_not_empty(new_nodes, split_text[1], text_type_text)
                else:
                    old_node = TextNode(split_text[1], text_type_text)
                    links_count -= 1
        else:
            new_nodes.append(old_node)

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not text_type_text and isAllowedTextType(
            old_node.text_type
        ):
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        links_count = len(links)

        if links_count > 0:
            for link in links:
                split_text = old_node.text.split(f"[{link[0]}]({link[1]})", 1)

                append_if_not_empty(new_nodes, split_text[0], text_type_text)
                append_if_not_empty(new_nodes, link[0], text_type_link, link[1])

                if links_count == len(split_text) - 1:
                    append_if_not_empty(new_nodes, split_text[1], text_type_text)
                else:
                    old_node = TextNode(split_text[1], text_type_text)
                    links_count -= 1
        else:
            new_nodes.append(old_node)

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]

    for delim in markdown_delimiters:
        if delim == text_type_image:
            nodes = split_nodes_images(nodes)
        elif delim == text_type_link:
            nodes = split_nodes_links(nodes)
        else:
            nodes = split_nodes_delimiter(
                nodes, markdown_delimiters[delim], delim)
    return nodes
