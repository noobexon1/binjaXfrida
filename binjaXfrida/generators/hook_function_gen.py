from binjaXfrida.generators.generators_utils import load_template, fill_template

TEMPLATE_FILENAME = "hook_function.js"

def generate_function_hook_snippet(module_name: str, function_relative_address: int, function_name: str) -> str:
    print(f"[binjaXfrida] Generating hook snippet for function at: {function_relative_address} (Name: {function_name})")

    template = load_template(TEMPLATE_FILENAME)
    if template.startswith("// Error:"):
        return template # Propagate error

    repdata = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "FUNCTION_RELATIVE_ADDRESS_PLACEHOLDER": function_relative_address,
        "FUNCTION_NAME_PLACEHOLDER": function_name,
    }

    return fill_template(template, repdata) 