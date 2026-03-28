"""Logging wrappers that automatically prepend the [binjaXfrida] tag."""

from binaryninja import log_info as _bn_log_info, log_warn as _bn_log_warn

_TAG = "[binjaXfrida]"


def log_info(msg: str) -> None:
    """Log an informational message with the plugin tag.

    :param msg: The message to log.
    """
    _bn_log_info(f"{_TAG} {msg}")


def log_warn(msg: str) -> None:
    """Log a warning message with the plugin tag.

    :param msg: The message to log.
    """
    _bn_log_warn(f"{_TAG} {msg}")
