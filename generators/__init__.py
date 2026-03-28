"""Public API for all Frida snippet generators."""

from binjaXfrida.generators.generator_framework import SnippetGenerator
from binjaXfrida.generators.hook_dlopen_functions_gen import DlopenHookGenerator
from binjaXfrida.generators.hook_function_gen import FunctionHookGenerator
from binjaXfrida.generators.modify_section_protection_gen import (
    ModifySectionProtectionGenerator,
)
from binjaXfrida.generators.negate_cond_branch_arm64_gen import (
    NegateArm64CondBranchGenerator,
)
from binjaXfrida.generators.negate_cond_branch_x86_gen import (
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
