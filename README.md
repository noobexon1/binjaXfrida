# binjaXfrida

> *Binja and Frida. Better together!*

A [Binary Ninja](https://binary.ninja/) plugin that generates
ready-to-use [Frida](https://frida.re/) JavaScript snippets directly
from your static analysis session. Right-click a function, an
instruction, or a section -- get a Frida script on your clipboard,
ready to paste and run.

Inspired by [idaXfrida](https://github.com/noobexon1/idaXfrida).

## Highlights

- Hook any function with a single click -- `Interceptor.attach`
  by module name and RVA
- Monitor `dlopen` / `android_dlopen_ext` to catch library loads
  at runtime
- Negate conditional branches in memory (**ARM64** and **x86/x64**)
- Change section protection to `rwx` for unpacking or
  self-modifying code
- Generated scripts are copied to the clipboard automatically
- Works on **Windows**, **macOS**, and **Linux**

## Installation

### Plugin Manager

Search for **binjaXfrida** in Binary Ninja's Plugin Manager and
click install.

### Manual

```bash
cd /path/to/binaryninja/plugins
git clone https://github.com/noobexon1/binjaXfrida.git
```

Restart Binary Ninja. That's it.

<details>
<summary>Where is my plugins directory?</summary>

- **Windows:** `%APPDATA%\Binary Ninja\plugins\`
- **macOS:** `~/Library/Application Support/Binary Ninja/plugins/`
- **Linux:** `~/.binaryninja/plugins/`

</details>

### Requirements

- [Binary Ninja](https://binary.ninja/) (any recent version)
- Python >= 3.13 (bundled with Binary Ninja)
- [Frida](https://frida.re/) on the target device (for running
  the generated scripts)

## Usage

1. Open a binary in Binary Ninja.
2. Right-click a function, address, or navigate to a section.
3. Pick an action from the **binjaXfrida** submenu.
4. Paste the clipboard into your Frida session.

| Action | Category | Scope | What it generates |
|--------|----------|-------|-------------------|
| **Generate function hook** | Hooks | Function | `Interceptor.attach` on a function by RVA |
| **Generate dlopen hooks** | Hooks | Binary | Hooks for `dlopen` / `android_dlopen_ext` |
| **Negate cond branch (ARM64)** | Patching | Address | XOR condition bit to flip a branch |
| **Negate cond branch (x86)** | Patching | Address | Patch short/near conditional jumps |
| **Modify section permissions** | Memory | Address | Set a section to `rwx` at runtime |

### Programmatic usage

The generators can also be called directly from Binary Ninja's
Python console:

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

```
┌──────────┐      ┌───────────┐      ┌──────────┐
│  Action   │ ---> │ Generator │ ---> │ Template │
│ (BN UI)   │      │ (Python)  │      │  (.js)   │
└──────────┘      └───────────┘      └──────────┘
  extracts          fills              Frida IIFE
  context from      placeholders       with [TOKEN]
  BinaryView        & returns string   placeholders
```

- **Templates** (`templates/*.js`) -- self-contained Frida scripts
  with `[PLACEHOLDER]` tokens.
- **Generators** (`generators/*_gen.py`) -- load a template, fill
  in placeholders, return the script string.
- **Actions** (`actions/*_action.py`) -- extract context from the
  `BinaryView`, call the generator, copy the result to clipboard.

The `ActionManager` routes each action to the right
`PluginCommand.register*` variant based on its base class:
`Action` (binary-wide), `AddressAction` (selected address), or
`FunctionAction` (selected function).

## Contributing

Contributions, bug reports, and feature requests are welcome!
Feel free to open an
[issue](https://github.com/noobexon1/binjaXfrida/issues) or
submit a pull request.

### Adding a new snippet type

1. Create a `.js` template in `templates/` using
   `[PLACEHOLDER_NAME]` syntax.
2. Create a `*_gen.py` generator in `generators/` that reads and
   fills the template.
3. Export the generator function in `generators/__init__.py`.
4. Create a `*_action.py` in `actions/` that subclasses `Action`,
   `AddressAction`, or `FunctionAction` and implements `execute()`.
5. Register the action in `plugin.py` via the `ActionManager`.

### Development setup

The included `install.ps1` (Windows/PowerShell) copies the plugin
into the Binary Ninja plugins directory and restarts BN:

```powershell
.\install.ps1            # install and restart
.\install.ps1 -NoRestart # install only
```

Run `npm install` for `@types/frida-gum` IntelliSense when editing
the JS templates.

## License

[MIT](LICENSE)

## Author

Created by [**noobexon1**](https://github.com/noobexon1).
