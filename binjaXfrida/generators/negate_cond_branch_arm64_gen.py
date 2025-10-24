from binaryninja import log_info

from binjaXfrida.generators.generators_utils import read_template, fill_template

TEMPLATE_FILENAME = "negate_cond_branch_arm64.js"

def generate_negate_arm64_cond_branch_snippet(module_name: str, relative_address: int) -> str:
    log_info(f"[binjaXfrida] Generating snippet to negate ARM64 conditional branch at: {relative_address}")

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
    }
    return fill_template(template, data_to_replace)