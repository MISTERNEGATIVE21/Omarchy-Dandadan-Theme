#!/bin/bash
# DANDADAN Omarchy Theme Installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/master/install.sh | bash
#   OR:
#   bash install.sh [--update] [--uninstall]

set -e

THEME_NAME="dandadan-theme"
REPO_URL="https://github.com/misternegative21/omarchy-Dandadan-Theme"
THEME_DIR="$HOME/.config/omarchy/themes/$THEME_NAME"
HOOKS_DIR="${HOOKS_DIR:-$HOME/.config/omarchy/hooks}"
WAYBAR_DIR="$HOME/.config/waybar"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

banner() {
cat << 'EOF'

 ██████╗  █████╗ ███╗   ██╗██████╗  █████╗ ██████╗  █████╗ ███╗   ██╗
 ██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗  ██║
 ██║  ██║███████║██╔██╗ ██║██║  ██║███████║██║  ██║███████║██╔██╗ ██║
 ██║  ██║██╔══██║██║╚██╗██║██║  ██║██╔══██║██║  ██║██╔══██║██║╚██╗██║
 ██████╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║██████╔╝██║  ██║██║ ╚████║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝

   Omarchy Theme by misternegative21 – Dynamic Wallpaper Accent Edition
   52 wallpapers · 21 app targets · per-image accent + complement theming
   https://github.com/misternegative21/omarchy-Dandadan-Theme

EOF
}

log()   { echo -e "${GREEN}[+]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
err()   { echo -e "${RED}[✗]${NC} $*" >&2; }
step()  { echo -e "\n${BOLD}${CYAN}━━ $* ${NC}"; }

check_deps() {
  step "Checking dependencies"
  for dep in git python3; do
    if command -v "$dep" &>/dev/null; then
      log "$dep ✓"
    else
      err "$dep not found – please install it first."
      exit 1
    fi
  done

  # Check Quickshell (Omarchy 4.0) or Waybar
  if command -v quickshell &>/dev/null || command -v omarchy-shell &>/dev/null; then
    log "Quickshell ✓"
  elif command -v waybar &>/dev/null; then
    log "Waybar ✓"
  else
    err "Neither Quickshell (quickshell/omarchy-shell) nor Waybar (waybar) found – please install one of them."
    exit 1
  fi

  if ! python3 -c "from PIL import Image" &>/dev/null; then
    warn "Pillow not found. Installing..."
    pip3 install Pillow -q || true
  fi
  log "Pillow ✓"
}

backup_waybar() {
  step "Backing up shell defaults"
  if [[ -f "$WAYBAR_DIR/config.jsonc" && ! -f "$WAYBAR_DIR/config.jsonc.default" ]]; then
    cp -f "$WAYBAR_DIR/config.jsonc" "$WAYBAR_DIR/config.jsonc.default"
    log "Backed up config.jsonc.default"
  fi
  if [[ -f "$WAYBAR_DIR/style.css" && ! -f "$WAYBAR_DIR/style.css.default" ]]; then
    cp -f "$WAYBAR_DIR/style.css" "$WAYBAR_DIR/style.css.default"
    log "Backed up style.css.default"
  fi
  if [[ -f "$HOME/.config/omarchy/shell.json" && ! -f "$HOME/.config/omarchy/shell.json.omarchy-default" ]]; then
    cp -f "$HOME/.config/omarchy/shell.json" "$HOME/.config/omarchy/shell.json.omarchy-default"
    log "Backed up shell.json.omarchy-default"
  fi
}

install_theme() {
  step "Installing Dandadan theme"

  if [[ -d "$THEME_DIR" && ! "$1" == "--update" ]]; then
    warn "Theme already installed at $THEME_DIR"
    read -rp "    Reinstall / overwrite? [y/N]: " ans
    [[ "${ans,,}" == "y" ]] || { log "Aborted."; exit 0; }
  fi

  # Clone or pull latest
  if [[ -d "$THEME_DIR/.git" ]]; then
    if [[ "$THEME_DIR" != "$(pwd)" ]]; then
      log "Updating existing installation..."
      git -C "$THEME_DIR" pull --ff-only || true
    else
      log "Running from repository directory – using current repository files"
    fi
  else
    log "Cloning from GitHub..."
    git clone --depth 1 "$REPO_URL" "$THEME_DIR"
  fi

  log "Theme files installed to $THEME_DIR"
}

install_hooks() {
  step "Installing Omarchy hooks"
  mkdir -p "$HOOKS_DIR"

  # ── theme-set hook ────────────────────────────────────────────────────────
  THEME_SET_HOOK="$HOOKS_DIR/theme-set"
  cat > "$THEME_SET_HOOK" << 'HOOK'
#!/bin/bash
THEME="$1"

if [[ "$THEME" == "dandadan" || "$THEME" == "dandadan-theme" ]]; then
  DANDADAN_DIR="$HOME/.config/omarchy/themes/dandadan-theme"
  DETECT_SCRIPT="$DANDADAN_DIR/scripts/detect_shell.sh"

  SHELL_MODE="quickshell"
  if [[ -x "$DETECT_SCRIPT" ]]; then
    SHELL_MODE=$("$DETECT_SCRIPT" --primary 2>/dev/null || echo "quickshell")
  elif command -v quickshell &>/dev/null || command -v omarchy-shell &>/dev/null; then
    SHELL_MODE="quickshell"
  fi

  if [[ "$SHELL_MODE" == "quickshell" || "$SHELL_MODE" == "dual" ]]; then
    # Backup default Quickshell config if not already backed up
    if [[ ! -f "$HOME/.config/omarchy/shell.json.omarchy-default" ]]; then
      if [[ -f "$HOME/.config/omarchy/shell.json" ]]; then
        cp -f "$HOME/.config/omarchy/shell.json" "$HOME/.config/omarchy/shell.json.omarchy-default"
      fi
    fi

    # Deploy Dandadan shell layout
    if [[ -f "$DANDADAN_DIR/shell.json" ]]; then
      cp -f "$DANDADAN_DIR/shell.json" "$HOME/.config/omarchy/shell.json"
    fi
  fi

  if [[ "$SHELL_MODE" == "waybar" || "$SHELL_MODE" == "dual" ]]; then
    # Backup system default waybar config if not already backed up
    if [[ ! -f "$HOME/.config/waybar/config.jsonc.omarchy-default" ]]; then
      if [[ -f "$HOME/.config/waybar/config.jsonc" ]]; then
        cp -f "$HOME/.config/waybar/config.jsonc" "$HOME/.config/waybar/config.jsonc.omarchy-default"
      fi
    fi

    # Deploy Dandadan waybar layout
    if [[ -f "$DANDADAN_DIR/waybar_config.jsonc" ]]; then
      cp -f "$DANDADAN_DIR/waybar_config.jsonc" "$HOME/.config/waybar/config.jsonc"
    fi

    (pkill -SIGUSR2 waybar >/dev/null 2>&1 || true) &
  fi

  # Deploy Fastfetch Dandadan config
  if [[ -f "$DANDADAN_DIR/fastfetch/config.jsonc" ]]; then
    mkdir -p "$HOME/.config/fastfetch"
    if [[ ! -f "$HOME/.config/fastfetch/config.jsonc.omarchy-default" && -f "$HOME/.config/fastfetch/config.jsonc" ]]; then
      cp -f "$HOME/.config/fastfetch/config.jsonc" "$HOME/.config/fastfetch/config.jsonc.omarchy-default"
    fi
    cp -f "$DANDADAN_DIR/fastfetch/config.jsonc" "$HOME/.config/fastfetch/config.jsonc"
  fi

  # Deploy Quickshell Menu Extension
  if [[ -f "$DANDADAN_DIR/extensions/omarchy-menu.jsonc" ]]; then
    mkdir -p "$HOME/.config/omarchy/extensions"
    if [[ ! -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc.omarchy-bak" && -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc" ]]; then
      cp -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc" "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc.omarchy-bak"
    fi
    cp -f "$DANDADAN_DIR/extensions/omarchy-menu.jsonc" "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc"
  fi

  # Deploy Plugin to ~/.config/omarchy/plugins/dandadan.theme-control
  if [[ -d "$DANDADAN_DIR/plugins/dandadan.theme-control" ]]; then
    mkdir -p "$HOME/.config/omarchy/plugins/dandadan.theme-control"
    cp -rf "$DANDADAN_DIR/plugins/dandadan.theme-control"/* "$HOME/.config/omarchy/plugins/dandadan.theme-control"/
  fi

  SCRIPT_PATH="$HOME/.local/state/omarchy/current/theme/update_wallpaper_colors.py"
  if [[ ! -f "$SCRIPT_PATH" ]]; then
    SCRIPT_PATH="$HOME/.config/omarchy/current/theme/update_wallpaper_colors.py"
  fi
  if [[ ! -f "$SCRIPT_PATH" ]]; then
    SCRIPT_PATH="$DANDADAN_DIR/update_wallpaper_colors.py"
  fi

  if [[ -f "$SCRIPT_PATH" ]]; then
    (python3 "$SCRIPT_PATH" >/dev/null 2>&1) &
  fi

  # Start live wallpaper change watcher
  WATCH_SCRIPT="$DANDADAN_DIR/scripts/dandadan-bg-watch.sh"
  if [[ -x "$WATCH_SCRIPT" ]] && ! pgrep -f "dandadan-bg-watch" >/dev/null 2>&1; then
    (bash "$WATCH_SCRIPT" >/dev/null 2>&1) &
  fi
else
  # Switching away to another Omarchy theme: Cleanly turn OFF all Dandadan addons, music & ricing

  # 1. Terminate all Dandadan background music, radio, and watcher daemons
  pkill -f "dandadan-music" >/dev/null 2>&1 || true
  pkill -f "dandadan-anime-radio" >/dev/null 2>&1 || true
  pkill -f "dandadan-bg-watch" >/dev/null 2>&1 || true
  rm -f /tmp/dandadan-music.pid 2>/dev/null || true

  # 2. Restore standard Omarchy shell.json layout (removing dandadan.theme-control widget)
  if [[ -f "$HOME/.config/omarchy/shell.json.omarchy-default" ]]; then
    cp -f "$HOME/.config/omarchy/shell.json.omarchy-default" "$HOME/.config/omarchy/shell.json"
  else
    python3 -c '
import json, os
p = os.path.expanduser("~/.config/omarchy/shell.json")
try:
    with open(p) as f: d = json.load(f)
    d["plugins"] = [x for x in d.get("plugins", []) if "dandadan" not in str(x)]
    for sec in ["left", "center", "right"]:
        if sec in d.get("bar", {}).get("layout", {}):
            d["bar"]["layout"][sec] = [w for w in d["bar"]["layout"][sec] if "dandadan" not in str(w.get("id", ""))]
    with open(p, "w") as f: json.dump(d, f, indent=2)
except Exception: pass
' 2>/dev/null || true
  fi

  # 3. Restore standard Waybar config
  if [[ -f "$HOME/.config/waybar/config.jsonc.omarchy-default" ]]; then
    cp -f "$HOME/.config/waybar/config.jsonc.omarchy-default" "$HOME/.config/waybar/config.jsonc"
  elif [[ -f "/usr/share/omarchy/config/waybar/config.jsonc" ]]; then
    cp -f "/usr/share/omarchy/config/waybar/config.jsonc" "$HOME/.config/waybar/config.jsonc"
  fi

  # 4. Restore fastfetch config
  if [[ -f "$HOME/.config/fastfetch/config.jsonc.omarchy-default" ]]; then
    cp -f "$HOME/.config/fastfetch/config.jsonc.omarchy-default" "$HOME/.config/fastfetch/config.jsonc"
  else
    rm -f "$HOME/.config/fastfetch/config.jsonc" 2>/dev/null || true
  fi

  # 5. Remove Dandadan user menu extension so other themes have a standard menu
  if [[ -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc.omarchy-bak" ]]; then
    cp -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc.omarchy-bak" "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc"
  elif [[ -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc" ]]; then
    rm -f "$HOME/.config/omarchy/extensions/omarchy-menu.jsonc"
  fi

  # 6. Notify running shell to rescan plugins and reload config
  if command -v omarchy-shell &>/dev/null; then
    omarchy-shell -q shell rescanPlugins >/dev/null 2>&1 || true
    omarchy-shell -q shell reloadConfig >/dev/null 2>&1 || true
  fi
  (pkill -SIGUSR2 waybar >/dev/null 2>&1 || true) &
fi
HOOK
  chmod +x "$THEME_SET_HOOK"
  mkdir -p "$HOOKS_DIR/theme-set.d"
  cp -f "$THEME_SET_HOOK" "$HOOKS_DIR/theme-set.d/dandadan-theme-set"
  chmod +x "$HOOKS_DIR/theme-set.d/dandadan-theme-set"
  log "theme-set hook installed (Quickshell & Waybar support for Dandadan)"

  # ── bg-set hook (fires on wallpaper change) ──────────────────────────────
  BG_SET_HOOK="$HOOKS_DIR/bg-set"
  cat > "$BG_SET_HOOK" << 'HOOK'
#!/bin/bash
THEME=""
if [[ -f "$HOME/.local/state/omarchy/current/theme.name" ]]; then
  THEME=$(cat "$HOME/.local/state/omarchy/current/theme.name" 2>/dev/null)
elif [[ -f "$HOME/.config/omarchy/current/theme.name" ]]; then
  THEME=$(cat "$HOME/.config/omarchy/current/theme.name" 2>/dev/null)
fi

if [[ "$THEME" == "dandadan" || "$THEME" == "dandadan-theme" ]]; then
  SCRIPT_PATH="$HOME/.local/state/omarchy/current/theme/update_wallpaper_colors.py"
  if [[ ! -f "$SCRIPT_PATH" ]]; then
    SCRIPT_PATH="$HOME/.config/omarchy/current/theme/update_wallpaper_colors.py"
  fi
  if [[ ! -f "$SCRIPT_PATH" ]]; then
    SCRIPT_PATH="$HOME/.config/omarchy/themes/dandadan-theme/update_wallpaper_colors.py"
  fi

  if [[ -f "$SCRIPT_PATH" ]]; then
    (python3 "$SCRIPT_PATH" >/dev/null 2>&1 && pkill -SIGUSR2 waybar >/dev/null 2>&1) &
  fi
fi
HOOK
  chmod +x "$BG_SET_HOOK"
  log "bg-set hook installed (non-blocking wallpaper recoloring)"

  # Start background watcher daemon if not already running
  if [[ -x "$THEME_DIR/scripts/dandadan-bg-watch.sh" ]] && ! pgrep -f "dandadan-bg-watch" >/dev/null 2>&1; then
    (bash "$THEME_DIR/scripts/dandadan-bg-watch.sh" >/dev/null 2>&1) &
    log "dandadan-bg-watch daemon started"
  fi
}

extract_colors() {
  step "Extracting per-wallpaper accent colors (52 wallpapers)"
  if [[ -f "$THEME_DIR/wallpaper_highlights.json" ]] && [[ "${1:-}" != "--force" ]]; then
    log "Curated wallpaper palettes verified in wallpaper_highlights.json (52 wallpapers) ✓"
    return 0
  fi
  if [[ -d "$THEME_DIR/backgrounds" ]]; then
    python3 "$THEME_DIR/extract_wallpaper_colors.py"
    log "Accent palette generated from wallpapers"
  else
    warn "No backgrounds/ folder found – skipping color extraction"
  fi
}

install_vscode_theme() {
  step "Installing VS Code / Codium / Antigravity IDE theme"
  VSCODE_THEME_DIR="$HOME/.vscode/extensions/dandadan-theme/themes"
  CODIUM_THEME_DIR="$HOME/.config/VSCodium/User/extensions/dandadan-theme/themes"
  AGY_THEME_DIR="$HOME/.config/antigravity/extensions/dandadan-theme/themes"

  for dir in "$VSCODE_THEME_DIR" "$CODIUM_THEME_DIR" "$AGY_THEME_DIR"; do
    parent="$(dirname "$(dirname "$dir")")"
    if [[ -d "$parent" ]] || [[ -d "$(dirname "$dir")" ]]; then
      mkdir -p "$dir"
      cp -f "$THEME_DIR/vscode.json" "$dir/dandadan-color-theme.json"
      cat > "$(dirname "$dir")/package.json" << 'PKG'
{
  "name": "dandadan-theme",
  "displayName": "Dandadan Theme",
  "description": "Dynamic Dandadan anime-inspired dark theme",
  "version": "2.0.0",
  "publisher": "misternegative21",
  "engines": { "vscode": "^1.60.0" },
  "categories": ["Themes"],
  "contributes": {
    "themes": [{
      "label": "Dandadan",
      "uiTheme": "vs-dark",
      "path": "./themes/dandadan-color-theme.json"
    }]
  }
}
PKG
      log "VS Code theme installed at $dir"
    fi
  done
}

install_zellij_theme() {
  step "Installing Zellij theme"
  if command -v zellij &>/dev/null || [[ -d "$HOME/.config/zellij" ]]; then
    mkdir -p "$HOME/.config/zellij/themes"
    cp -f "$THEME_DIR/zellij.kdl" "$HOME/.config/zellij/themes/dandadan.kdl"
    log "Zellij theme installed at ~/.config/zellij/themes/dandadan.kdl"
  else
    log "Zellij not found – skipping"
  fi
}

install_warp_theme() {
  step "Installing Warp terminal theme"
  WARP_THEMES_DIR="$HOME/.local/share/warp-terminal/themes"
  if [[ -d "$(dirname "$WARP_THEMES_DIR")" ]]; then
    mkdir -p "$WARP_THEMES_DIR"
    cp -f "$THEME_DIR/warp.yaml" "$WARP_THEMES_DIR/dandadan.yaml"
    log "Warp theme installed at $WARP_THEMES_DIR/dandadan.yaml"
  else
    log "Warp not found – skipping"
  fi
}

install_wofi_theme() {
  step "Installing Wofi launcher theme"
  if command -v wofi &>/dev/null || [[ -d "$HOME/.config/wofi" ]]; then
    mkdir -p "$HOME/.config/wofi"
    cp -f "$THEME_DIR/wofi.css" "$HOME/.config/wofi/style.css"
    log "Wofi theme installed at ~/.config/wofi/style.css"
  else
    log "Wofi not found – skipping"
  fi
}

install_vencord_theme() {
  step "Installing Vencord / Vesktop theme"
  for vesktop_path in \
    "$HOME/.config/vesktop/themes" \
    "$HOME/.var/app/dev.vencord.Vesktop/config/vesktop/themes"
  do
    parent="$(dirname "$vesktop_path")"
    if [[ -d "$parent" ]]; then
      mkdir -p "$vesktop_path"
      cp -f "$THEME_DIR/vencord.theme.css" "$vesktop_path/dandadan.theme.css"
      log "Vencord theme installed at $vesktop_path"
    fi
  done
}

activate_theme() {
  step "Activating Dandadan theme"
  if command -v omarchy-theme-set &>/dev/null; then
    omarchy-theme-set dandadan-theme
    log "Theme activated via omarchy-theme-set"
  else
    warn "omarchy-theme-set not found – copy files manually to ~/.config/omarchy/current/theme/"
  fi
}

install_terminal_configs() {
  step "Configuring terminal themes (Kitty, Alacritty, Ghostty, Foot)"

  # Kitty
  if command -v kitty &>/dev/null || [[ -d "$HOME/.config/kitty" ]]; then
    mkdir -p "$HOME/.config/kitty"
    KITTY_USER="$HOME/.config/kitty/kitty.conf"
    if [[ -f "$KITTY_USER" ]]; then
      if ! grep -q "current/theme/kitty.conf" "$KITTY_USER"; then
        sed -i '1iinclude ~/.local/state/omarchy/current/theme/kitty.conf\n' "$KITTY_USER"
      fi
    else
      echo "include ~/.local/state/omarchy/current/theme/kitty.conf" > "$KITTY_USER"
    fi
    log "Kitty configured to import theme"
  fi

  # Alacritty
  if command -v alacritty &>/dev/null || [[ -d "$HOME/.config/alacritty" ]]; then
    mkdir -p "$HOME/.config/alacritty"
    ALACRITTY_USER="$HOME/.config/alacritty/alacritty.toml"
    if [[ -f "$ALACRITTY_USER" ]]; then
      if ! grep -q "current/theme/alacritty.toml" "$ALACRITTY_USER"; then
        sed -i '1igeneral.import = [ "~/.local/state/omarchy/current/theme/alacritty.toml" ]\n' "$ALACRITTY_USER"
      fi
    else
      echo 'general.import = [ "~/.local/state/omarchy/current/theme/alacritty.toml" ]' > "$ALACRITTY_USER"
    fi
    log "Alacritty configured to import theme"
  fi

  # Ghostty
  if command -v ghostty &>/dev/null || [[ -d "$HOME/.config/ghostty" ]]; then
    mkdir -p "$HOME/.config/ghostty"
    GHOSTTY_USER="$HOME/.config/ghostty/config"
    if [[ -f "$GHOSTTY_USER" ]]; then
      if ! grep -q "current/theme/ghostty.conf" "$GHOSTTY_USER"; then
        sed -i '1iconfig-file = ?"~/.local/state/omarchy/current/theme/ghostty.conf"\n' "$GHOSTTY_USER"
      fi
    else
      echo 'config-file = ?"~/.local/state/omarchy/current/theme/ghostty.conf"' > "$GHOSTTY_USER"
    fi
    log "Ghostty configured to import theme"
  fi

  # Foot
  if command -v foot &>/dev/null || [[ -d "$HOME/.config/foot" ]]; then
    mkdir -p "$HOME/.config/foot"
    FOOT_USER="$HOME/.config/foot/foot.ini"
    if [[ -f "$FOOT_USER" ]]; then
      if ! grep -q "current/theme/foot.ini" "$FOOT_USER"; then
        if grep -q "^\[main\]" "$FOOT_USER"; then
          sed -i '/^\[main\]/a include=~/.local/state/omarchy/current/theme/foot.ini' "$FOOT_USER"
        else
          sed -i '1i[main]\ninclude=~/.local/state/omarchy/current/theme/foot.ini\n' "$FOOT_USER"
        fi
      fi
    else
      cat > "$FOOT_USER" << 'FOOTCONF'
[main]
include=~/.local/state/omarchy/current/theme/foot.ini
FOOTCONF
    fi
    log "Foot configured to import theme"
  fi
}

install_quickshell_extensions() {
  step "Configuring Quickshell extensions (Dandadan Theme Control & Menu Extensions)"

  # 1. Install Plugin
  PLUGIN_SRC="$THEME_DIR/plugins/dandadan.theme-control"
  PLUGIN_DEST="$HOME/.config/omarchy/plugins/dandadan.theme-control"
  if [[ -d "$PLUGIN_SRC" ]]; then
    mkdir -p "$PLUGIN_DEST"
    cp -rf "$PLUGIN_SRC"/* "$PLUGIN_DEST"/
    if command -v omarchy &>/dev/null; then
      omarchy plugin validate "$PLUGIN_DEST" &>/dev/null || true
    fi
    log "Installed Dandadan Theme Control plugin to ~/.config/omarchy/plugins/"
  fi

  # 2. Install Menu Extensions
  MENU_SRC="$THEME_DIR/extensions/omarchy-menu.jsonc"
  MENU_DEST="$HOME/.config/omarchy/extensions/omarchy-menu.jsonc"
  if [[ -f "$MENU_SRC" ]]; then
    mkdir -p "$(dirname "$MENU_DEST")"
    if [[ ! -f "$MENU_DEST" ]] || ! grep -q "dandadan" "$MENU_DEST"; then
      cp -f "$MENU_SRC" "$MENU_DEST"
      log "Installed Dandadan Menu Extension to ~/.config/omarchy/extensions/"
    fi
  fi

  # 3. Ensure dandadan.theme-control is enabled and on bar
  SHELL_JSON="$HOME/.config/omarchy/shell.json"
  if [[ -f "$SHELL_JSON" ]]; then
    python3 -c '
import json, os
p = os.path.expanduser("~/.config/omarchy/shell.json")
try:
    with open(p) as f:
        data = json.load(f)
    changed = False
    plugins = data.setdefault("plugins", [])
    if "dandadan.theme-control" not in plugins:
        plugins.append("dandadan.theme-control")
        changed = True
    right = data.setdefault("bar", {}).setdefault("layout", {}).setdefault("right", [])
    has_widget = any(w.get("id") == "dandadan.theme-control" for w in right if isinstance(w, dict))
    if not has_widget:
        right.insert(0, {"id": "dandadan.theme-control"})
        changed = True
    if changed:
        with open(p, "w") as f:
            json.dump(data, f, indent=2)
except Exception:
    pass
'
    log "Registered dandadan.theme-control widget in ~/.config/omarchy/shell.json"
  fi

  # 4. Trigger Quickshell rescan
  if command -v omarchy-shell &>/dev/null; then
    omarchy-shell -q shell rescanPlugins &>/dev/null || true
    omarchy-shell -q shell reloadConfig &>/dev/null || true
  fi
}

uninstall_theme() {
  step "Uninstalling Dandadan theme"
  [[ -d "$THEME_DIR" ]] && rm -rf "$THEME_DIR" && log "Removed $THEME_DIR"
  [[ -f "$HOOKS_DIR/bg-set" ]] && rm -f "$HOOKS_DIR/bg-set" && log "Removed bg-set hook"
  [[ -f "$HOOKS_DIR/theme-set" ]] && rm -f "$HOOKS_DIR/theme-set" && log "Removed theme-set hook"
  [[ -d "$HOME/.config/omarchy/plugins/dandadan.theme-control" ]] && rm -rf "$HOME/.config/omarchy/plugins/dandadan.theme-control" && log "Removed dandadan.theme-control plugin"
  log "Uninstall complete. Run: omarchy-theme-set <your-theme>"
  exit 0
}

# ── Main ───────────────────────────────────────────────────────────────────────
banner

case "${1:-}" in
  --uninstall) uninstall_theme ;;
  --hooks-only)
    install_hooks
    ;;
  --update)
    check_deps
    install_theme --update
    extract_colors
    install_terminal_configs
    install_quickshell_extensions
    install_vscode_theme
    install_zellij_theme
    install_warp_theme
    install_wofi_theme
    install_vencord_theme
    activate_theme
    ;;
  *)
    check_deps
    backup_waybar
    install_theme
    install_hooks
    extract_colors
    install_terminal_configs
    install_quickshell_extensions
    install_vscode_theme
    install_zellij_theme
    install_warp_theme
    install_wofi_theme
    install_vencord_theme
    activate_theme
    ;;
esac

echo ""
echo -e "${BOLD}${GREEN}✓ Dandadan theme installed successfully!${NC}"
echo -e "  GitHub       : $REPO_URL"
echo -e "  Shell Support: Quickshell (Omarchy 4.0) & Waybar auto-detected"
echo -e "  Wallpapers   : ${CYAN}omarchy theme bg next${NC}  ← auto-recolors all 21 targets"
echo -e "  Activate     : ${CYAN}omarchy-theme-set dandadan-theme${NC}"
echo -e "  Recolor now  : ${CYAN}python3 ~/.config/omarchy/current/theme/update_wallpaper_colors.py${NC}"
echo ""
