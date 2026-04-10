"""Generator for Frida ARM64 conditional branch negation snippets."""

from binjaXfrida.core import SnippetGenerator


class NegateArm64CondBranchGenerator(SnippetGenerator):
    """Generate a Frida script that negates an ARM64 conditional branch."""

    template_filename = "negate_cond_branch_arm64.js"

    def generate(self, module_name: str, relative_address: str) -> str:
        """Generate a Frida script that negates an ARM64 conditional branch.

        :param module_name: The target module's file name.
        :param relative_address: The instruction's offset from the module
            base, as a hex string (e.g. ``0x1234``).
        :return: The filled Frida JavaScript snippet.
        """
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
            "RELATIVE_ADDRESS_PLACEHOLDER": relative_address,
        })
