import os

from PySide6.QtWidgets import QApplication

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

def copy_to_clipboard(data: str) -> bool:
    """Copies the given data string to the system clipboard."""
    if not data or data.startswith("// Error:"):
        print("[binjaXfrida] Error: No valid script data generated to copy.")
        return False

    clipboard_copied = False
    try:
        app = QApplication.instance()
        if not app:
            print("[binjaXfrida] Warning: QApplication.instance() is None. Attempting to create one for clipboard.")
            app = QApplication([])

        clipboard = app.clipboard()
        if clipboard:
            clipboard.setText(data)
            print("[binjaXfrida] Generated Frida script copied to clipboard!")
            clipboard_copied = True
        else:
            print("[binjaXfrida] Warning: Could not get clipboard instance.")
    except Exception as e:
        print(f"[binjaXfrida] Error copying script to clipboard: {e}")

    return clipboard_copied