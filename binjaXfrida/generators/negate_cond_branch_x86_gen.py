from generators.generators_utils import load_template, fill_template

TEMPLATE_FILENAME = "negate_cond_branch_x86.js"

def generate_negate_x86_cond_branch_script(module_name: str, relative_address: int) -> str:
    print(f"[binjaXfrida] Generating negate cond branch script (for module: {module_name}, relative address: {relative_address})")

    template_str = load_template(TEMPLATE_FILENAME)
    if template_str.startswith("// Error:"):
        return template_str # Propagate error

    repdata = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
    }
    return fill_template(template_str, repdata) 