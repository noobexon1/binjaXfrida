from binaryninja import BinaryView, log_info, PluginCommand

PLUGIN_MENU = "binjaXfrida"  # everything goes under this submenu

class CommandExample:
    def __init__(self, bv: BinaryView):
        log_info("[binjaXfrida] CommandExample registered!")
        self.bv = bv

    def print_functions(self):
        for f in self.bv.functions:
            log_info(f"[binjaXfrida] {f.name} -> {f.start}")

class CommandExample2:
    def __init__(self, bv: BinaryView):
        log_info("[binjaXfrida] CommandExample2 registere!")
        self.bv = bv

    def print_functions(self):
        for f in self.bv.functions:
            log_info(f"[binjaXfrida] {f.name} -> {f.start}")

def register_plugin_commands():
    def example_command(bv: BinaryView):
        command = CommandExample(bv)
        command.print_functions()

    PluginCommand.register(
        f"{PLUGIN_MENU}\\example_command",
        "Binja and Frida. Better together!",
        example_command
    )

    def example_command2(bv: BinaryView):
        command = CommandExample2(bv)
        command.print_functions()

    PluginCommand.register(
        f"{PLUGIN_MENU}\\example_command2",
        "Binja and Frida. Better together!",
        example_command2
    )

    log_info("[binjaXfrida] binjaXfrida plugin started!")

