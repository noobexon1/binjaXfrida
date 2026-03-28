"""Action to generate a Frida function hook snippet."""

from binaryninja import BinaryView, Function

from binjaXfrida.actions.action_framework import FunctionAction
from binjaXfrida.log import log_warn
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.hook_function_gen import generate_function_hook_snippet


class GenerateFunctionHook(FunctionAction):
    """Generate a Frida Interceptor.attach script for the selected function."""

    description = "Generate function hook"
    category_name = "Hooks"

    def execute(self, bv: BinaryView, func: Function) -> None:
        """Generate a hook snippet and copy it to the clipboard.

        :param bv: The current Binary Ninja BinaryView.
        :param func: The function to hook.
        """
        module_name = get_module_name(bv)
        function_relative_address = hex(func.start - bv.start)
        function_name = func.name or f"sub_{function_relative_address.lstrip('0x')}"

        snippet = generate_function_hook_snippet(
            module_name, function_relative_address, function_name
        )

        if snippet and not snippet.startswith("// Error:"):
            copy_to_clipboard(snippet)
        else:
            log_warn("Error: Failed to generate hook script.")
