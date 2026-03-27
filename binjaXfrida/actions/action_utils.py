import os

from PySide6.QtWidgets import QApplication
from binaryninja import BinaryView, log_info


def get_module_name(bv: BinaryView) -> str:
    result = os.path.basename(bv.file.original_filename)
    log_info(f"[binjaXfrida] get_module_name: {result}")
    return result


def get_binja_image_base(bv: BinaryView) -> int:
    result = bv.start
    log_info(f"[binjaXfrida] get_binja_image_base: {hex(result)}")
    return result

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
