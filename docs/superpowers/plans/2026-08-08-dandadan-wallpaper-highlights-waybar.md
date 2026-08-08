# DANDADAN Theme Wallpaper Highlights & Waybar Customization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete per-wallpaper highlight system for all 39 wallpapers (`01.webp` through `39.webp`), a floating capsule/pill Waybar configuration, updated app configs across the desktop environment, and a wallpaper switcher helper script for the DANDADAN Omarchy theme.

**Architecture:** A unified JSON manifest (`wallpaper_highlights.json`) and generated CSS stylesheet (`wallpapers.css`) provide color tokens for every wallpaper. Waybar imports these CSS variables to dynamically style floating capsule modules (`waybar_config.jsonc`, `waybar.css`). A bash helper script (`wallpaper_switch.sh`) manages background switching and live CSS reloads.

**Tech Stack:** JSON, CSS, TOML, GTK/Waybar CSS, Hyprland Config, Bash Shell.

## Global Constraints
- Target directory: `/home/mister/.config/omarchy/themes/DANDADAN`
- Symlink target: `/home/mister/.config/omarchy/current/background`
- Wallpaper count: 39 wallpapers (`01.webp` to `39.webp`)
- All JSON files must pass `python3 -m json.tool` validation.
- All shell scripts must be executable (`chmod +x`).

---

### Task 1: Per-Wallpaper Highlight Manifest & CSS Color System

**Files:**
- Create: `/home/mister/.config/omarchy/themes/DANDADAN/wallpaper_highlights.json`
- Create: `/home/mister/.config/omarchy/themes/DANDADAN/wallpapers.css`

**Interfaces:**
- Produces: `wallpaper_highlights.json` mapping `"01"` .. `"39"` to hex color fields (`accent`, `highlight`, `background`, `foreground`, `border`, `glow`, `vibe`).
- Produces: `wallpapers.css` defining `.wallpaper-01` .. `.wallpaper-39` CSS property blocks with `--wp-accent`, `--wp-highlight`, `--wp-bg`, `--wp-fg`, `--wp-border`, `--wp-glow`.

- [ ] **Step 1: Write `wallpaper_highlights.json`**

Write a JSON manifest defining color palettes for all 39 wallpapers (`01` through `39`).

- [ ] **Step 2: Validate JSON syntax**

Run: `python3 -m json.tool /home/mister/.config/omarchy/themes/DANDADAN/wallpaper_highlights.json > /dev/null`  
Expected: Exit code 0 (valid JSON).

- [ ] **Step 3: Create `wallpapers.css`**

Write `wallpapers.css` containing CSS rules `.wallpaper-01` to `.wallpaper-39` with corresponding CSS custom variables derived from the highlight manifest.

- [ ] **Step 4: Verify CSS syntax**

Run: `grep -E "^\.wallpaper-[0-9]{2}" /home/mister/.config/omarchy/themes/DANDADAN/wallpapers.css | wc -l`  
Expected: `39` matching selectors.

---

### Task 2: Floating Pill Waybar Configuration & Styling

**Files:**
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/waybar.css`
- Create: `/home/mister/.config/omarchy/themes/DANDADAN/waybar_config.jsonc`

**Interfaces:**
- Consumes: `wallpapers.css` via `@import 'wallpapers.css';`
- Produces: Waybar JSONC configuration (`waybar_config.jsonc`) with left, center, right pill modules and Waybar CSS styling (`waybar.css`).

- [ ] **Step 1: Write `waybar_config.jsonc`**

Create `waybar_config.jsonc` with modules:
- Left: `custom/omarchy`, `hyprland/workspaces`
- Center: `clock#horizontal`, `clock#vertical`, `custom/weather`, `custom/update`, `custom/screenrecording-indicator`, `custom/idle-indicator`
- Right: `group/tray-expander`, `bluetooth`, `network`, `pulseaudio`, `cpu`, `battery`

- [ ] **Step 2: Validate `waybar_config.jsonc` syntax**

Run: `python3 -c "import json, re; content = open('/home/mister/.config/omarchy/themes/DANDADAN/waybar_config.jsonc').read(); json.loads(re.sub(r'//.*', '', content))"`  
Expected: Clean load without JSON errors.

- [ ] **Step 3: Update `waybar.css`**

Import `wallpapers.css`, set default class `.wallpaper-01`, and style floating capsule modules (`border-radius: 12px; margin: 4px 6px; padding: 2px 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); background: var(--wp-bg); color: var(--wp-fg); border: 1px solid var(--wp-border);`).

- [ ] **Step 4: Verify `waybar.css`**

Run: `head -n 10 /home/mister/.config/omarchy/themes/DANDADAN/waybar.css`  
Expected: `@import 'wallpapers.css';` present at top of file.

---

### Task 3: Desktop Application Palette & Config Updates

**Files:**
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/colors.toml`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/omarchist.json`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/hyprland.conf`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/hyprlock.conf`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/kitty.conf`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/ghostty.conf`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/alacritty.toml`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/mako.ini`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/walker.css`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/swayosd.css`
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/btop.theme`

- [ ] **Step 1: Update core color files (`colors.toml` and `omarchist.json`)**

Ensure `colors.toml` and `omarchist.json` contain the complete Dandadan color definitions (accent `#D8B3FE`, cursor `#E1477A`, foreground `#2C393B`, background `#EEEDEE`, color0-15).

- [ ] **Step 2: Update `hyprland.conf` & `hyprlock.conf`**

Set `col.active_border = rgb(E1477A) rgb(D8B3FE) 45deg` in `hyprland.conf`. Set input field accent and ring colors in `hyprlock.conf`.

- [ ] **Step 3: Update terminal configs (`kitty.conf`, `alacritty.toml`, `ghostty.conf`)**

Ensure matching cursor, selection, foreground, background, and 16 ANSI colors across all three terminal config files.

- [ ] **Step 4: Update UI elements (`mako.ini`, `walker.css`, `swayosd.css`, `btop.theme`)**

Apply capsule rounded borders (`border-radius = 12`) to `mako.ini`, floating modal styling to `walker.css`, OSD pill styling to `swayosd.css`, and thermal/memory color gradients to `btop.theme`.

---

### Task 4: Wallpaper Switcher Helper Script (`wallpaper_switch.sh`)

**Files:**
- Create: `/home/mister/.config/omarchy/themes/DANDADAN/wallpaper_switch.sh`

- [ ] **Step 1: Write `wallpaper_switch.sh`**

Create bash script accepting wallpaper index `01`..`39` or `random`:
- Validates input.
- Updates symlink `/home/mister/.config/omarchy/current/background`.
- Updates `waybar.css` active `.wallpaper-XX` selector or class.
- Signals Waybar (`killall -SIGUSR2 waybar` or `pkill -SIGUSR2 waybar`) to refresh.

- [ ] **Step 2: Make executable**

Run: `chmod +x /home/mister/.config/omarchy/themes/DANDADAN/wallpaper_switch.sh`

- [ ] **Step 3: Test execution**

Run: `/home/mister/.config/omarchy/themes/DANDADAN/wallpaper_switch.sh 01`  
Expected: Output confirming wallpaper `01.webp` set and Waybar reloaded.

---

### Task 5: End-to-End Verification

- [ ] **Step 1: Validate all JSON files**

Run:
```bash
python3 -m json.tool /home/mister/.config/omarchy/themes/DANDADAN/wallpaper_highlights.json > /dev/null && echo "Highlights JSON OK"
python3 -m json.tool /home/mister/.config/omarchy/themes/DANDADAN/omarchist.json > /dev/null && echo "Omarchist JSON OK"
```

- [ ] **Step 2: Test switcher script across multiple wallpapers**

Run:
```bash
/home/mister/.config/omarchy/themes/DANDADAN/wallpaper_switch.sh 05
/home/mister/.config/omarchy/themes/DANDADAN/wallpaper_switch.sh 12
/home/mister/.config/omarchy/themes/DANDADAN/wallpaper_switch.sh 01
```
Expected: All switch commands complete without errors.
