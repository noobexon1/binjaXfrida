from binaryninja import log_info

from binjaXfrida.generators.generators_utils import read_template, fill_template

TEMPLATE_FILENAME = "modify_section_protection.js"

def generate_modify_section_protection_snippet(module_name: str, section_name: str) -> str:
    log_info(f"[binjaXfrida] Generating modify section protection snippet (for module: {module_name}, section: {section_name})")
    
    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "SECTION_NAME_PLACEHOLDER": section_name,
    }

    return fill_template(template, data_to_replace)