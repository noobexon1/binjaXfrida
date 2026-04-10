"""Generator for Frida section protection modification snippets."""

from binjaXfrida.core import SnippetGenerator


class ModifySectionProtectionGenerator(SnippetGenerator):
    """Generate a Frida script that sets a section's protection to rwx."""

    template_filename = "modify_section_protection.js"

    def generate(self, module_name: str, section_name: str) -> str:
        """Generate a Frida script that sets a section's protection to rwx.

        :param module_name: The target module's file name.
        :param section_name: The name of the section to modify
            (e.g. ``.text``).
        :return: The filled Frida JavaScript snippet.
        """
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
            "SECTION_NAME_PLACEHOLDER": section_name,
        })
