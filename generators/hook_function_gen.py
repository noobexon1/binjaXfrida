"""Generator for Frida function hook snippets."""

from binaryninja import log_info

from binjaXfrida.generators.generators_utils import fill_template, read_template

TEMPLATE_FILENAME = "hook_function.js"


def generate_function_hook_snippet(
    module_name: str,
    function_relative_address: str,
    function_name: str,
) -> str:
    """Generate a Frida Interceptor.attach script for a function.

    :param module_name: The target module's file name.
    :param function_relative_address: The function's offset from the
        module base, as a hex string (e.g. ``0x1234``).
    :param function_name: A human-readable name for the function.
    :return: The filled Frida JavaScript snippet.
    """
    log_info(
        f"[binjaXfrida] Generating hook snippet for function "
        f"at: {function_relative_address} (Name: {function_name})"
    )

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "FUNCTION_RELATIVE_ADDRESS_PLACEHOLDER": function_relative_address,
        "FUNCTION_NAME_PLACEHOLDER": function_name,
    }

    return fill_template(template, data_to_replace)
