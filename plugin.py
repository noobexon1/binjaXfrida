"""Plugin initialization and action registration for binjaXfrida."""

from binjaXfrida.actions.action_framework import ActionManager
from binjaXfrida.log import log_info
from binjaXfrida.actions.hook_dlopen_functions_action import GenerateDlopenHooks
from binjaXfrida.actions.hook_function_action import GenerateFunctionHook
from binjaXfrida.actions.modify_section_protection_action import (
    ModifySectionProtection,
)
from binjaXfrida.actions.negate_cond_branch_arm64_action import NegateArm64CondBranch
from binjaXfrida.actions.negate_cond_branch_x86_action import NegateX86CondBranch


def init_plugin() -> None:
    """Register all binjaXfrida actions with Binary Ninja."""
    manager = ActionManager()

    manager.register(GenerateFunctionHook())
    manager.register(GenerateDlopenHooks())
    manager.register(NegateArm64CondBranch())
    manager.register(NegateX86CondBranch())
    manager.register(ModifySectionProtection())

    log_info("Plugin started!")
