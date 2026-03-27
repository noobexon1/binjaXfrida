"""Generator for Frida ARM64 conditional branch negation snippets."""

from binaryninja import log_info

from binjaXfrida.generators.generators_utils import fill_template, read_template

TEMPLATE_FILENAME = "negate_cond_branch_arm64.js"


def generate_negate_arm64_cond_branch_snippet(
    module_name: str,
    relative_address: str,
) -> str:
    """Generate a Frida script that negates an ARM64 conditional branch.

    :param module_name: The target module's file name.
    :param relative_address: The instruction's offset from the module
        base, as a hex string (e.g. ``0x1234``).
    :return: The filled Frida JavaScript snippet.
    """
    log_info(
        f"[binjaXfrida] Generating snippet to negate ARM64 "
        f"conditional branch at: {relative_address}"
    )

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
    }

    return fill_template(template, data_to_replace)
