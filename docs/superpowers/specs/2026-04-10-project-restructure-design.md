# binjaXfrida Project Restructure

**Date:** 2026-04-10
**Branch:** `refactor_project_struct`
**Scope:** Structural refactor only — no behavioral changes to any code.

## Goal

Reorganize the project to follow Binary Ninja plugin conventions observed in well-maintained plugins (Tanto, Ariadne, Kaitai, Snippets). The restructure should make it easy for open-source contributors to add new actions and generators by creating a single file each, without touching existing code.

## Constraints

- No headless support required.
- One class per file — contributor-friendly, avoids merge conflicts.
- All existing behavior preserved exactly. No logic changes.

---

## Target Layout

```
binjaXfrida/
├── __init__.py                          # Entry point + action registration
├── plugin.json                          # Tracked in git
├── log.py                               # Logging wrappers (unchanged)
├── LICENSE
├── README.md
├── install.ps1                          # Updated for new layout
│
├── core/                                # Pure Frida snippet generation (no BN/Qt)
│   ├── __init__.py                      # SnippetGenerator base class + re-exports
│   ├── utils.py                         # read_template, fill_template, TEMPLATES_DIR
│   ├── hook_function.py                 # FunctionHookGenerator
│   ├── hook_dlopen_functions.py         # DlopenHookGenerator
│   ├── modify_section_protection.py     # ModifySectionProtectionGenerator
│   ├── negate_cond_branch_arm64.py      # NegateArm64CondBranchGenerator
│   └── negate_cond_branch_x86.py        # NegateX86CondBranchGenerator
│
├── actions/                             # BN command handlers
│   ├── __init__.py                      # Action/AddressAction/FunctionAction/ActionManager
│   ├── utils.py                         # BV helpers (get_module_name, etc.) — no Qt
│   ├── hook_function.py                 # GenerateFunctionHook
│   ├── hook_dlopen_functions.py         # GenerateDlopenHooks
│   ├── modify_section_protection.py     # ModifySectionProtection
│   ├── negate_cond_branch_arm64.py      # NegateArm64CondBranch
│   └── negate_cond_branch_x86.py        # NegateX86CondBranch
│
├── ui/                                  # Qt/PySide6 code (groundwork for future)
│   ├── __init__.py                      # Empty for now
│   └── clipboard.py                     # copy_to_clipboard
│
├── templates/                           # Static JS template files (unchanged)
│   ├── hook_function.js
│   ├── hook_dlopen_functions.js
│   ├── modify_section_protection.js
│   ├── negate_cond_branch_arm64.js
│   └── negate_cond_branch_x86.js
│
└── assets/                              # README images (unchanged)
```

---

## File Moves and Deletions

| Current file | Destination | Notes |
|---|---|---|
| `__init__.py` | `__init__.py` | Rewritten: absorbs `plugin.py` registration logic |
| `plugin.py` | **deleted** | Merged into `__init__.py` |
| `log.py` | `log.py` | Unchanged |
| `actions/__init__.py` | `actions/__init__.py` | Rewritten: absorbs `action_framework.py` classes |
| `actions/action_framework.py` | **deleted** | Merged into `actions/__init__.py` |
| `actions/action_utils.py` | `actions/utils.py` | Renamed; clipboard code removed |
| `actions/hook_function_action.py` | `actions/hook_function.py` | Renamed; imports updated |
| `actions/hook_dlopen_functions_action.py` | `actions/hook_dlopen_functions.py` | Renamed; imports updated |
| `actions/modify_section_protection_action.py` | `actions/modify_section_protection.py` | Renamed; imports updated |
| `actions/negate_cond_branch_arm64_action.py` | `actions/negate_cond_branch_arm64.py` | Renamed; imports updated |
| `actions/negate_cond_branch_x86_action.py` | `actions/negate_cond_branch_x86.py` | Renamed; imports updated |
| `generators/__init__.py` | `core/__init__.py` | Rewritten: absorbs `generator_framework.py` + re-exports |
| `generators/generator_framework.py` | **deleted** | Merged into `core/__init__.py` |
| `generators/generators_utils.py` | `core/utils.py` | Renamed; imports updated |
| `generators/hook_function_gen.py` | `core/hook_function.py` | Renamed; imports updated |
| `generators/hook_dlopen_functions_gen.py` | `core/hook_dlopen_functions.py` | Renamed; imports updated |
| `generators/modify_section_protection_gen.py` | `core/modify_section_protection.py` | Renamed; imports updated |
| `generators/negate_cond_branch_arm64_gen.py` | `core/negate_cond_branch_arm64.py` | Renamed; imports updated |
| `generators/negate_cond_branch_x86_gen.py` | `core/negate_cond_branch_x86.py` | Renamed; imports updated |
| *(new)* | `ui/__init__.py` | Empty groundwork |
| *(new)* | `ui/clipboard.py` | `copy_to_clipboard` extracted from `action_utils.py` |
| *(new)* | `plugin.json` | Created and tracked in git |

---

## Import Mapping

| Old import | New import |
|---|---|
| `from binjaXfrida.plugin import init_plugin` | *(removed — inline in `__init__.py`)* |
| `from binjaXfrida.actions.action_framework import Action` | `from binjaXfrida.actions import Action` |
| `from binjaXfrida.actions.action_framework import AddressAction` | `from binjaXfrida.actions import AddressAction` |
| `from binjaXfrida.actions.action_framework import FunctionAction` | `from binjaXfrida.actions import FunctionAction` |
| `from binjaXfrida.actions.action_framework import ActionManager` | `from binjaXfrida.actions import ActionManager` |
| `from binjaXfrida.actions.action_utils import copy_to_clipboard` | `from binjaXfrida.ui.clipboard import copy_to_clipboard` |
| `from binjaXfrida.actions.action_utils import get_module_name` | `from binjaXfrida.actions.utils import get_module_name` |
| `from binjaXfrida.actions.action_utils import get_relative_address` | `from binjaXfrida.actions.utils import get_relative_address` |
| `from binjaXfrida.actions.action_utils import get_function_name` | `from binjaXfrida.actions.utils import get_function_name` |
| `from binjaXfrida.actions.action_utils import get_binja_image_base` | `from binjaXfrida.actions.utils import get_binja_image_base` |
| `from binjaXfrida.generators.generator_framework import SnippetGenerator` | `from binjaXfrida.core import SnippetGenerator` |
| `from binjaXfrida.generators.generators_utils import fill_template, read_template` | `from binjaXfrida.core.utils import fill_template, read_template` |
| `from binjaXfrida.generators.hook_function_gen import FunctionHookGenerator` | `from binjaXfrida.core.hook_function import FunctionHookGenerator` |
| `from binjaXfrida.generators.hook_dlopen_functions_gen import DlopenHookGenerator` | `from binjaXfrida.core.hook_dlopen_functions import DlopenHookGenerator` |
| `from binjaXfrida.generators.modify_section_protection_gen import ModifySectionProtectionGenerator` | `from binjaXfrida.core.modify_section_protection import ModifySectionProtectionGenerator` |
| `from binjaXfrida.generators.negate_cond_branch_arm64_gen import NegateArm64CondBranchGenerator` | `from binjaXfrida.core.negate_cond_branch_arm64 import NegateArm64CondBranchGenerator` |
| `from binjaXfrida.generators.negate_cond_branch_x86_gen import NegateX86CondBranchGenerator` | `from binjaXfrida.core.negate_cond_branch_x86 import NegateX86CondBranchGenerator` |

---

## Other Updates

### plugin.json

Create a standard Binary Ninja plugin manifest with:
- `pluginmetadataversion`: 2
- `name`: "binjaXfrida"
- `type`: ["helper"]
- `api`: ["python3"]
- `description`: "Generate Frida scripts directly from Binary Ninja"
- `longdescription`: Summary from README (Frida snippet generation for hooking, patching, etc.)
- `license`: `{"name": "MIT", "text": "..."}`  (full MIT text from LICENSE)
- `platforms`: `["Darwin", "Linux", "Windows"]`
- `author`: "noobexon1"
- `version`: "1.0.0"
- `minimumbinaryninjaversion`: 3164

### .gitignore

Remove the `plugin.json` line so the file is tracked.

### install.ps1

Update the file/folder copy list to reflect the new layout:
- Copy `core/`, `actions/`, `ui/`, `templates/`, `log.py`, `__init__.py`, `plugin.json`
- Remove references to `plugin.py`, `generators/`

---

## What Does NOT Change

- All class names, method signatures, and behavior remain identical.
- `templates/` directory and its JS files are untouched.
- `assets/` directory is untouched.
- `log.py` is untouched.
- `LICENSE` is untouched.
