"""Action to generate a Frida dlopen hook snippet."""

from binaryninja import BinaryView

from binjaXfrida.actions.action_framework import Action
from binjaXfrida.log import log_warn
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.hook_dlopen_functions_gen import (
    generate_dlopen_hook_snippet,
)


class GenerateDlopenHooks(Action):
    """Generate a Frida script that hooks dlopen-family functions."""

    description = "Generate dlopen hooks (Basic for Android native libs)"
    category_name = "Hooks"

    def execute(self, bv: BinaryView) -> None:
        """Generate a dlopen hook snippet and copy it to the clipboard.

        :param bv: The current Binary Ninja BinaryView.
        """
        module_name = get_module_name(bv)

        if not module_name:
            log_warn("Error: Could not get module name.")
            return

        snippet = generate_dlopen_hook_snippet(module_name)
        copy_to_clipboard(snippet)
