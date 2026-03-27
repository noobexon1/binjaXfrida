from binaryninja import BinaryView, log_warn

from binjaXfrida.actions.action_framework import AddressAction
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.modify_section_protection_gen import generate_modify_section_protection_snippet


class ModifySectionProtection(AddressAction):
    description = "Modify current section permissions"
    category_name = "Memory"

    @staticmethod
    def _get_section_name_at(bv: BinaryView, addr: int) -> str | None:
        for name, section in bv.sections.items():
            if section.start <= addr < section.start + section.length:
                return name
        return None

    def execute(self, bv: BinaryView, addr: int) -> None:
        module_name = get_module_name(bv)

        section_name = self._get_section_name_at(bv, addr)
        if not section_name:
            log_warn(f"[binjaXfrida] Error: Could not determine the containing section for address {hex(addr)}.")
            return

        if not section_name.startswith("."):
            log_warn(
                f"[binjaXfrida] Error: Address is not in a standard section. "
                f"(Section name: {section_name})"
            )
            return

        snippet = generate_modify_section_protection_snippet(module_name, section_name)

        if snippet and not snippet.startswith("// Error:"):
            copy_to_clipboard(snippet)
        else:
            log_warn(f"[binjaXfrida] Error: Could not generate modify section protection script: {snippet}")
