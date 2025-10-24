from PySide6.QtWidgets import QApplication

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