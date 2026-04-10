"""Action to generate a Frida dlopen hook snippet."""

from binaryninja import BinaryView

from binjaXfrida.actions import Action
from binjaXfrida.actions.utils import get_module_name
from binjaXfrida.core.hook_dlopen_functions import DlopenHookGenerator
from binjaXfrida.log import log_warn
from binjaXfrida.ui.clipboard import copy_to_clipboard


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

        snippet = DlopenHookGenerator().generate(module_name)
        copy_to_clipboard(snippet)
