from binaryninja import BinaryView, Function, log_warn

from binjaXfrida.actions.action_framework import FunctionAction
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.hook_function_gen import generate_function_hook_snippet


class GenerateFunctionHook(FunctionAction):
    description = "Generate function hook"
    category_name = "Hooks"

    def execute(self, bv: BinaryView, func: Function) -> None:
        module_name = get_module_name(bv)
        function_relative_address = hex(func.start - bv.start)
        function_name = func.name or f"sub_{function_relative_address.lstrip('0x')}"

        snippet = generate_function_hook_snippet(module_name, function_relative_address, function_name)

        if snippet and not snippet.startswith("// Error:"):
            copy_to_clipboard(snippet)
        else:
            log_warn("[binjaXfrida] Error: Failed to generate hook script.")
