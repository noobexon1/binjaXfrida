import os

from PySide6.QtWidgets import QApplication
from binaryninja import log_error

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
