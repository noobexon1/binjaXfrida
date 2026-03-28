"""Action to generate a Frida section protection modification snippet."""

from binaryninja import BinaryView

from binjaXfrida.actions.action_framework import AddressAction
from binjaXfrida.log import log_warn
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.modify_section_protection_gen import (
    generate_modify_section_protection_snippet,
)


class ModifySectionProtection(AddressAction):
    """Generate a Frida script that changes a section's memory protection to rwx."""

    description = "Modify current section permissions"
    category_name = "Memory"

    @staticmethod
    def _get_section_name_at(bv: BinaryView, addr: int) -> str | None:
        """Find the section that contains *addr*.

        :param bv: The current Binary Ninja BinaryView.
        :param addr: The address to look up.
        :return: The section name, or ``None`` if no section contains
            the address.
        """
        for name, section in bv.sections.items():
            if section.start <= addr < section.start + section.length:
                return name
        return None

    def execute(self, bv: BinaryView, addr: int) -> None:
        """Generate a section protection snippet and copy it to the clipboard.

        :param bv: The current Binary Ninja BinaryView.
        :param addr: An address within the target section.
        """
        module_name = get_module_name(bv)

        section_name = self._get_section_name_at(bv, addr)
        if not section_name:
            log_warn(
                f"Error: Could not determine the "
                f"containing section for address {hex(addr)}."
            )
            return

        if not section_name.startswith("."):
            log_warn(
                f"Error: Address is not in a standard section. "
                f"(Section name: {section_name})"
            )
            return

        snippet = generate_modify_section_protection_snippet(
            module_name, section_name
        )
        copy_to_clipboard(snippet)
