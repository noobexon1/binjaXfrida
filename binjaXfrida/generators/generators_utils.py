import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")

def load_template(template_filename: str) -> str:
    """Loads a template file from the templates' directory."""
    filepath = os.path.join(TEMPLATES_DIR, template_filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        error_msg = f"// [binjaXfrida] Error: Could not load template from {template_filename}\n// {e}"
        print(error_msg.replace("// ", ""))
        return error_msg

def fill_template(template_content: str, repdata: dict) -> str:
    """Replaces placeholders in a template string with values from repdata."""
    s = template_content
    for key, v in repdata.items():
        s = s.replace(f"[{key}]", str(v))
    return s
