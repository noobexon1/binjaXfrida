"""Generator for Frida dlopen hook snippets."""

from binaryninja import log_info

from binjaXfrida.generators.generators_utils import fill_template, read_template

TEMPLATE_FILENAME = "hook_dlopen_functions.js"


def generate_dlopen_hook_snippet(module_name: str) -> str:
    """Generate a Frida script that hooks dlopen-family functions.

    :param module_name: The target module's file name to watch for
        during dynamic loading.
    :return: The filled Frida JavaScript snippet.
    """
    log_info(
        f"[binjaXfrida] Generating dlopen hook snippet "
        f"(for module: {module_name})"
    )

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
    }

    return fill_template(template, data_to_replace)
