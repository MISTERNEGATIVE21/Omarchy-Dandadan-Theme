# Omarchy 4.0 Quickshell UI Redesign & Shell Detection Design Document

**Date:** 2026-08-14  
**Author:** Antigravity  
**Branch:** `feat/omarchy-4-quickshell`  
**Repository:** `omarchy-Dandadan-Theme` (`~/.config/omarchy/themes/dandadan-theme`)

---

## 1. Context & Motivation

Omarchy released version 4.0 (Quattro), transitioning from Waybar to Quickshell (`omarchy-shell`) for the unified status bar, notifications, OSD, lock screen, and system menus. Omarchy 4.0 also migrated state directories from `~/.config/omarchy/current/` to `~/.local/state/omarchy/current/` and adopted a Lua-based configuration system for Hyprland (`hyprland.lua`).

The Dandadan theme requires:
1. Complete native Quickshell GUI dotfiles (`shell.toml`, `shell.lock.toml`, `shell.json`, `hyprland.lua`).
2. Dual-shell detection and compatibility support: prioritizing Quickshell on Omarchy 4.0 while providing fallback support for Waybar on older or custom setups.
3. Upgraded dynamic color engine (`update_wallpaper_colors.py`) to generate all Quickshell and GUI target configs dynamically on wallpaper changes with live Quickshell IPC reload.
4. Upgraded hooks and installer (`install.sh`, `hooks/theme-set`, `hooks/bg-set`, `scripts/detect_shell.sh`).

---

## 2. Architectural Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Dandadan Theme Engine                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌───────────────────────┐             ┌───────────────────────┐
│ Priority 1:           │             │ Priority 2 (Fallback):│
│ Quickshell Engine     │             │ Waybar Engine         │
├───────────────────────┤             ├───────────────────────┤
│ • shell.toml          │             │ • waybar.css          │
│ • shell.lock.toml     │             │ • waybar_config.jsonc │
│ • shell.json          │             │ • pkill -SIGUSR2      │
│ • hyprland.lua        │             │   waybar              │
│ • omarchy-shell IPC   │             │ • omarchy-restart-    │
│                       │             │   waybar              │
└───────────────────────┘             └───────────────────────┘
```

### 2.1 Shell Detection Strategy (`scripts/detect_shell.sh`)
* **Detection Logic**:
  1. Inspect running processes for `quickshell` or `omarchy-shell`.
  2. Inspect binary availability: `which omarchy-shell` / `/usr/share/omarchy/bin/omarchy-shell` / `which quickshell`.
  3. Inspect Omarchy version file (`/usr/share/omarchy/version`) and state directories (`~/.local/state/omarchy/`).
  4. Inspect Waybar: `which waybar` and `pgrep -x waybar`.
* **Output**: `quickshell`, `waybar`, or `dual`.

### 2.2 Path Resolution
Dynamic path handling supporting both Omarchy 4.0+ and Omarchy 3.x:
* `STATE_THEME_DIR`: `$HOME/.local/state/omarchy/current/theme` (fallback: `$HOME/.config/omarchy/current/theme`)
* `STATE_BG_LINK`: `$HOME/.local/state/omarchy/current/background` (fallback: `$HOME/.config/omarchy/current/background`)
* `STATE_NAME_FILE`: `$HOME/.local/state/omarchy/current/theme.name` (fallback: `$HOME/.config/omarchy/current/theme.name`)

---

## 3. UI & GUI Dotfile Specifications

### 3.1 `shell.toml` (Quickshell Theme Configuration)
Defines design tokens with Dandadan anime aesthetics (translucent dark glass, neon accent highlights, glowing focus states):
* `[bar]`: `background = "{{ background }}"`, `background-alpha = 0.88`, `text = "{{ foreground }}"`, `active = "{{ red }}"`, `scale-with-font = true`, `size-horizontal = 30`.
* `[hyprland]`: `active-border = "{{ shell_gradient hyprland_active_border accent }}"`, `active-border-foreground = "{{ shell_gradient hyprland_active_border foreground }}"`.
* `[controls]`: `hover-cursor-fill-alpha = 0.12`, `selected-fill-alpha = 0.22`, `selected-border = "{{ accent }}"`, `selected-border-width = 1`.
* `[popups]`, `[tooltip]`, `[notifications]`: Translucent panels (`alpha = 0.95`), accent countdowns, glowing active borders.
* `[launcher]`, `[menu]`, `[polkit]`, `[lock]`, `[image-picker]`: High contrast typography, customized scrim darkening, glowing selection outlines.

### 3.2 `shell.lock.toml` (Lock Screen Specialization)
* Specialized tokens for the centered lock authentication card with Turbo Granny & Okarun cursed energy glows.

### 3.3 `shell.json` (Dandadan Layout Preset)
* Custom bar layout:
  * **Left**: `omarchy.menu` + `omarchy.workspaces`
  * **Center**: `omarchy.indicators` + `omarchy.clock` (`"format": "dddd HH:mm"`) + `omarchy.keyboard-layout` + `omarchy.weather` + `omarchy.system-update`
  * **Right**: `omarchy.tray` + `omarchy.tailscale` + `omarchy.audio` + `omarchy.bluetooth` + `omarchy.network` + `omarchy.monitor` + `omarchy.power`

### 3.4 `hyprland.lua` (Hyprland Lua Configuration)
* Uses `hl.config()` to set:
  * `general.col.active_border`: Multi-stop dynamic gradient (accent + cursor/glow at 45deg).
  * `general.col.inactive_border`: `rgba(61636780)`.
  * `decoration.shadow`: Active window glow matching wallpaper accent (`range = 10`, `render_power = 4`, `color = active_shadow_color`).

---

## 4. Dynamic Color Engine (`update_wallpaper_colors.py`)

### 4.1 Target Expansion
Extends dynamic generation from 21 targets to full Quickshell + Omarchy 4.0 coverage:
1. `shell.toml`
2. `shell.lock.toml`
3. `colors.toml`
4. `hyprland.lua`
5. `hyprland.conf`
6. `hyprlock.conf`
7. `waybar.css` (for Waybar fallback)
8. Terminal & editor targets: Alacritty, Kitty, Foot, Ghostty, Warp, Neovim, Zed, VS Code / Antigravity IDE, Btop, SwayOSD, Mako, Walker, Wofi, Vencord, Telegram, Zellij, etc.

### 4.2 Live IPC Integration
* Upon calculating wallpaper colors:
  * Encodes `colors.toml` and `shell.toml` in base64.
  * Sends IPC call to `omarchy-shell` via `omarchy-shell -q shell applyTheme "$colors_b64" "$shell_b64"`.
  * If Waybar is running, triggers `pkill -SIGUSR2 waybar`.

---

## 5. Hooks & Installer Flow

### 5.1 `install.sh`
* Checks system dependencies (Python3, Pillow, Git, Quickshell/Waybar).
* Creates backups of user configurations.
* Installs/updates theme files in `~/.config/omarchy/themes/dandadan-theme`.
* Installs `hooks/theme-set` and `hooks/bg-set`.
* Installs IDE and app extensions.
* Runs initial color extraction and activates theme via `omarchy-theme-set dandadan-theme`.

### 5.2 `hooks/theme-set`
* Identifies if theme being activated is `dandadan` / `dandadan-theme`.
* Detects shell environment:
  * If Quickshell: Deploys `shell.json` preset (after backup), sets up `shell.toml`.
  * If Waybar: Deploys `waybar_config.jsonc` and restarts Waybar.
* Executes `update_wallpaper_colors.py` in background.

### 5.3 `hooks/bg-set`
* Listens for wallpaper change events (`omarchy theme bg next`).
* Executes `update_wallpaper_colors.py` asynchronously.

---

## 6. Verification & Testing Plan

1. **Detection Test**: Verify `scripts/detect_shell.sh` accurately identifies Quickshell on Omarchy 4.0.
2. **Dynamic Generation Test**: Execute `update_wallpaper_colors.py` across multiple wallpapers (e.g. 01, 32, 41) and verify generated `shell.toml`, `shell.lock.toml`, `colors.toml`, `hyprland.lua`, and all 21 app configs.
3. **Quickshell IPC Test**: Verify `omarchy-shell` accepts `applyTheme` and hot-reloads colors without errors.
4. **Waybar Fallback Test**: Verify Waybar configurations are generated and reloaded when Waybar is active.
5. **Installer & Hook Test**: Test `install.sh --update` and verify hooks fire cleanly.
