from typing import Optional

from binaryninja import BinaryView, Function, PluginCommand, log_info, log_warn


PLUGIN_MENU = "binjaXfrida"


class Action:
    """Base action that operates on a BinaryView."""

    description: str = ""
    category_name: Optional[str] = None

    @property
    def name(self) -> str:
        return f"binjaXfrida:{type(self).__name__}"

    @property
    def menu_path(self) -> str:
        """Full backslash-separated menu path used by PluginCommand."""
        if self.category_name:
            return f"{PLUGIN_MENU}\\{self.category_name}\\{self.description}"
        return f"{PLUGIN_MENU}\\{self.description}"

    def execute(self, bv: BinaryView) -> None:
        raise NotImplementedError


class AddressAction(Action):
    """Action that operates on a BinaryView and a specific address."""

    def execute(self, bv: BinaryView, addr: int) -> None:  # type: ignore[override]
        raise NotImplementedError


class FunctionAction(Action):
    """Action that operates on a BinaryView and a specific function."""

    def execute(self, bv: BinaryView, func: Function) -> None:  # type: ignore[override]
        raise NotImplementedError


class ActionManager:
    """Registers Action instances as Binary Ninja PluginCommands."""

    def __init__(self) -> None:
        self._actions: list[Action] = []

    def register(self, action: Action) -> None:
        if any(a.name == action.name for a in self._actions):
            log_warn(f"[binjaXfrida] Warning: Action '{action.name}' already registered. Skipping.")
            return

        self._actions.append(action)

        if isinstance(action, FunctionAction):
            PluginCommand.register_for_function(
                action.menu_path,
                action.description,
                lambda bv, func, a=action: a.execute(bv, func),
            )
        elif isinstance(action, AddressAction):
            PluginCommand.register_for_address(
                action.menu_path,
                action.description,
                lambda bv, addr, a=action: a.execute(bv, addr),
            )
        else:
            PluginCommand.register(
                action.menu_path,
                action.description,
                lambda bv, a=action: a.execute(bv),
            )

        log_info(f"[binjaXfrida] Action '{action.name}' registered.")

    def finalize(self) -> None:
        """Clear internal tracking. BN commands persist for the session."""
        log_info("[binjaXfrida] Finalizing actions...")
        self._actions.clear()
