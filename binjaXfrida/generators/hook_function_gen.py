from binaryninja import log_info

from binjaXfrida.generators.generators_utils import read_template, fill_template

TEMPLATE_FILENAME = "hook_function.js"

def generate_function_hook_snippet(module_name: str, function_relative_address: int, function_name: str) -> str:
    log_info(f"[binjaXfrida] Generating hook snippet for function at: {function_relative_address} (Name: {function_name})")

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "FUNCTION_RELATIVE_ADDRESS_PLACEHOLDER": function_relative_address,
        "FUNCTION_NAME_PLACEHOLDER": function_name,
    }

    return fill_template(template, data_to_replace)