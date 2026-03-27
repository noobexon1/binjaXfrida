"""Generator for Frida section protection modification snippets."""

from binaryninja import log_info

from binjaXfrida.generators.generators_utils import fill_template, read_template

TEMPLATE_FILENAME = "modify_section_protection.js"


def generate_modify_section_protection_snippet(
    module_name: str,
    section_name: str,
) -> str:
    """Generate a Frida script that sets a section's protection to rwx.

    :param module_name: The target module's file name.
    :param section_name: The name of the section to modify
        (e.g. ``.text``).
    :return: The filled Frida JavaScript snippet.
    """
    log_info(
        f"[binjaXfrida] Generating modify section protection "
        f"snippet (module: {module_name}, section: {section_name})"
    )

    template = read_template(TEMPLATE_FILENAME)

    data_to_replace = {
        "MODULE_NAME_PLACEHOLDER": module_name,
        "SECTION_NAME_PLACEHOLDER": section_name,
    }

    return fill_template(template, data_to_replace)
