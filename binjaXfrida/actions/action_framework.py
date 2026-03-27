"""Action framework for registering binjaXfrida commands in Binary Ninja."""

from typing import Optional

from binaryninja import BinaryView, Function, PluginCommand, log_info, log_warn


PLUGIN_MENU = "binjaXfrida"


class Action:
    """Base action that operates on a BinaryView.

    Subclass this for commands that only need access to the
    full binary view (e.g. module-level operations).
    """

    description: str = ""
    category_name: Optional[str] = None

    @property
    def name(self) -> str:
        """Return a unique identifier for this action.

        :return: A string in the form ``binjaXfrida:<ClassName>``.
        """
        return f"binjaXfrida:{type(self).__name__}"

    @property
    def menu_path(self) -> str:
        """Return the full backslash-separated menu path for PluginCommand.

        :return: Menu path including plugin name, optional category,
            and description.
        """
        if self.category_name:
            return f"{PLUGIN_MENU}\\{self.category_name}\\{self.description}"
        return f"{PLUGIN_MENU}\\{self.description}"

    def execute(self, bv: BinaryView) -> None:
        """Execute the action.

        :param bv: The current Binary Ninja BinaryView.
        :raises NotImplementedError: Must be overridden by subclasses.
        """
        raise NotImplementedError


class AddressAction(Action):
    """Action that operates on a BinaryView and a specific address.

    Registered via ``PluginCommand.register_for_address`` so Binary
    Ninja provides the selected address automatically.
    """

    def execute(self, bv: BinaryView, addr: int) -> None:  # type: ignore[override]
        """Execute the action at a specific address.

        :param bv: The current Binary Ninja BinaryView.
        :param addr: The currently selected address.
        :raises NotImplementedError: Must be overridden by subclasses.
        """
        raise NotImplementedError


class FunctionAction(Action):
    """Action that operates on a BinaryView and a specific function.

    Registered via ``PluginCommand.register_for_function`` so Binary
    Ninja provides the selected function automatically.
    """

    def execute(self, bv: BinaryView, func: Function) -> None:  # type: ignore[override]
        """Execute the action for a specific function.

        :param bv: The current Binary Ninja BinaryView.
        :param func: The currently selected function.
        :raises NotImplementedError: Must be overridden by subclasses.
        """
        raise NotImplementedError


class ActionManager:
    """Registers Action instances as Binary Ninja PluginCommands.

    Routes each action to the appropriate ``PluginCommand.register*``
    variant based on whether it is a base Action, AddressAction,
    or FunctionAction.
    """

    def __init__(self) -> None:
        self._actions: list[Action] = []

    def register(self, action: Action) -> None:
        """Register an action as a Binary Ninja PluginCommand.

        :param action: The action instance to register.
        """
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
        """Clear internal action tracking.

        Binary Ninja commands persist for the session; this only
        resets the manager's internal list.
        """
        log_info("[binjaXfrida] Finalizing actions...")
        self._actions.clear()
