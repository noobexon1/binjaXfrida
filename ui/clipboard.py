"""Clipboard access via Qt."""

from PySide6.QtWidgets import QApplication

from binjaXfrida.log import log_info, log_warn


def copy_to_clipboard(data: str) -> bool:
    """Copy the given string to the system clipboard via Qt.

    :param data: The text to copy.
    :return: ``True`` if the data was copied successfully,
        ``False`` otherwise.
    """
    if not data:
        log_warn("Error: No valid script data generated to copy.")
        return False

    clipboard_copied = False
    try:
        app = QApplication.instance()
        if not app:
            log_warn(
                "Warning: QApplication.instance()"
                " is None. Attempting to create one."
            )
            app = QApplication([])

        if not isinstance(app, QApplication):
            log_warn("Warning: App instance is not a QApplication.")
            return False

        clipboard = app.clipboard()
        if clipboard:
            clipboard.setText(data)
            log_info("Generated Frida script copied to clipboard!")
            clipboard_copied = True
        else:
            log_warn("Warning: Could not get clipboard instance.")
    except Exception as e:
        log_warn(f"Error copying script to clipboard: {e}")

    return clipboard_copied
