"""Generator for Frida dlopen hook snippets."""

from binjaXfrida.generators.generator_framework import SnippetGenerator


class DlopenHookGenerator(SnippetGenerator):
    """Generate a Frida script that hooks dlopen-family functions."""

    template_filename = "hook_dlopen_functions.js"

    def generate(self, module_name: str) -> str:
        """Generate a Frida script that hooks dlopen-family functions.

        :param module_name: The target module's file name to watch for
            during dynamic loading.
        :return: The filled Frida JavaScript snippet.
        """
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
        })
