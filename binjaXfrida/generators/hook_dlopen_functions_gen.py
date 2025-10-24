from binaryninja import log_info

from binjaXfrida.generators.generators_utils import read_template, fill_template

TEMPLATE_FILENAME = "hook_dlopen_functions.js"

def generate_dlopen_hook_snippet(module_name: str) -> str:
    log_info(f"[binjaXfrida] Generating dlopen hook snippet (for module: {module_name})")

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
    }

    return fill_template(template, data_to_replace)
