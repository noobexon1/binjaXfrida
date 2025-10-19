from generators.generators_utils import load_template, fill_template

TEMPLATE_FILENAME = "hook_dlopen_functions.js"

def generate_dlopen_hook_script(module_name: str) -> str:
    print(f"[binjaXfrida] Generating dlopen hook script (for module: {module_name})")

    template = load_template(TEMPLATE_FILENAME)
    if template.startswith("// Error:"):
        return template # Propagate error

    repdata = {
        "MODULE_NAME_PLACEHOLDER": module_name,
    }
    
    return fill_template(template, repdata) 