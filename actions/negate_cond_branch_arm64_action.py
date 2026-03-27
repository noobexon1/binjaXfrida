"""Action to generate a Frida ARM64 conditional branch negation snippet."""

from binaryninja import BinaryView, log_warn

from binjaXfrida.actions.action_framework import AddressAction
from binjaXfrida.actions.action_utils import copy_to_clipboard, get_module_name
from binjaXfrida.generators.negate_cond_branch_arm64_gen import (
    generate_negate_arm64_cond_branch_snippet,
)


class NegateArm64CondBranch(AddressAction):
    """Generate a Frida script that negates an ARM64 conditional branch."""

    description = "Negate cond branch instruction (ARM64)"
    category_name = "Patching"

    ARM64_COND_BRANCHES = {
        "b.eq", "b.ne", "b.hs", "b.lo", "b.cs",
        "b.mi", "b.pl", "b.vs", "b.vc",
        "b.hi", "b.ls", "b.ge", "b.lt",
        "b.gt", "b.le",
    }

    @staticmethod
    def _is_arm64_cond_branch(bv: BinaryView, addr: int) -> bool:
        """Check whether the instruction at *addr* is an ARM64 conditional branch.

        :param bv: The current Binary Ninja BinaryView.
        :param addr: The address to inspect.
        :return: ``True`` if the mnemonic is a recognized ARM64
            conditional branch.
        """
        try:
            disasm = bv.get_disassembly(addr)
            if not disasm:
                return False
            mnemonic = disasm.split()[0].lower()
            return mnemonic in NegateArm64CondBranch.ARM64_COND_BRANCHES
        except Exception:
            return False

    def execute(self, bv: BinaryView, addr: int) -> None:
        """Generate a branch negation snippet and copy it to the clipboard.

        :param bv: The current Binary Ninja BinaryView.
        :param addr: The address of the conditional branch instruction.
        """
        module_name = get_module_name(bv)

        if not self._is_arm64_cond_branch(bv, addr):
            disasm = bv.get_disassembly(addr) or "<unknown>"
            log_warn(
                f"[binjaXfrida] Error: Instruction at {hex(addr)} ('{disasm}') "
                f"is not a recognized ARM64 conditional branch."
            )
            return

        relative_address = hex(addr - bv.start)
        snippet = generate_negate_arm64_cond_branch_snippet(
            module_name, relative_address
        )

        if snippet and not snippet.startswith("// Error:"):
            copy_to_clipboard(snippet)
        else:
            log_warn("[binjaXfrida] Error: Failed to generate script.")
