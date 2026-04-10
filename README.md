<!-- PROJECT LOGO -->
<br />

<img src="assets/logo.jpg" alt="binjaXfrida logo" width="400" />

# binjaXfrida: Binary Ninja <-> Frida

`binjaXfrida` is a Binary Ninja plugin designed to bridge the gap between static analysis in Binary Ninja and dynamic analysis with Frida. It allows users to quickly generate Frida JavaScript snippets based on the current context in Binary Ninja (e.g., selected function, instruction, or module details) to aid in reverse engineering and dynamic instrumentation tasks.

## Examples:

### Generate a function hook:

<div align="center">
    <img src="assets/image1.png" alt="plugin_showcase" width="1024"/>
</div>

<div align="center">
    <img src="assets/image2.png" alt="generated" width="1024" />
</div>

### Generate a scripts to negate conditional branch on AArch64:

<div align="center">
    <img src="assets/image3.png" alt="plugin_showcase" width="1024"/>
</div>

<div align="center">
    <img src="assets/image4.png" alt="generated" width="1024" />
</div>


## Features

*   **Rapid Frida Script Generation:** Right-click in Binja's Disassembly, Pseudocode, or Functions views to access script generation options.
*   **Scripts are independent and composable:** Scripts are independent of one another, but can be nested. This design helps creating complex scripts from basic blocks. For example, you can combine snippets to hook a function, negate a conditional instruction upon enter, and then restore the code back to its original state upon leaveing the function. All that with a few clicks on the mouse in Binja.
*   **Context-Aware Snippets:** Scripts are tailored based on the current address, function, module name, and other relevant Binja information.
*   **Organized UI:** Actions are neatly categorized in the Binja context menu for ease of use.
*   **Currently Supported Actions:**
    *   **Hooks Category:**
        *   `Generate function hook`: Creates a Frida script to intercept calls to the selected function, logging entry and exit.
        *   `Generate dlopen hooks`: Generates a script to monitor `dlopen` (and related Android functions) to detect when a specific module is loaded.
    *   **Memory Category:**
        *   `Generate modify section protection script`: Creates a script to change the memory protection of the section containing the currently selected address (e.g., to make it writable).
    *   **Patching Category:**
        *   `Negate cond branch instruction (ARM64)`: Generates a script to flip the condition of an ARM64 conditional branch instruction.
        *   `Negate cond branch instruction (x86/x64)`: Generates a script to flip the condition of an x86/x64 conditional branch instruction.
*   **Clipboard Integration:** Generated scripts are automatically copied to the clipboard.
*   **Extensible Framework:** Designed with a clear separation of concerns (actions, generators, templates) making it easy to add new Frida script generation capabilities.

## How it Works

The plugin operates on a simple three-part system for each feature:

1.  **Frida Templates (`templates/`):** These are pre-defined Frida JavaScript files with placeholders (e.g., for module name, function address).
2.  **Binja Actions (`actions/`):** Python classes that interface with the Binary Ninja API. They gather the necessary data from the current Binja context (e.g., function name, address under cursor), perform error handling, and then invoke a generator.
3.  **Script Generators (`generators/`):** Python modules that take the data from an Action and populate the corresponding Frida Template, producing the final script.

This modular design allows for easy addition of new features by creating a new template, an action to gather data, and a generator to combine them.

## Installation

1.  **Prerequisites:**
    *   Binary Ninja with plugins support.
    *   Frida installed and set up on your target system/device.
2.  **Locate your Binary Ninja plugins directory.**
    *   You can find this in Binary Ninja via the Plugin Manager, or by checking the `User Folder` path under `Settings` -> `Paths`.
    *   Common paths:
        *   Windows: `%APPDATA%\Binary Ninja\plugins`
        *   Linux: `~/.binaryninja/plugins`
        *   macOS: `~/Library/Application Support/Binary Ninja/plugins`
3.  **Copy the Plugin:**
    *   Copy the entire `binjaXfrida` directory (the one containing `binjaXfrida.py`, the `actions/` folder, etc.) into your Binary Ninja Pro plugins directory. Alternatively, download and unzip the latest release from https://github.com/noobexon1/binjaXfrida/releases into you plugins directory.
4.  **Restart Binary Ninja.** The plugin should be loaded automatically. You will see messages from `[binjaXfrida]` in the Binary Ninja Output window if it loads correctly.

## Usage

1.  Open your target binary in Binary Ninja.
2.  Navigate to a function, instruction, or area of interest in the Disassembly, Pseudocode, or Functions view.
3.  **Right-click** to open the context menu.
4.  Hover over the **`binjaXfrida`** menu item.
5.  Select the desired category (e.g., `Hooks`, `Memory`, `Patching`).
6.  Click on the specific script generation action you want to perform.
7.  The generated Frida script will be printed to the Binja Output window and automatically **copied to your clipboard**.
8.  Paste the script into your Frida CCLI, your own Frida agent, or save it to a `.js` file for later use with Frida.
9.  Optional: Try to nest scripts within scripts! It works and its powerfull!

## Contributing

`binjaXfrida` is all about sharing. You got some nice scripts? make a snippet template for them so everyone can enjoy! :)
Contributions are welcome! If you have ideas for new Frida snippets, improvements to existing ones, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch for your feature or fix.
3.  Make your changes.
4.  Submit a pull request.

Please try to follow the existing code structure (templates, actions, generators) when adding new features.
In the future, I will create a wiki with information on how to setup a comfortable development environement, but for now just go with the flow.

## Future Enhancements (Ideas)

*   More sophisticated script generation (e.g., memory dumping).
*   User-configurable templates or settings.
*   Support for more architectures or Frida APIs.
*   Create a wiki to help contributers setup a comfortable dev environment to create new snippets.
*   Create a clear contribution guidelines (For now, I will code review to make sure structure is ok).

## License

MIT.