# binjaXfrida

> Binja and Frida. Better together!

A [Binary Ninja](https://binary.ninja/) plugin that bridges the gap between **static analysis** in Binary Ninja and **dynamic instrumentation** with [Frida](https://frida.re/). Generate ready-to-use Frida JavaScript snippets directly from your Binary Ninja session and copy them to the clipboard with a single click.

Inspired by [idaXfrida](https://github.com/noobexon1/idaXfrida).

---

## Features

- **Hook any function** -- Generate a Frida `Interceptor.attach` script for a function identified in Binary Ninja, targeting it by module name and relative virtual address (RVA).
- **Hook `dlopen` family** -- Monitor dynamic library loading (`dlopen`, `dlopen_ext`, `android_dlopen_ext`) and detect when a specific module is loaded at runtime.
- **Negate conditional branches** -- Patch conditional branch instructions in memory via Frida's `Memory.patchCode`, with architecture-specific support for **ARM64** and **x86/x64**.
- **Modify section protection** -- Change memory protection of a named section to `rwx` at runtime, useful for self-modifying code or unpacking scenarios.
- **Clipboard integration** -- Generated scripts are automatically copied to the system clipboard, ready to paste into your Frida workflow.
- **Cross-platform** -- Works on **Windows**, **macOS**, and **Linux**.

## Project Structure

```
binjaXfrida/
├── __init__.py                        # Plugin entry point
├── plugin.json                        # Binary Ninja plugin metadata
├── pyproject.toml                     # Python project metadata
├── package.json                       # Dev dependency (@types/frida-gum)
└── binjaXfrida/
    ├── binjaXfrida.py                 # PluginCommand registration
    ├── actions/
    │   └── action_utils.py            # BinaryView helpers & clipboard
    ├── generators/
    │   ├── __init__.py                # Re-exports all generators
    │   ├── generators_utils.py        # Template loading & placeholder filling
    │   ├── hook_dlopen_functions_gen.py
    │   ├── hook_function_gen.py
    │   ├── modify_section_protection_gen.py
    │   ├── negate_cond_branch_arm64_gen.py
    │   └── negate_cond_branch_x86_gen.py
    └── templates/
        ├── hook_dlopen_functions.js
        ├── hook_function.js
        ├── modify_section_protection.js
        ├── negate_cond_branch_arm64.js
        └── negate_cond_branch_x86.js
```

## Installation

### From the Binary Ninja Plugin Manager

Search for **binjaXfrida** in the Plugin Manager and install it directly.

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
3. Use the **binjaXfrida** submenu from the command palette or plugin menu to generate a Frida snippet.
4. The generated JavaScript is copied to your clipboard automatically.
5. Paste the snippet into your Frida session (`frida` CLI, a Python script, or any Frida-based tool).

### Available Generators

| Generator | Description | Parameters |
|-----------|-------------|------------|
| **Hook Function** | `Interceptor.attach` on a function by RVA | Module name, RVA, function name |
| **Hook dlopen** | Monitor `dlopen` / `android_dlopen_ext` calls | Module name |
| **Negate Branch (ARM64)** | XOR condition bit to flip a branch | Module name, RVA |
| **Negate Branch (x86)** | Patch short/near conditional jumps | Module name, RVA |
| **Modify Section Protection** | Set a section to `rwx` at runtime | Module name, section name |

### Programmatic Usage

You can also use the generators directly from Binary Ninja's Python console or your own scripts:

```python
from binjaXfrida.generators import generate_function_hook_snippet

script = generate_function_hook_snippet(
    module_name="libtarget.so",
    function_relative_address="0x1234",
    function_name="secret_check"
)
print(script)
```

## How It Works

binjaXfrida follows a **template + generator** architecture:

1. **Templates** (`templates/*.js`) are self-contained Frida scripts wrapped in IIFEs with `[PLACEHOLDER]` tokens.
2. **Generators** (`generators/*_gen.py`) accept parameters derived from Binary Ninja's `BinaryView` (module name, RVA, section name, etc.), load the corresponding template, and fill in the placeholders.
3. **Actions** (`actions/action_utils.py`) extract information from the current BinaryView and copy the generated script to the clipboard via Qt.

This separation makes it straightforward to add new snippet types -- just create a `.js` template and a corresponding generator.

## Requirements

- [Binary Ninja](https://binary.ninja/) (any recent version)
- Python >= 3.13 (provided by Binary Ninja's bundled Python)
- [Frida](https://frida.re/) installed on the target device / environment (for running the generated scripts)

### Optional (Development)

- `npm install` to get `@types/frida-gum` for IntelliSense when editing the JS templates.

## Contributing

Contributions are welcome! If you'd like to add a new generator, fix a bug, or improve the UI integration:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

When adding a new snippet type:
1. Create a `.js` template in `binjaXfrida/templates/` using `[PLACEHOLDER_NAME]` syntax.
2. Create a `*_gen.py` generator in `binjaXfrida/generators/` that reads and fills the template.
3. Export the generator function in `binjaXfrida/generators/__init__.py`.
4. Register a `PluginCommand` in `binjaXfrida/binjaXfrida.py` to wire it into the UI.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Author

**noobexon1**
