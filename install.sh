#!/bin/bash
# DANDADAN Omarchy Theme Installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/main/install.sh | bash
#   OR:
#   bash install.sh [--update] [--uninstall]

set -e

THEME_NAME="dandadan"
REPO_URL="https://github.com/misternegative21/omarchy-Dandadan-Theme"
THEME_DIR="$HOME/.config/omarchy/themes/$THEME_NAME"
HOOKS_DIR="$HOME/.config/omarchy/hooks"
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
   https://github.com/misternegative21/omarchy-Dandadan-Theme

EOF
}

log()   { echo -e "${GREEN}[+]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
err()   { echo -e "${RED}[✗]${NC} $*" >&2; }
step()  { echo -e "\n${BOLD}${CYAN}━━ $* ${NC}"; }

check_deps() {
  step "Checking dependencies"
  for dep in git python3 waybar; do
    if command -v "$dep" &>/dev/null; then
      log "$dep ✓"
    else
      err "$dep not found – please install it first."
      exit 1
    fi
  done
  if ! python3 -c "from PIL import Image" &>/dev/null; then
    warn "Pillow not found. Installing..."
    pip3 install Pillow -q || true
  fi
}

backup_waybar() {
  step "Backing up Waybar defaults"
  if [[ -f "$WAYBAR_DIR/config.jsonc" && ! -f "$WAYBAR_DIR/config.jsonc.default" ]]; then
    cp -f "$WAYBAR_DIR/config.jsonc" "$WAYBAR_DIR/config.jsonc.default"
    log "Backed up config.jsonc.default"
  fi
  if [[ -f "$WAYBAR_DIR/style.css" && ! -f "$WAYBAR_DIR/style.css.default" ]]; then
    cp -f "$WAYBAR_DIR/style.css" "$WAYBAR_DIR/style.css.default"
    log "Backed up style.css.default"
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
    log "Updating existing installation..."
    git -C "$THEME_DIR" pull --ff-only
  else
    log "Cloning from GitHub..."
    git clone --depth 1 "$REPO_URL" "$THEME_DIR"
  fi

  log "Theme files installed to $THEME_DIR"
}

install_hook() {
  step "Installing Omarchy hooks"
  mkdir -p "$HOOKS_DIR"

  # theme-set hook
  THEME_SET="$HOOKS_DIR/theme-set"
  if [[ ! -f "$THEME_SET" ]]; then
    cat > "$THEME_SET" << 'HOOK'
#!/bin/bash
THEME="$1"
if [[ "$THEME" == "dandadan" ]]; then
  python3 "$HOME/.config/omarchy/themes/dandadan/update_wallpaper_colors.py" 2>/dev/null
  [[ -f "$HOME/.config/omarchy/themes/dandadan/config.jsonc" ]] && \
    cp -f "$HOME/.config/omarchy/themes/dandadan/config.jsonc" "$HOME/.config/waybar/config.jsonc"
  [[ -f "$HOME/.config/omarchy/themes/dandadan/style.css" ]] && \
    cp -f "$HOME/.config/omarchy/themes/dandadan/style.css" "$HOME/.config/waybar/style.css"
else
  [[ -f "$HOME/.config/waybar/config.jsonc.default" ]] && \
    cp -f "$HOME/.config/waybar/config.jsonc.default" "$HOME/.config/waybar/config.jsonc"
  [[ -f "$HOME/.config/waybar/style.css.default" ]] && \
    cp -f "$HOME/.config/waybar/style.css.default" "$HOME/.config/waybar/style.css"
fi
omarchy-restart-waybar >/dev/null 2>&1 &
HOOK
    chmod +x "$THEME_SET"
    log "theme-set hook installed"
  else
    log "theme-set hook already exists – skipping"
  fi

  # bg-set hook
  BG_SET="$HOOKS_DIR/bg-set"
  cat > "$BG_SET" << 'HOOK'
#!/bin/bash
THEME=$(cat "$HOME/.config/omarchy/current/theme.name" 2>/dev/null)
if [[ "$THEME" == "dandadan" ]]; then
  python3 "$HOME/.config/omarchy/themes/dandadan/update_wallpaper_colors.py"
  pkill -SIGUSR2 waybar 2>/dev/null || true
fi
HOOK
  chmod +x "$BG_SET"
  log "bg-set hook installed"
}

extract_colors() {
  step "Extracting per-wallpaper accent colors"
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

  for dir in "$VSCODE_THEME_DIR" "$CODIUM_THEME_DIR"; do
    if [[ -d "$(dirname "$dir")" ]] || [[ -d "$(dirname "$(dirname "$dir")")" ]]; then
      mkdir -p "$dir"
      cp -f "$THEME_DIR/vscode.json" "$dir/dandadan-color-theme.json"
      # Create package.json for the extension
      cat > "$(dirname "$dir")/package.json" << 'PKG'
{
  "name": "dandadan-theme",
  "displayName": "Dandadan Theme",
  "description": "Dynamic Dandadan anime-inspired dark theme for VS Code",
  "version": "1.0.0",
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

activate_theme() {
  step "Activating Dandadan theme"
  if command -v omarchy-theme-set &>/dev/null; then
    omarchy-theme-set dandadan
    log "Theme activated via omarchy-theme-set"
  else
    log "Run: omarchy-theme-set dandadan"
  fi
  waybar >/dev/null 2>&1 &
  log "Waybar restarted"
}

uninstall_theme() {
  step "Uninstalling Dandadan theme"
  [[ -d "$THEME_DIR" ]] && rm -rf "$THEME_DIR" && log "Removed $THEME_DIR"
  [[ -f "$HOOKS_DIR/bg-set" ]] && rm -f "$HOOKS_DIR/bg-set" && log "Removed bg-set hook"
  log "Uninstall complete. Run: omarchy-theme-set <your-theme>"
  exit 0
}

# ── Main ───────────────────────────────────────────────────────────────────────
banner

case "${1:-}" in
  --uninstall) uninstall_theme ;;
  --update)
    check_deps
    install_theme --update
    extract_colors
    activate_theme
    ;;
  *)
    check_deps
    backup_waybar
    install_theme
    install_hook
    extract_colors
    install_vscode_theme
    activate_theme
    ;;
esac

echo ""
echo -e "${BOLD}${GREEN}✓ Dandadan theme installed successfully!${NC}"
echo -e "  GitHub : $REPO_URL"
echo -e "  Wallpapers cycle: ${CYAN}omarchy theme bg next${NC}"
echo -e "  Activate theme  : ${CYAN}omarchy-theme-set dandadan${NC}"
echo ""
