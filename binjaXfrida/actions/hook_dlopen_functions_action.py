from binaryninja import BinaryView, log_warn

from binjaXfrida.actions.action_framework import Action
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.hook_dlopen_functions_gen import generate_dlopen_hook_snippet


class GenerateDlopenHooks(Action):
    description = "Generate dlopen hooks (Basic for Android native libs)"
    category_name = "Hooks"

    def execute(self, bv: BinaryView) -> None:
        module_name = get_module_name(bv)

        if not module_name:
            log_warn("[binjaXfrida] Error: Could not get module name.")
            return

        snippet = generate_dlopen_hook_snippet(module_name)

        if snippet and not snippet.startswith("// Error:"):
            copy_to_clipboard(snippet)
        else:
            log_warn(f"[binjaXfrida] Error: Could not generate dlopen hook script: {snippet}")
