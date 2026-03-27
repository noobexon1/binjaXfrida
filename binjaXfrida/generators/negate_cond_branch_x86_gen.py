"""Generator for Frida x86 conditional branch negation snippets."""

from binaryninja import log_info

from binjaXfrida.generators.generators_utils import fill_template, read_template

TEMPLATE_FILENAME = "negate_cond_branch_x86.js"


def generate_negate_x86_cond_branch_snippet(
    module_name: str,
    relative_address: str,
) -> str:
    """Generate a Frida script that negates an x86 conditional branch.

    :param module_name: The target module's file name.
    :param relative_address: The instruction's offset from the module
        base, as a hex string (e.g. ``0x1234``).
    :return: The filled Frida JavaScript snippet.
    """
    log_info(f"[binjaXfrida] Generating negate cond branch snippet (for module: {module_name}, relative address: {relative_address})")

    template_str = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
    }

    return fill_template(template_str, data_to_replace)
