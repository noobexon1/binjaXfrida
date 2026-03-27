# binjaXfrida

> Binja and Frida. Better together!

A [Binary Ninja](https://binary.ninja/) plugin that bridges the gap
between **static analysis** in Binary Ninja and **dynamic
instrumentation** with [Frida](https://frida.re/). Generate
ready-to-use Frida JavaScript snippets directly from your Binary Ninja
session and copy them to the clipboard with a single click.

Inspired by [idaXfrida](https://github.com/noobexon1/idaXfrida).

---

## Features

- **Hook any function** -- Generate a Frida `Interceptor.attach` script
  for a function identified in Binary Ninja, targeting it by module name
  and relative virtual address (RVA).
- **Hook `dlopen` family** -- Monitor dynamic library loading (`dlopen`,
  `dlopen_ext`, `android_dlopen_ext`) and detect when a specific module
  is loaded at runtime.
- **Negate conditional branches** -- Patch conditional branch
  instructions in memory via Frida's `Memory.patchCode`, with
  architecture-specific support for **ARM64** and **x86/x64**.
- **Modify section protection** -- Change memory protection of a named
  section to `rwx` at runtime, useful for self-modifying code or
  unpacking scenarios.
- **Clipboard integration** -- Generated scripts are automatically
  copied to the system clipboard, ready to paste into your Frida
  workflow.
- **Cross-platform** -- Works on **Windows**, **macOS**, and **Linux**.

## Project Structure

```
binjaXfrida/
├── __init__.py                        # Plugin entry point
├── plugin.py                          # Plugin init & action registration
├── plugin.json                        # Binary Ninja plugin metadata
├── pyproject.toml                     # Python project metadata
├── LICENSE                            # MIT license
├── package.json                       # Dev dependency (@types/frida-gum)
├── install.ps1                        # Dev helper: install & restart BN
├── actions/
│   ├── __init__.py
│   ├── action_framework.py            # Action / ActionManager base classes
│   ├── action_utils.py                # BinaryView helpers & clipboard
│   ├── hook_function_action.py
│   ├── hook_dlopen_functions_action.py
│   ├── modify_section_protection_action.py
│   ├── negate_cond_branch_arm64_action.py
│   └── negate_cond_branch_x86_action.py
├── generators/
│   ├── __init__.py                    # Re-exports all generators
│   ├── generators_utils.py            # Template loading & placeholder filling
│   ├── hook_function_gen.py
│   ├── hook_dlopen_functions_gen.py
│   ├── modify_section_protection_gen.py
│   ├── negate_cond_branch_arm64_gen.py
│   └── negate_cond_branch_x86_gen.py
└── templates/
    ├── hook_function.js
    ├── hook_dlopen_functions.js
    ├── modify_section_protection.js
    ├── negate_cond_branch_arm64.js
    └── negate_cond_branch_x86.js
```

## Installation

### From the Binary Ninja Plugin Manager

Search for **binjaXfrida** in the Plugin Manager and install it
directly.

### Manual Installation

1. Locate your Binary Ninja plugins directory:
   - **Windows:** `%APPDATA%\Binary Ninja\plugins\`
   - **macOS:** `~/Library/Application Support/Binary Ninja/plugins/`
   - **Linux:** `~/.binaryninja/plugins/`

2. Clone this repository into the plugins directory:

   ```bash
   cd /path/to/binaryninja/plugins
   git clone https://github.com/noobexon1/binjaXfrida.git
   ```

3. Restart Binary Ninja.

## Usage

1. Open a binary in Binary Ninja.
2. Navigate to a function or address of interest.
3. Open the **binjaXfrida** submenu from the command palette or plugin
   menu. Actions are grouped into categories:
   - **Hooks** -- function hooks, dlopen hooks
   - **Patching** -- negate conditional branches (ARM64 / x86)
   - **Memory** -- modify section protection
4. The generated JavaScript is copied to your clipboard automatically.
5. Paste the snippet into your Frida session (`frida` CLI, a Python
   script, or any Frida-based tool).

### Available Actions

| Action | Category | Scope | Description |
|--------|----------|-------|-------------|
| **Generate function hook** | Hooks | Function | `Interceptor.attach` on a function by RVA |
| **Generate dlopen hooks** | Hooks | Binary | Monitor `dlopen` / `android_dlopen_ext` calls |
| **Negate cond branch (ARM64)** | Patching | Address | XOR condition bit to flip an ARM64 branch |
| **Negate cond branch (x86)** | Patching | Address | Patch short/near x86 conditional jumps |
| **Modify section permissions** | Memory | Address | Set a section to `rwx` at runtime |

### Programmatic Usage

You can also use the generators directly from Binary Ninja's Python
console or your own scripts:

```python
from binjaXfrida.generators import generate_function_hook_snippet

script = generate_function_hook_snippet(
    module_name="libtarget.so",
    function_relative_address="0x1234",
    function_name="secret_check",
)
print(script)
```

## How It Works

binjaXfrida follows a three-layer **action -> generator -> template**
architecture:

1. **Templates** (`templates/*.js`) are self-contained Frida scripts
   wrapped in IIFEs with `[PLACEHOLDER]` tokens.
2. **Generators** (`generators/*_gen.py`) load a template, fill in the
   placeholders with concrete values, and return the resulting script
   string.
3. **Actions** (`actions/*_action.py`) are Binary Ninja `PluginCommand`
   wrappers. Each action extracts the relevant context from the current
   `BinaryView` (module name, RVA, section, etc.), calls the
   appropriate generator, and copies the result to the clipboard.

The `ActionManager` in `action_framework.py` handles registration,
automatically routing each action to the correct `PluginCommand`
variant (`register`, `register_for_address`, or
`register_for_function`) based on its base class:

- **`Action`** -- operates on the whole binary (e.g. dlopen hooks).
- **`AddressAction`** -- operates on a selected address
  (e.g. branch negation, section protection).
- **`FunctionAction`** -- operates on a selected function
  (e.g. function hooks).

## Adding a New Snippet Type

1. Create a `.js` template in `templates/` using
   `[PLACEHOLDER_NAME]` syntax.
2. Create a `*_gen.py` generator in `generators/` that reads and
   fills the template.
3. Export the generator function in `generators/__init__.py`.
4. Create a `*_action.py` in `actions/` that subclasses `Action`,
   `AddressAction`, or `FunctionAction` and implements `execute()`.
5. Register the action in `plugin.py` via the `ActionManager`.

## Requirements

- [Binary Ninja](https://binary.ninja/) (any recent version)
- Python >= 3.13 (provided by Binary Ninja's bundled Python)
- [Frida](https://frida.re/) installed on the target device /
  environment (for running the generated scripts)

### Optional (Development)

- `npm install` to get `@types/frida-gum` for IntelliSense when
  editing the JS templates.

## Contributing

Contributions are welcome! If you'd like to add a new snippet type,
fix a bug, or improve the UI integration:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License

This project is licensed under the
[MIT License](https://opensource.org/licenses/MIT).

## Author

**noobexon1**
