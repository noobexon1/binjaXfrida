from binaryninja import log_info

from binjaXfrida.generators.generators_utils import read_template, fill_template

TEMPLATE_FILENAME = "negate_cond_branch_x86.js"

def generate_negate_x86_cond_branch_snippet(module_name: str, relative_address: int) -> str:
    log_info(f"[binjaXfrida] Generating negate cond branch snippet (for module: {module_name}, relative address: {relative_address})")

    template_str = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
    }
    return fill_template(template_str, data_to_replace)