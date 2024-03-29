from copystatic import copy_static
from markdowntohtml import generate_pages

copy_static("static", "public")
generate_pages(
    "content",
    "template.html",
    "public",
)
