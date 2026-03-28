"""Template loading and placeholder substitution utilities."""

import os
from collections.abc import Mapping

TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "templates"
)


def read_template(template_filename: str) -> str:
    """Read a JavaScript template file from the templates directory.

    :param template_filename: The file name of the template
        (e.g. ``hook_function.js``).
    :return: The raw template content as a string.
    """
    filepath = os.path.join(TEMPLATES_DIR, template_filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def fill_template(template: str, data_to_replace: Mapping[str, str | int]) -> str:
    """Replace ``[PLACEHOLDER]`` tokens in a template with actual values.

    :param template: The template string containing placeholders.
    :param data_to_replace: A mapping of placeholder names (without
        brackets) to their replacement values.
    :return: The filled template string.
    """
    for placeholder, value in data_to_replace.items():
        template = template.replace(f"[{placeholder}]", str(value))
    return template
