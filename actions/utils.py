"""Utility helpers for extracting BinaryView info."""

import os

from binaryninja import BinaryView, Function

from binjaXfrida.log import log_info


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
