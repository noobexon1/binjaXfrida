"""Binary Ninja plugin entry point for binjaXfrida."""

from binjaXfrida.actions import ActionManager
from binjaXfrida.actions.hook_dlopen_functions import GenerateDlopenHooks
from binjaXfrida.actions.hook_function import GenerateFunctionHook
from binjaXfrida.actions.modify_section_protection import ModifySectionProtection
from binjaXfrida.actions.negate_cond_branch_arm64 import NegateArm64CondBranch
from binjaXfrida.actions.negate_cond_branch_x86 import NegateX86CondBranch
from binjaXfrida.log import log_info

manager = ActionManager()

manager.register(GenerateFunctionHook())
manager.register(GenerateDlopenHooks())
manager.register(NegateArm64CondBranch())
manager.register(NegateX86CondBranch())
manager.register(ModifySectionProtection())

log_info("Plugin started!")
