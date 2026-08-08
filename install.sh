#!/bin/bash
# DANDADAN Omarchy Theme Installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/main/install.sh | bash
#   OR:
#   bash install.sh [--update] [--uninstall]

set -e

THEME_NAME="dandadan-theme"
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
  log "Pillow ✓"
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

install_hooks() {
  step "Installing Omarchy hooks"
  mkdir -p "$HOOKS_DIR"

  # ── theme-set hook ────────────────────────────────────────────────────────
  THEME_SET_HOOK="$HOOKS_DIR/theme-set"
  if [[ ! -f "$THEME_SET_HOOK" ]]; then
    cat > "$THEME_SET_HOOK" << 'HOOK'
#!/bin/bash
THEME="$1"
if [[ "$THEME" == "dandadan-theme" ]]; then
  python3 "$HOME/.config/omarchy/themes/dandadan-theme/update_wallpaper_colors.py" 2>/dev/null
  # Deploy waybar layout
  [[ -f "$HOME/.config/omarchy/themes/dandadan-theme/waybar_config.jsonc" ]] && \
    cp -f "$HOME/.config/omarchy/themes/dandadan-theme/waybar_config.jsonc" "$HOME/.config/waybar/config.jsonc"
  [[ -f "$HOME/.config/omarchy/themes/dandadan-theme/style.css" ]] && \
    cp -f "$HOME/.config/omarchy/themes/dandadan-theme/style.css" "$HOME/.config/waybar/style.css"
else
  [[ -f "$HOME/.config/waybar/config.jsonc.default" ]] && \
    cp -f "$HOME/.config/waybar/config.jsonc.default" "$HOME/.config/waybar/config.jsonc"
  [[ -f "$HOME/.config/waybar/style.css.default" ]] && \
    cp -f "$HOME/.config/waybar/style.css.default" "$HOME/.config/waybar/style.css"
fi
omarchy-restart-waybar >/dev/null 2>&1 &
HOOK
    chmod +x "$THEME_SET_HOOK"
    log "theme-set hook installed"
  else
    log "theme-set hook already exists – skipping"
  fi

  # ── bg-set hook (fires on every wallpaper change) ─────────────────────────
  BG_SET_HOOK="$HOOKS_DIR/bg-set"
  cat > "$BG_SET_HOOK" << 'HOOK'
#!/bin/bash
THEME=$(cat "$HOME/.config/omarchy/current/theme.name" 2>/dev/null)
if [[ "$THEME" == "dandadan-theme" ]]; then
  python3 "$HOME/.config/omarchy/current/theme/update_wallpaper_colors.py" 2>/dev/null
  pkill -SIGUSR2 waybar 2>/dev/null || true
fi
HOOK
  chmod +x "$BG_SET_HOOK"
  log "bg-set hook installed (auto-recolors on wallpaper switch)"
}

extract_colors() {
  step "Extracting per-wallpaper accent colors (52 wallpapers)"
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

uninstall_theme() {
  step "Uninstalling Dandadan theme"
  [[ -d "$THEME_DIR" ]] && rm -rf "$THEME_DIR" && log "Removed $THEME_DIR"
  [[ -f "$HOOKS_DIR/bg-set" ]] && rm -f "$HOOKS_DIR/bg-set" && log "Removed bg-set hook"
  [[ -f "$HOOKS_DIR/theme-set" ]] && rm -f "$HOOKS_DIR/theme-set" && log "Removed theme-set hook"
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
echo -e "  GitHub      : $REPO_URL"
echo -e "  Wallpapers  : ${CYAN}omarchy theme bg next${NC}  ← auto-recolors everything"
echo -e "  Activate    : ${CYAN}omarchy-theme-set dandadan-theme${NC}"
echo -e "  Recolor now : ${CYAN}python3 ~/.config/omarchy/current/theme/update_wallpaper_colors.py${NC}"
echo ""
