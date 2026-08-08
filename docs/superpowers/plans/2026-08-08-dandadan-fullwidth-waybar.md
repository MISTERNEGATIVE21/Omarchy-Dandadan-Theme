# DANDADAN Full-Width Waybar & Center Music Controls Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a full-width header Waybar configuration (`waybar_config.jsonc`) with center music controls (`mpris` module) and high-end GTK CSS styling (`waybar.css`) for the DANDADAN Omarchy theme.

**Architecture:** Update `waybar_config.jsonc` with left, center (mpris + clock), and right modules. Update `waybar.css` with full-width container styling, glassmorphism, glowing active workspace indicators, and center music control card styling. Apply theme and verify Waybar process.

**Tech Stack:** Waybar JSONC, GTK CSS, Hyprland, Omarchy CLI.

## Global Constraints
- Target directory: `/home/mister/.config/omarchy/themes/DANDADAN`
- Waybar width: 100% full-width header bar
- GTK `@define-color` definitions for theme colors (`background`, `foreground`, `accent`, `cursor`, `highlight`)
- Valid JSONC configuration in `waybar_config.jsonc` and GTK CSS in `waybar.css`.

---

### Task 1: Full-Width Waybar JSONC Configuration with Center Music Controls

**Files:**
- Create/Modify: `/home/mister/.config/omarchy/themes/DANDADAN/waybar_config.jsonc`

- [ ] **Step 1: Write `waybar_config.jsonc`**

Create `waybar_config.jsonc` with:
- Left: `custom/omarchy`, `hyprland/workspaces`
- Center: `mpris`, `clock#horizontal`, `custom/weather`
- Right: `cpu`, `pulseaudio`, `network`, `bluetooth`, `battery`, `group/tray-expander`
- Module configurations for `mpris` (playerctl controls, artist/title format, max-length 32), `cpu` (`󰍛 {usage}%`), `pulseaudio` (`{icon} {volume}%`), `network` (`󰤨  {essid}`), `battery` (`{icon} {capacity}%`).

- [ ] **Step 2: Validate JSONC syntax**

Run: `python3 -c "import json, re; content = open('/home/mister/.config/omarchy/themes/DANDADAN/waybar_config.jsonc').read(); json.loads(re.sub(r'//.*', '', content))"`  
Expected: Exit code 0 (valid JSONC).

---

### Task 2: Full-Width Waybar GTK CSS Styling & Aesthetics

**Files:**
- Modify: `/home/mister/.config/omarchy/themes/DANDADAN/waybar.css`

- [ ] **Step 1: Write `waybar.css`**

Define `@define-color` variables:
- `background #EEEDEE;`
- `foreground #2C393B;`
- `accent #D8B3FE;`
- `cursor #E1477A;`
- `highlight #E8759B;`

Style elements:
- `window#waybar`: Full-width top bar, `background: rgba(20, 22, 30, 0.90)`, `border-bottom: 2px solid @cursor`.
- `#custom-omarchy`: Neon pink badge (`background: @cursor; color: #FFFFFF; font-size: 16px; border-radius: 8px; margin: 3px 6px; padding: 2px 10px;`).
- `#workspaces button.active`: Glowing magenta pill (`background: @cursor; color: #FFFFFF; font-weight: bold; border-radius: 6px; box-shadow: 0 0 12px @cursor;`).
- `#mpris`: Center music card (`background: rgba(255, 255, 255, 0.08); border: 1px solid @accent; border-radius: 10px; padding: 2px 14px; margin: 3px 8px; color: @foreground; font-weight: bold;`).
- `#clock`, `#cpu`, `#pulseaudio`, `#network`, `#bluetooth`, `#battery`: Glassmorphic pill modules (`background: rgba(238, 237, 238, 0.10); color: #F0F4FC; border: 1px solid rgba(216, 179, 254, 0.3); border-radius: 10px; margin: 3px 4px; padding: 2px 10px;`).

- [ ] **Step 2: Test GTK CSS syntax**

Run: `waybar --help > /dev/null`

---

### Task 3: Apply Theme & Verify Waybar Runtime

**Files:**
- Sync to `/home/mister/.config/omarchy/current/theme/` via `omarchy-theme-set DANDADAN`

- [ ] **Step 1: Execute `omarchy-theme-set DANDADAN`**

Run: `/home/mister/.local/share/omarchy/bin/omarchy-theme-set DANDADAN`

- [ ] **Step 2: Verify Waybar process**

Run: `pgrep -a waybar`  
Expected: Active PID output for `waybar`.

- [ ] **Step 3: Commit to Git**

Run: `git add . && git commit -m "feat: full-width waybar layout with center music controls"`
