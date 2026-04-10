#!/usr/bin/env bash
#
# Deploy binjaXfrida to the Binary Ninja plugins directory and
# restart Binary Ninja.
#
# Copies the plugin files from the development directory into
# the user plugins folder, overwriting any existing version,
# then restarts Binary Ninja so the changes take effect.
#
# The script aborts on any error; every destructive or I/O step
# is followed by a validation check.

set -euo pipefail

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- Defaults ---
BINJA_PLUGINS_DIR="${HOME}/.binaryninja/plugins"
NO_RESTART=false

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --plugins-dir)
            BINJA_PLUGINS_DIR="$2"
            shift 2
            ;;
        --no-restart)
            NO_RESTART=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--plugins-dir DIR] [--no-restart]"
            echo ""
            echo "  --plugins-dir DIR   Binary Ninja plugins directory"
            echo "                      (default: ~/.binaryninja/plugins)"
            echo "  --no-restart        Skip restarting Binary Ninja after install"
            exit 0
            ;;
        *)
            echo -e "${RED}[install] Unknown argument: $1${NC}"
            exit 1
            ;;
    esac
done

abort() {
    echo -e "${RED}[install] FATAL: $1${NC}" >&2
    exit 1
}

# --- Resolve paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="binjaXfrida"
TARGET_DIR="${BINJA_PLUGINS_DIR}/${PLUGIN_NAME}"

echo -e "${CYAN}[install] Source:  ${SCRIPT_DIR}${NC}"
echo -e "${CYAN}[install] Target:  ${TARGET_DIR}${NC}"

# --- Validate source directory ---
[[ -d "$SCRIPT_DIR" ]] || abort "Source directory does not exist: ${SCRIPT_DIR}"

# --- Validate plugins parent directory ---
[[ -d "$BINJA_PLUGINS_DIR" ]] || abort "Binary Ninja plugins directory does not exist: ${BINJA_PLUGINS_DIR}"

# --- Validate required source items exist before doing anything ---
ITEMS=(
    "__init__.py"
    "log.py"
    "plugin.json"
    "LICENSE"
    "core"
    "actions"
    "ui"
    "templates"
)

for item in "${ITEMS[@]}"; do
    [[ -e "${SCRIPT_DIR}/${item}" ]] || abort "Required item '${item}' not found at: ${SCRIPT_DIR}/${item}"
done
echo -e "${GREEN}[install] All required source items verified.${NC}"

# --- Clean previous install ---
if [[ -d "$TARGET_DIR" ]]; then
    echo -e "${YELLOW}[install] Removing existing plugin folder...${NC}"
    rm -rf "$TARGET_DIR"

    [[ ! -e "$TARGET_DIR" ]] || abort "Failed to remove existing plugin folder: ${TARGET_DIR}"
    echo -e "${GREEN}[install] Existing folder removed.${NC}"
else
    echo -e "${GREEN}[install] No existing plugin folder found (clean install).${NC}"
fi

# --- Create fresh target directory ---
mkdir -p "$TARGET_DIR"

[[ -d "$TARGET_DIR" ]] || abort "Failed to create target directory: ${TARGET_DIR}"

if [[ -n "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]]; then
    abort "Target directory is not empty after creation: ${TARGET_DIR}"
fi
echo -e "${GREEN}[install] Target directory created and verified empty.${NC}"

# --- Copy items ---
for item in "${ITEMS[@]}"; do
    src="${SCRIPT_DIR}/${item}"
    dst="${TARGET_DIR}/${item}"

    if [[ -d "$src" ]]; then
        cp -r "$src" "$dst"
    else
        cp "$src" "$dst"
    fi

    [[ -e "$dst" ]] || abort "Failed to copy '${item}' to: ${dst}"
    echo -e "${GREEN}[install] Copied ${item}${NC}"
done

# --- Remove __pycache__ directories from the copy ---
while IFS= read -r -d '' pycache; do
    echo -e "${YELLOW}[install] Removing __pycache__: ${pycache}${NC}"
    rm -rf "$pycache"
    [[ ! -e "$pycache" ]] || abort "Failed to remove __pycache__: ${pycache}"
done < <(find "$TARGET_DIR" -type d -name "__pycache__" -print0 2>/dev/null)

echo -e "${GREEN}[install] Plugin deployed successfully!${NC}"

# --- Restart Binary Ninja ---
if $NO_RESTART; then
    echo -e "${YELLOW}[install] Skipping Binary Ninja restart (--no-restart).${NC}"
    exit 0
fi

if pgrep -x binaryninja >/dev/null 2>&1; then
    BN_PID="$(pgrep -x binaryninja | head -n1)"
    echo -e "${YELLOW}[install] Stopping Binary Ninja (PID: ${BN_PID})...${NC}"
    pkill -x binaryninja
    sleep 2

    if pgrep -x binaryninja >/dev/null 2>&1; then
        abort "Failed to stop Binary Ninja."
    fi
    echo -e "${GREEN}[install] Binary Ninja stopped.${NC}"
else
    echo -e "${YELLOW}[install] Binary Ninja is not running.${NC}"
fi

SEARCH_PATHS=(
    "/opt/binaryninja"
    "${HOME}/binaryninja"
    "/usr/local/binaryninja"
)

BN_EXE=""
for dir in "${SEARCH_PATHS[@]}"; do
    if [[ -x "${dir}/binaryninja" ]]; then
        BN_EXE="${dir}/binaryninja"
        break
    fi
done

if [[ -z "$BN_EXE" ]]; then
    BN_EXE="$(command -v binaryninja 2>/dev/null || true)"
fi

if [[ -n "$BN_EXE" ]]; then
    echo -e "${CYAN}[install] Starting Binary Ninja: ${BN_EXE}${NC}"
    nohup "$BN_EXE" >/dev/null 2>&1 &
else
    echo -e "${YELLOW}[install] Could not locate binaryninja. Please start it manually.${NC}"
fi
