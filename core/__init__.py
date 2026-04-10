"""Base class for Frida snippet generators.

Every generator **must** subclass :class:`SnippetGenerator` and:

1. Set the ``template_filename`` class attribute to the name of a
   JavaScript template file located in the ``templates/`` directory.
2. Implement a ``generate()`` method with explicit, typed parameters
   that builds a placeholder mapping and delegates to :meth:`_render`.

Example::

    class MyNewGenerator(SnippetGenerator):
        template_filename = "my_template.js"

        def generate(self, module_name: str, offset: str) -> str:
            return self._render({
                "MODULE_NAME_PLACEHOLDER": module_name,
                "OFFSET_PLACEHOLDER": offset,
            })

Both constraints are validated at class-creation time; forgetting
either one raises :class:`TypeError` immediately.
"""

from collections.abc import Mapping

from binjaXfrida.core.utils import fill_template, read_template
from binjaXfrida.log import log_info


class SnippetGenerator:
    """Abstract base for all Frida snippet generators.

    Subclasses must define ``template_filename`` and override
    ``generate()``.  The shared rendering pipeline lives in
    :meth:`_render`.
    """

    template_filename: str

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

        if not getattr(cls, "template_filename", None):
            raise TypeError(
                f"{cls.__name__} must define 'template_filename' "
                f"as a non-empty class attribute."
            )

        if "generate" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must implement a 'generate()' method."
            )

    def _render(self, placeholders: Mapping[str, str | int]) -> str:
        """Read the template, substitute placeholders, and return the result.

        :param placeholders: Mapping of placeholder names (without
            brackets) to replacement values.
        :return: The filled Frida JavaScript snippet.
        """
        log_info(
            f"{type(self).__name__}: {placeholders}"
        )
        template = read_template(self.template_filename)
        return fill_template(template, placeholders)


from binjaXfrida.core.hook_dlopen_functions import DlopenHookGenerator
from binjaXfrida.core.hook_function import FunctionHookGenerator
from binjaXfrida.core.modify_section_protection import (
    ModifySectionProtectionGenerator,
)
from binjaXfrida.core.negate_cond_branch_arm64 import (
    NegateArm64CondBranchGenerator,
)
from binjaXfrida.core.negate_cond_branch_x86 import (
    NegateX86CondBranchGenerator,
)

__all__ = [
    "SnippetGenerator",
    "DlopenHookGenerator",
    "FunctionHookGenerator",
    "ModifySectionProtectionGenerator",
    "NegateArm64CondBranchGenerator",
    "NegateX86CondBranchGenerator",
]
