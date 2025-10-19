from binjaXfrida.generators.generators_utils import load_template, fill_template

TEMPLATE_FILENAME = "modify_section_protection.js"

def generate_modify_section_protection_snippet(module_name: str, section_name: str) -> str:
    print(f"[binjaXfrida] Generating modify section protection snippet (for module: {module_name}, section: {section_name})")
    
    template = load_template(TEMPLATE_FILENAME)
    if template.startswith("// Error:"):
        return template # Propagate error 

    repdata = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "SECTION_NAME_PLACEHOLDER": section_name,
    }

    return fill_template(template, repdata)