"""Public API for all Frida snippet generators."""

from binjaXfrida.generators.hook_dlopen_functions_gen import generate_dlopen_hook_snippet
from binjaXfrida.generators.hook_function_gen import generate_function_hook_snippet
from binjaXfrida.generators.modify_section_protection_gen import generate_modify_section_protection_snippet
from binjaXfrida.generators.negate_cond_branch_arm64_gen import generate_negate_arm64_cond_branch_snippet
from binjaXfrida.generators.negate_cond_branch_x86_gen import generate_negate_x86_cond_branch_snippet

__all__ = [
    "generate_dlopen_hook_snippet",
    "generate_function_hook_snippet",
    "generate_modify_section_protection_snippet",
    "generate_negate_arm64_cond_branch_snippet",
    "generate_negate_x86_cond_branch_snippet",
]
