"""Generator for Frida function hook snippets."""

from binjaXfrida.generators.generator_framework import SnippetGenerator


class FunctionHookGenerator(SnippetGenerator):
    """Generate a Frida ``Interceptor.attach`` script for a function."""

    template_filename = "hook_function.js"

    def generate(
        self,
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
        return self._render({
            "MODULE_NAME_PLACEHOLDER": module_name,
            "FUNCTION_RELATIVE_ADDRESS_PLACEHOLDER": function_relative_address,
            "FUNCTION_NAME_PLACEHOLDER": function_name,
        })
