import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")

def read_template(template_filename: str) -> str:
    """Reads a template file from the templates' directory."""
    filepath = os.path.join(TEMPLATES_DIR, template_filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def fill_template(template: str, data_to_replace: dict) -> str:
    """Replaces placeholders in a template string with values from repdata."""
    for placeholder, value in data_to_replace.items():
        template = template.replace(f"[{placeholder}]", str(value))
    return template
