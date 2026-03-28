"""Utility helpers for extracting BinaryView info and clipboard access."""

import os

from binaryninja import BinaryView, Function

from binjaXfrida.log import log_info, log_warn
from PySide6.QtWidgets import QApplication


def get_module_name(bv: BinaryView) -> str:
    """Extract the module file name from a BinaryView.

    :param bv: The current Binary Ninja BinaryView.
    :return: The base file name of the loaded binary.
    """
    result = os.path.basename(bv.file.original_filename)
    log_info(f"get_module_name: {result}")
    return result


def get_relative_address(bv: BinaryView, addr: int) -> str:
    """Compute an address's offset from the module base as a hex string.

    :param bv: The current Binary Ninja BinaryView.
    :param addr: The absolute address.
    :return: The offset as a hex string (e.g. ``0x1234``).
    """
    result = hex(addr - bv.start)
    log_info(f"get_relative_address: {result}")
    return result


def get_function_name(bv: BinaryView, func: Function) -> str:
    """Return a human-readable name for a function.

    Falls back to ``sub_<offset>`` when the function has no symbol name.

    :param bv: The current Binary Ninja BinaryView.
    :param func: The function to name.
    :return: The function's name or a generated fallback.
    """
    relative_address = get_relative_address(bv, func.start)
    result = func.name or f"sub_{relative_address.lstrip('0x')}"
    log_info(f"get_function_name: {result}")
    return result


def get_binja_image_base(bv: BinaryView) -> int:
    """Return the image base address of the loaded binary.

    :param bv: The current Binary Ninja BinaryView.
    :return: The start address of the binary.
    """
    result = bv.start
    log_info(f"get_binja_image_base: {hex(result)}")
    return result


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
