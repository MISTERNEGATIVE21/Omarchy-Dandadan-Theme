# Omarchy 4.0 Quickshell UI Redesign & Shell Detection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement full Omarchy 4.0 Quickshell support for Dandadan theme (custom `shell.toml`, `shell.lock.toml`, `shell.json`, `hyprland.lua`), shell auto-detection (Quickshell priority with Waybar fallback), dynamic wallpaper recoloring engine updates with live Quickshell IPC, and updated installer/hooks.

**Architecture:** A smart dual-shell architecture prioritizing Quickshell on Omarchy 4.0+ systems while maintaining fallback compatibility for Waybar. The dynamic Python recoloring engine inspects the active wallpaper, extracts accent/highlight pairs, renders all UI configs (Quickshell, Hyprland Lua, Waybar, 21 app targets), and triggers live Quickshell IPC or Waybar signals.

**Tech Stack:** Bash, Python 3 (Pillow, colorsys), Quickshell QML / TOML theme engine, Hyprland Lua configuration API, Waybar CSS.

## Global Constraints
- Target Git Branch: `feat/omarchy-4-quickshell`
- Primary shell priority: Quickshell (`omarchy-shell` / `quickshell`)
- Fallback shell: Waybar (`waybar`)
- State paths: Support `$HOME/.local/state/omarchy/current/` (Omarchy 4.0+) with fallback to `$HOME/.config/omarchy/current/` (Omarchy 3.x)
- Preserve all 52 Dandadan wallpaper accent pairings in `wallpaper_highlights.json`

---

### Task 1: Shell Auto-Detection Engine (`scripts/detect_shell.sh`)

**Files:**
- Create: `scripts/detect_shell.sh`
- Create: `tests/test_detect_shell.sh`

**Interfaces:**
- Consumes: Environment, process table (`pgrep`), filesystem (`/usr/share/omarchy/`, `~/.local/state/omarchy/`).
- Produces: `scripts/detect_shell.sh` returning exit 0 and stdout: `quickshell`, `waybar`, `dual`, or `none`.

- [ ] **Step 1: Write the failing test for shell detection**

```bash
mkdir -p tests scripts
cat > tests/test_detect_shell.sh << 'EOF'
#!/bin/bash
set -e

# Test 1: Script exists and is executable
if [[ ! -x "scripts/detect_shell.sh" ]]; then
  echo "FAIL: scripts/detect_shell.sh is not executable"
  exit 1
fi

# Test 2: Execution produces valid output token
OUTPUT=$(./scripts/detect_shell.sh)
if [[ "$OUTPUT" != "quickshell" && "$OUTPUT" != "waybar" && "$OUTPUT" != "dual" && "$OUTPUT" != "none" ]]; then
  echo "FAIL: Unexpected output '$OUTPUT'"
  exit 1
fi

echo "PASS: test_detect_shell.sh passed (Detected: $OUTPUT)"
EOF
chmod +x tests/test_detect_shell.sh
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/test_detect_shell.sh`  
Expected: FAIL with "scripts/detect_shell.sh is not executable" or file missing.

- [ ] **Step 3: Implement `scripts/detect_shell.sh`**

```bash
cat > scripts/detect_shell.sh << 'EOF'
#!/bin/bash
# Dandadan Theme — Shell Detection Engine
# Detects whether the current environment uses Quickshell (Omarchy 4.0+), Waybar, or both.
# Priority: Quickshell > Waybar

has_quickshell=0
has_waybar=0

# Check running processes
if pgrep -x quickshell >/dev/null 2>&1 || pgrep -f "quickshell.*omarchy" >/dev/null 2>&1 || pgrep -f "omarchy-shell" >/dev/null 2>&1; then
  has_quickshell=1
fi

if pgrep -x waybar >/dev/null 2>&1; then
  has_waybar=1
fi

# If neither is actively running, check system installation & Omarchy version
if (( !has_quickshell && !has_waybar )); then
  if command -v omarchy-shell >/dev/null 2>&1 || [[ -d "/usr/share/omarchy/shell" ]] || [[ -f "/usr/share/omarchy/version" && $(cat /usr/share/omarchy/version 2>/dev/null) =~ ^4\. ]]; then
    has_quickshell=1
  fi
  if command -v waybar >/dev/null 2>&1; then
    has_waybar=1
  fi
fi

if (( has_quickshell && has_waybar )); then
  # If Quickshell is running, report quickshell as primary
  if pgrep -x quickshell >/dev/null 2>&1 || pgrep -f "omarchy-shell" >/dev/null 2>&1; then
    echo "quickshell"
  elif pgrep -x waybar >/dev/null 2>&1; then
    echo "waybar"
  else
    echo "quickshell"
  fi
elif (( has_quickshell )); then
  echo "quickshell"
elif (( has_waybar )); then
  echo "waybar"
else
  echo "none"
fi
EOF
chmod +x scripts/detect_shell.sh
```

- [ ] **Step 4: Run test to verify it passes**

Run: `bash tests/test_detect_shell.sh`  
Expected: PASS with "Detected: quickshell".

- [ ] **Step 5: Commit**

```bash
git add scripts/detect_shell.sh tests/test_detect_shell.sh
git commit -m "feat(shell): implement shell auto-detection helper script"
```

---

### Task 2: Quickshell GUI Dotfiles (`shell.toml`, `shell.lock.toml`, `shell.json`, `hyprland.lua`)

**Files:**
- Create: `shell.toml`
- Create: `shell.lock.toml`
- Create: `shell.json`
- Modify: `hyprland.lua`
- Create: `tests/test_gui_dotfiles.py`

**Interfaces:**
- Consumes: Omarchy 4.0 theming tokens from `colors.toml` (`accent`, `cursor`, `foreground`, `background`, `color0`..`color15`).
- Produces: Valid Quickshell theme definition, lock screen override, shell layout preset, and Hyprland Lua border/shadow configuration.

- [ ] **Step 1: Write validation test for GUI dotfiles**

```python
cat > tests/test_gui_dotfiles.py << 'EOF'
import os, json, tomli or tomllib

try:
    import tomllib
except ImportError:
    import tomli as tomllib

def test_dotfiles_exist_and_valid():
    assert os.path.exists("shell.toml"), "shell.toml missing"
    assert os.path.exists("shell.lock.toml"), "shell.lock.toml missing"
    assert os.path.exists("shell.json"), "shell.json missing"
    assert os.path.exists("hyprland.lua"), "hyprland.lua missing"

    with open("shell.json") as f:
        shell_json = json.load(f)
    assert "bar" in shell_json
    assert "layout" in shell_json["bar"]
    assert "left" in shell_json["bar"]["layout"]
    assert "center" in shell_json["bar"]["layout"]
    assert "right" in shell_json["bar"]["layout"]

    with open("shell.toml", "rb") as f:
        shell_toml = tomllib.load(f)
    assert "bar" in shell_toml
    assert "controls" in shell_toml
    assert "notifications" in shell_toml

    with open("hyprland.lua") as f:
        lua_content = f.read()
    assert "hl.config" in lua_content
    assert "active_border" in lua_content
    assert "shadow" in lua_content

    print("PASS: GUI dotfiles valid")

if __name__ == "__main__":
    test_dotfiles_exist_and_valid()
EOF
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 tests/test_gui_dotfiles.py`  
Expected: FAIL (missing `shell.toml` / `shell.lock.toml` / `shell.json`).

- [ ] **Step 3: Create `shell.toml`, `shell.lock.toml`, `shell.json`, and update `hyprland.lua`**

Create `shell.toml`:
```toml
# DANDADAN Omarchy 4.0 Quickshell Surface Styling
# Supernatural anime aesthetic: dark translucent glass, vivid cursed neon glow

[bar]
background       = "#14161E"
background-alpha = 0.85
text             = "#F0F4FC"
active           = "#08F503"
scale-with-font  = true
size-horizontal  = 30
size-vertical    = 32

[hyprland]
active-border            = "#08F503 #EA0B08 45deg"
active-border-foreground = "#08F503"

[controls]
normal-color        = "#F0F4FC"
normal-fill-alpha   = 0.05
normal-border       = "#08F503"
normal-border-width = 1
normal-border-alpha = 0.25

hover-cursor-color        = "#FFFFFF"
hover-cursor-fill-alpha   = 0.12
hover-cursor-border       = "#08F503"
hover-cursor-border-width = 1
hover-cursor-border-alpha = 0.50

focus-color        = "#FFFFFF"
focus-fill-alpha   = 0.12
focus-border       = "#08F503"
focus-border-width = 1
focus-border-alpha = 0.50

selected-color        = "#FFFFFF"
selected-fill-alpha   = 0.22
selected-border       = "#08F503"
selected-border-width = 1
selected-border-alpha = 0.80

pressed-fill-alpha   = 0.28
selection-fill-alpha = 0.35

[spacing]
scale           = 1.0
scale-with-font = true

[font]
base-size = 12

[popups]
background       = "#14161E"
background-alpha = 0.94
text             = "#F0F4FC"
border           = "#08F503"
border-alpha     = 0.80
border-width     = 1

[tooltip]
background       = "#14161E"
background-alpha = 0.96
text             = "#F0F4FC"
border           = "#08F503"
border-alpha     = 0.70

[notifications]
background       = "#14161E"
background-alpha = 0.95
text             = "#F0F4FC"
border           = "#08F503"
border-alpha     = 0.85
border-width     = 1
countdown        = "#08F503"

[launcher]
background                = "#14161E"
background-alpha          = 0.94
text                      = "#F0F4FC"
border                    = "#08F503"
border-alpha              = 0.75
scrim                     = "#14161E"
scrim-alpha               = 0.55
selected-background       = "#08F503"
selected-background-alpha = 0.15
selected-text             = "#08F503"
selected-border           = "#08F503"
selected-border-alpha     = 0.50

[menu]
background                = "#14161E"
background-alpha          = 0.95
text                      = "#F0F4FC"
border                    = "#08F503"
border-alpha              = 0.75
scrim                     = "#14161E"
scrim-alpha               = 0.55
selected-background       = "#08F503"
selected-background-alpha = 0.15
selected-text             = "#08F503"
selected-border           = "#08F503"
selected-border-alpha     = 0.50

[polkit]
background       = "#14161E"
background-alpha = 0.96
text             = "#F0F4FC"
text-error       = "#EA0B08"
border           = "#08F503"
border-error     = "#EA0B08"
border-alpha     = 0.90
scrim            = "#14161E"
scrim-alpha      = 0.60
accent           = "#08F503"

[lock]
background       = "#14161E"
background-alpha = 0.85
text             = "#F0F4FC"
placeholder      = "#616367"
text-error       = "#EA0B08"
border           = "#08F503"
border-active    = "#08F503"
border-error     = "#EA0B08"
border-alpha     = 0.90
selection        = "#08F503"
selection-alpha  = 0.45

[image-picker]
scrim                   = "#14161E"
scrim-alpha             = 0.55
text                    = "#F0F4FC"
selected-border         = "#08F503"
selected-border-alpha   = 1.0
unselected-border       = "#F0F4FC"
unselected-border-alpha = 0.25
```

Create `shell.lock.toml`:
```toml
text             = "#F0F4FC"
placeholder      = "#616367"
text-error       = "#EA0B08"
border           = "#08F503"
border-active    = "#08F503"
border-error     = "#EA0B08"
```

Create `shell.json`:
```json
{
  "bar": {
    "centerAnchor": "omarchy.clock",
    "layout": {
      "center": [
        {
          "id": "omarchy.indicators"
        },
        {
          "format": "dddd HH:mm",
          "formatAlt": "d MMMM 'W'ww yyyy",
          "id": "omarchy.clock",
          "verticalFormat": "HH\n—\nmm"
        },
        {
          "id": "omarchy.keyboard-layout"
        },
        {
          "id": "omarchy.weather"
        },
        {
          "id": "omarchy.system-update"
        }
      ],
      "left": [
        {
          "id": "omarchy.menu"
        },
        {
          "id": "omarchy.workspaces"
        }
      ],
      "right": [
        {
          "id": "omarchy.tray"
        },
        {
          "id": "omarchy.tailscale"
        },
        {
          "id": "omarchy.agents"
        },
        {
          "id": "omarchy.bluetooth"
        },
        {
          "id": "omarchy.network"
        },
        {
          "id": "omarchy.audio"
        },
        {
          "id": "omarchy.monitor"
        },
        {
          "id": "omarchy.power"
        }
      ]
    },
    "position": "top",
    "transparent": false
  },
  "idle": {
    "lock": 300,
    "screensaver": 150
  },
  "plugins": [],
  "version": 1
}
```

Update `hyprland.lua`:
```lua
local active_border_color = "rgb(08F503) rgb(EA0B08) 45deg"
local inactive_border_color = "rgba(61636780)"
local active_shadow_color = "rgba(08F50366)"
local inactive_shadow_color = "rgba(00000044)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },
  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },
  decoration = {
    shadow = {
      enabled = true,
      range = 10,
      render_power = 4,
      color = active_shadow_color,
      color_inactive = inactive_shadow_color,
    },
  },
})
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_gui_dotfiles.py`  
Expected: PASS: GUI dotfiles valid.

- [ ] **Step 5: Commit**

```bash
git add shell.toml shell.lock.toml shell.json hyprland.lua tests/test_gui_dotfiles.py
git commit -m "feat(quickshell): add Dandadan shell.toml, shell.lock.toml, shell.json, and hyprland.lua"
```

---

### Task 3: Dynamic Color Engine Overhaul (`update_wallpaper_colors.py`)

**Files:**
- Modify: `update_wallpaper_colors.py`
- Create: `tests/test_dynamic_engine.py`

**Interfaces:**
- Consumes: `wallpaper_highlights.json`, active background symlink (`~/.local/state/omarchy/current/background` or `~/.config/omarchy/current/background`).
- Produces: Dynamically rendered `shell.toml`, `shell.lock.toml`, `colors.toml`, `hyprland.lua`, `hyprland.conf`, `hyprlock.conf`, `waybar.css`, 21 app targets, and triggers `omarchy-shell` IPC or Waybar signals.

- [ ] **Step 1: Write integration test for dynamic color generation**

```python
cat > tests/test_dynamic_engine.py << 'EOF'
import subprocess, os, json

def test_engine_execution():
    result = subprocess.run(["python3", "update_wallpaper_colors.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Engine failed: {result.stderr}"

    # Verify generated files exist and contain updated tokens
    for fname in ["shell.toml", "shell.lock.toml", "colors.toml", "hyprland.lua", "waybar.css"]:
        assert os.path.exists(fname), f"{fname} was not created"
        with open(fname) as f:
            content = f.read()
            assert len(content) > 0, f"{fname} is empty"

    print("PASS: Dynamic color engine executed successfully and generated all targets")

if __name__ == "__main__":
    test_engine_execution()
EOF
```

- [ ] **Step 2: Run test to verify it fails/passes with old code**

Run: `python3 tests/test_dynamic_engine.py`

- [ ] **Step 3: Update `update_wallpaper_colors.py`**
  - Add path resolution for both `$HOME/.local/state/omarchy/current` (Omarchy 4.0) and `$HOME/.config/omarchy/current` (legacy).
  - Add dynamic `shell.toml` generation with per-wallpaper accent, complement, highlight, cursor, and glow.
  - Add dynamic `shell.lock.toml` generation.
  - Add dynamic `hyprland.lua` generation with multi-stop gradient border and shadow color.
  - Add live Quickshell IPC dispatch (`omarchy-shell -q shell applyTheme "$colors_b64" "$shell_b64"`).
  - Add live Waybar signal dispatch (`pkill -SIGUSR2 waybar` if waybar is running).

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 tests/test_dynamic_engine.py`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add update_wallpaper_colors.py tests/test_dynamic_engine.py
git commit -m "feat(engine): add Quickshell dynamic generation, Omarchy 4.0 paths, and live IPC"
```

---

### Task 4: Omarchy Hooks & Installer Overhaul (`hooks/theme-set`, `hooks/bg-set`, `install.sh`)

**Files:**
- Modify: `install.sh`
- Create: `tests/test_installer_hooks.sh`

**Interfaces:**
- Consumes: `scripts/detect_shell.sh`, `shell.json`, `waybar_config.jsonc`, `update_wallpaper_colors.py`.
- Produces: Installed hooks in `~/.config/omarchy/hooks/` and seamless theme setup.

- [ ] **Step 1: Write test for installer syntax and hook generation**

```bash
cat > tests/test_installer_hooks.sh << 'EOF'
#!/bin/bash
set -e

# Test 1: Bash syntax check
bash -n install.sh
echo "PASS: install.sh syntax valid"

# Test 2: Verify installer includes quickshell detection and path handling
grep -q "detect_shell.sh" install.sh || grep -q "quickshell" install.sh
grep -q "shell.json" install.sh

echo "PASS: install.sh includes Quickshell and shell detection integration"
EOF
chmod +x tests/test_installer_hooks.sh
```

- [ ] **Step 2: Run test to verify it fails**

Run: `bash tests/test_installer_hooks.sh`

- [ ] **Step 3: Update `install.sh`**
  - Add Quickshell check alongside Waybar check.
  - Update `theme-set` hook to check active shell:
    - If Quickshell: Backup `~/.config/omarchy/shell.json` to `~/.config/omarchy/shell.json.omarchy-default` (if not already backed up), copy Dandadan `shell.json` to `~/.config/omarchy/shell.json`, and trigger Quickshell reload.
    - If Waybar: Backup `~/.config/waybar/config.jsonc`, deploy `waybar_config.jsonc`, and trigger `omarchy-restart-waybar`.
    - Run `update_wallpaper_colors.py` against detected theme state path (`~/.local/state/omarchy/current/theme` or `~/.config/omarchy/current/theme`).
  - Update `bg-set` hook to call `update_wallpaper_colors.py` on wallpaper change.
  - Update theme activation and documentation banner.

- [ ] **Step 4: Run test to verify it passes**

Run: `bash tests/test_installer_hooks.sh`  
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add install.sh tests/test_installer_hooks.sh
git commit -m "feat(installer): update installer and hooks for Omarchy 4.0 Quickshell support and auto-detection"
```

---

### Task 5: End-to-End Verification & Validation

**Files:**
- Modify: `README.md`
- Test: Full wallpaper cycle & shell update test

- [ ] **Step 1: Test `update_wallpaper_colors.py` across multiple wallpapers**
  - Verify wallpaper 01, wallpaper 32, wallpaper 41 correctly generate all dotfiles.

- [ ] **Step 2: Test `scripts/detect_shell.sh` and hook triggers**

- [ ] **Step 3: Update `README.md` with Omarchy 4.0 Quickshell features and compatibility notes**

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README with Omarchy 4.0 Quickshell documentation and shell detection"
```
