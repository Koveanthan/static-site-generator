import os
import re

from blockmarkdown import markdown_to_html


def extract_title(markdown):
    if re.search(r"^#\s", markdown):
        return markdown.split("# ")[1].split("\n")[0]
    else:
        raise ValueError("No header present in markdown")


def generate_pages(from_path, template_path, to_path):
    if not from_path.startswith(os.getcwd()):
        from_path = os.path.join(os.getcwd(), from_path)
    if not template_path.startswith(os.getcwd()):
        template_path = os.path.join(os.getcwd(), template_path)
    if not to_path.startswith(os.getcwd()):
        to_path = os.path.join(os.getcwd(), to_path)

    dirs = os.listdir(from_path)
    print(f"Dirs for {from_path} is {dirs}")
    for dir in dirs:
        if os.path.isdir(os.path.join(from_path, dir)):
            if not os.path.exists(os.path.join(to_path, dir)):
                os.mkdir(os.path.join(to_path, dir))
            generate_pages(
                os.path.join(from_path, dir),
                template_path,
                os.path.join(to_path, dir),
            )
        else:
            from_file_path = os.path.join(from_path, dir)
            to_file_path = os.path.join(to_path, dir).replace(".md", ".html")

            print(
                f"Generating a page from {from_file_path} to {to_file_path} using {template_path}"
            )

            markdown_text = get_text(from_file_path)
            template_text = get_text(template_path)
            html_body = markdown_to_html(markdown_text)
            title = extract_title(markdown_text)

            html_text = template_text.replace("{{ Title }}", title).replace(
                "{{ Content }}", html_body
            )

            with open(to_file_path, "a") as f:
                f.write(html_text)

            print(f"Your {to_file_path} is successfully written")


def get_text(from_path):
    with open(from_path) as f:
        return f.read()
