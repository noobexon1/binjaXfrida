from binaryninja import BinaryView, log_info, PluginCommand


def print_functions(bv: BinaryView):
    for f in bv.functions:
        log_info(f"[binjaXfrida] {f.name} -> {f.start}")


def start(bv: BinaryView):
    log_info("[binjaXfrida] binjaXfrida plugin started!")
    print_functions(bv)


PluginCommand.register("binjaXfrida", "Binja and Frida. Better together!", start)
