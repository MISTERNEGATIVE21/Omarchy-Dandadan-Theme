#!/usr/bin/env python3
"""
DANDADAN OMARCHY THEME — Universal Dynamic Color Engine
═══════════════════════════════════════════════════════
Updates ALL 21+ config targets on wallpaper change with zero inverted colors.
Strict semantic ANSI color mapping (Red=Red, Green=Green, etc.).
Full Omarchy 4.0 distro & Quickshell implementation.

Targets: Neovim · GTK · Zed · VS Code / Antigravity IDE · Alacritty · Btop · Chromium
         Foot · Ghostty · Hyprland Lua · Hyprlock · Icons · Kitty · Mako
         SwayOSD · Vencord · Walker · Warp · Waybar · Wofi · Zellij · Quickshell
"""

import json, os, sys, subprocess, colorsys, math, base64

# ─── Paths ─────────────────────────────────────────────────────────────────────
HOME      = os.path.expanduser("~")
THEME_DIR = f"{HOME}/.config/omarchy/themes/dandadan-theme"

# Omarchy 4.0 state directories with legacy fallback
STATE_CURR_DIRS = [
    f"{HOME}/.local/state/omarchy/current/theme",
    f"{HOME}/.config/omarchy/current/theme"
]

manifest_path   = f"{THEME_DIR}/wallpaper_highlights.json"
current_bg_link = None
for bg_path in [
    f"{HOME}/.local/state/omarchy/current/background",
    f"{HOME}/.config/omarchy/current/background"
]:
    if os.path.islink(bg_path) or os.path.exists(bg_path):
        current_bg_link = bg_path
        break

if current_bg_link is None:
    current_bg_link = f"{HOME}/.local/state/omarchy/current/background"

if not os.path.exists(manifest_path):
    sys.exit(0)

with open(manifest_path) as f:
    data = json.load(f)

# ─── Detect active wallpaper ────────────────────────────────────────────────────
active_idx = "01"
active_bg_path = None
if os.path.islink(current_bg_link) or os.path.exists(current_bg_link):
    try:
        target = os.readlink(current_bg_link) if os.path.islink(current_bg_link) else current_bg_link
        active_bg_path = target
        base   = os.path.basename(target)
        # handles "001.png", "01.webp", "32.webp", "1-name.jpg" etc.
        num    = base.split(".")[0].split("-")[0].lstrip("0") or "0"
        idx    = num.zfill(2)
        if idx in data:
            active_idx = idx
        elif num in data:
            active_idx = num
    except Exception:
        pass

colors    = data.get(active_idx, data.get("01", {}))
accent    = colors.get("accent",     "#E80202")
cursor    = colors.get("border",     colors.get("glow", accent))
highlight = colors.get("highlight",  "#E3847B")
bg        = colors.get("background", "#14161E")
fg        = colors.get("foreground", "#F0F4FC")
vibe      = colors.get("vibe",       f"Dandadan Scene {active_idx}")

# ─── Color math helpers ─────────────────────────────────────────────────────────
def h2r(hex_code: str):
    h = hex_code.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def r2h(r, g, b) -> str:
    return f"#{int(max(0, min(255, r))):02X}{int(max(0, min(255, g))):02X}{int(max(0, min(255, b))):02X}"

def hex_to_rgb_str(hex_code: str) -> str:
    r, g, b = h2r(hex_code)
    return f"{r},{g},{b}"

def complementary(hex_code: str) -> str:
    """Return 180° hue-rotated complement."""
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h2 = (h + 0.5) % 1.0
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
    return r2h(r2*255, g2*255, b2*255)

def darken(hex_code: str, factor: float = 0.65) -> str:
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v * factor)
    return r2h(r2*255, g2*255, b2*255)

def lighten(hex_code: str, factor: float = 1.3, max_v: float = 0.98) -> str:
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, max(s*0.75, 0.15), min(v * factor, max_v))
    return r2h(r2*255, g2*255, b2*255)

def with_alpha(hex_code: str, alpha_hex: str = "AA") -> str:
    return hex_code.rstrip("#") + alpha_hex if not hex_code.startswith("#") else hex_code + alpha_hex

def get_fg_for_bg(hex_color: str, dark: str = "#14161E", light: str = "#FFFFFF") -> str:
    """Return high-contrast foreground color based on relative luminance."""
    r, g, b = h2r(hex_color)
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    return dark if lum > 0.50 else light

# ─── Strict Semantic Palette Generator (NO INVERTED CHANNELS) ──────────────────
def build_semantic_palette(accent_hex: str, highlight_hex: str):
    """
    Constructs a true 16-color ANSI and full semantic palette.
    Guarantees:
      - Red is RED (Hue 345°-15°)
      - Green is GREEN (Hue 80°-155°)
      - Yellow is YELLOW (Hue 40°-75°)
      - Blue is BLUE (Hue 205°-255°)
      - Magenta is MAGENTA (Hue 275°-345°)
      - Cyan is CYAN (Hue 160°-200°)
      - Orange is ORANGE (Hue 15°-40°)
    Dynamically tunes the exact hue bucket of the wallpaper's accent/highlight
    while keeping all other ANSI channels vibrant and true to their roles.
    """
    sem = {
        "red":            "#FF5555",
        "bright_red":     "#FF6E6E",
        "orange":         "#FF9E64",
        "yellow":         "#F1FA8C",
        "bright_yellow":  "#FFFFA5",
        "green":          "#50FA7B",
        "bright_green":   "#69FF94",
        "cyan":           "#00F5D4",
        "bright_cyan":    "#56D4E8",
        "blue":           "#7AA2F7",
        "bright_blue":    "#9AB8FF",
        "magenta":        "#EF02F5",
        "bright_magenta": "#FF92DF",
        "brown":          "#75493D",
    }

    # Dynamically inject vibrant wallpaper colors into matching hue buckets
    for col in [accent_hex, highlight_hex]:
        r, g, b = h2r(col)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        if s > 0.20 and v > 0.25:
            if h < 0.05 or h >= 0.95:  # Red
                sem["red"] = col
                sem["bright_red"] = lighten(col, 1.2)
            elif 0.05 <= h < 0.12:    # Orange
                sem["orange"] = col
            elif 0.12 <= h < 0.21:    # Yellow / Gold
                sem["yellow"] = col
                sem["bright_yellow"] = lighten(col, 1.2)
            elif 0.21 <= h < 0.43:    # Green
                sem["green"] = col
                sem["bright_green"] = lighten(col, 1.2)
            elif 0.43 <= h < 0.55:    # Cyan / Teal
                sem["cyan"] = col
                sem["bright_cyan"] = lighten(col, 1.2)
            elif 0.55 <= h < 0.70:    # Blue
                sem["blue"] = col
                sem["bright_blue"] = lighten(col, 1.2)
            elif 0.70 <= h < 0.95:    # Magenta / Violet / Purple
                sem["magenta"] = col
                sem["bright_magenta"] = lighten(col, 1.2)

    return sem

sem = build_semantic_palette(accent, highlight)
accent_comp = complementary(accent)
border_c2 = accent_comp.lstrip('#') if accent_comp != accent else cursor.lstrip('#')
border_c2_hex = f"#{border_c2}"

# Dark backgrounds and crisp text
dark_bg      = "#0E1017"
darker_bg    = "#090A0F"
lighter_bg   = "#1D202B"
bg_mid       = "#1A1D2A"
bg_mid2      = "#212536"
selection_bg = "#384166"   # Enhanced visible indigo-slate highlight (>10:1 contrast with white text)
selection_fg = "#FFFFFF"

ansi_black   = "#26293B"   # Distinct dark slate black (never identical to bg, so black badges/text are visible!)
dark_fg      = "#6A738C"
light_fg     = "#C5CDE3"
bright_fg    = "#FFFFFF"
muted        = "#7E859E"   # Enhanced muted/bright black (>4.5:1 WCAG AA contrast for comments/line numbers)

def get_best_icon_theme(hex_code: str) -> str:
    """Map hue to verified existing installed icon themes (Yaru-*-dark / Yaru-*)."""
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    if 0.95 <= h or h < 0.05:
        candidates = ["Yaru-red-dark", "Yaru-red", "Yaru-dark"]
    elif 0.05 <= h < 0.12:
        candidates = ["Yaru-wartybrown-dark", "Yaru-dark", "Yaru-wartybrown", "Yaru"]
    elif 0.12 <= h < 0.20:
        candidates = ["Yaru-yellow-dark", "Yaru-yellow", "Yaru-dark"]
    elif 0.20 <= h < 0.40:
        candidates = ["Yaru-prussiangreen-dark", "Yaru-sage-dark", "Yaru-olive-dark", "Yaru-prussiangreen"]
    elif 0.40 <= h < 0.55:
        candidates = ["Yaru-prussiangreen-dark", "Yaru-blue-dark", "Yaru-blue"]
    elif 0.55 <= h < 0.68:
        candidates = ["Yaru-blue-dark", "Yaru-blue"]
    elif 0.68 <= h < 0.78:
        candidates = ["Yaru-purple-dark", "Yaru-purple"]
    elif 0.78 <= h < 0.95:
        candidates = ["Yaru-magenta-dark", "Yaru-magenta"]
    else:
        candidates = ["Yaru-red-dark", "Yaru-red", "Yaru-dark"]

    for c in candidates:
        for prefix in ["/usr/share/icons", f"{HOME}/.local/share/icons", f"{HOME}/.icons"]:
            if os.path.exists(f"{prefix}/{c}"):
                return c
    return candidates[0]

icon_theme_name = get_best_icon_theme(accent)

print(f"[dandadan] Wallpaper {active_idx} — {vibe}")
print(f"  accent={accent}  highlight={highlight}  comp={accent_comp}")
print(f"  red={sem['red']}  green={sem['green']}  yellow={sem['yellow']}  blue={sem['blue']}")

def write(path: str, content: str):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
    except Exception:
        pass

def write_both(filename: str, content: str):
    """Write to both theme dir and all active current/theme dirs."""
    write(f"{THEME_DIR}/{filename}", content)
    for curr in STATE_CURR_DIRS:
        write(f"{curr}/{filename}", content)

# ══════════════════════════════════════════════════════════════════════════════
# 1 · COLORS.TOML (Omarchy 4.0 Standard Semantic Specification)
# ══════════════════════════════════════════════════════════════════════════════
colors_toml = f"""# DANDADAN Colors — Wallpaper {active_idx}: {vibe}
mode = "dark"

accent = "{accent}"
selection = "{selection_bg}"
muted = "{muted}"

background = "{bg}"
dark_background = "{dark_bg}"
darker_background = "{darker_bg}"
lighter_background = "{lighter_bg}"

foreground = "{fg}"
dark_foreground = "{dark_fg}"
light_foreground = "{light_fg}"
bright_foreground = "{bright_fg}"

hyprland_active_border = "{accent} {border_c2_hex} 45deg"
hyprland_inactive_border = "{muted}"

red = "{sem['red']}"
yellow = "{sem['yellow']}"
orange = "{sem['orange']}"
green = "{sem['green']}"
cyan = "{sem['cyan']}"
blue = "{sem['blue']}"
magenta = "{sem['magenta']}"
brown = "{sem['brown']}"

bright_red = "{sem['bright_red']}"
bright_yellow = "{sem['bright_yellow']}"
bright_green = "{sem['bright_green']}"
bright_cyan = "{sem['bright_cyan']}"
bright_blue = "{sem['bright_blue']}"
bright_magenta = "{sem['bright_magenta']}"
"""
write_both("colors.toml", colors_toml)

# ══════════════════════════════════════════════════════════════════════════════
# 2 · QUICKSHELL shell.toml & shell.lock.toml
# ══════════════════════════════════════════════════════════════════════════════
shell_toml = f"""# DANDADAN Omarchy 4.0 Quickshell Surface Styling — Wallpaper {active_idx}: {vibe}

[bar]
background       = "{bg}"
background-alpha = 0.95
text             = "{fg}"
active           = "{accent}"
scale-with-font  = true
size-horizontal  = 30
size-vertical    = 32

[hyprland]
active-border            = "{accent} {border_c2_hex} 45deg"
active-border-foreground = "{fg}"

[controls]
normal-color        = "{fg}"
normal-fill-alpha   = 0.06
normal-border       = "{fg}"
normal-border-width = 1
normal-border-alpha = 0.35

hover-cursor-color        = "{bright_fg}"
hover-cursor-fill-alpha   = 0.15
hover-cursor-border       = "{accent}"
hover-cursor-border-width = 1
hover-cursor-border-alpha = 0.70

focus-color        = "{bright_fg}"
focus-fill-alpha   = 0.15
focus-border       = "{accent}"
focus-border-width = 1
focus-border-alpha = 0.75

selected-color        = "{bright_fg}"
selected-fill-alpha   = 0.25
selected-border       = "{accent}"
selected-border-width = 1
selected-border-alpha = 0.90

pressed-fill-alpha   = 0.30
selection-fill-alpha = 0.40

[spacing]
scale           = 1.0
scale-with-font = true

[font]
base-size = 12

[popups]
background       = "{bg}"
background-alpha = 0.98
text             = "{fg}"
border           = "hyprland.active-border"
border-alpha     = 1.0
border-width     = 1

[tooltip]
background       = "{bg}"
background-alpha = 0.97
text             = "{fg}"
border           = "hyprland.active-border-foreground"
border-alpha     = 1.0

[notifications]
background       = "{bg}"
background-alpha = 0.98
text             = "{fg}"
border           = "hyprland.active-border"
border-alpha     = 1.0
border-width     = 1
countdown        = "{accent}"

[launcher]
background                = "{bg}"
background-alpha          = 0.98
text                      = "{fg}"
border                    = "hyprland.active-border"
border-alpha              = 1.0
scrim                     = "{bg}"
scrim-alpha               = 0.60
selected-background       = "{fg}"
selected-background-alpha = 0.12
selected-text             = "{bright_fg}"
selected-border           = "{accent}"
selected-border-alpha     = 0.70

[menu]
background                = "{bg}"
background-alpha          = 0.98
text                      = "{fg}"
border                    = "hyprland.active-border"
border-alpha              = 1.0
scrim                     = "{bg}"
scrim-alpha               = 0.60
selected-background       = "{fg}"
selected-background-alpha = 0.12
selected-text             = "{bright_fg}"
selected-border           = "{accent}"
selected-border-alpha     = 0.70

[polkit]
background       = "{bg}"
background-alpha = 0.98
text             = "{fg}"
text-error       = "{sem['red']}"
border           = "hyprland.active-border"
border-error     = "{sem['red']}"
border-alpha     = 1.0
scrim            = "{bg}"
scrim-alpha      = 0.60
accent           = "{accent}"

[lock]
background       = "{bg}"
background-alpha = 0.88
text             = "{fg}"
placeholder      = "#8B90A0"
text-error       = "{sem['red']}"
border           = "hyprland.active-border"
border-active    = "hyprland.active-border"
border-error     = "{sem['red']}"
border-alpha     = 1.0
selection        = "{accent}"
selection-alpha  = 0.45

[image-picker]
scrim                   = "{bg}"
scrim-alpha             = 0.60
text                    = "{fg}"
selected-border         = "{accent}"
selected-border-alpha   = 1.0
unselected-border       = "{fg}"
unselected-border-alpha = 0.35
"""
write_both("shell.toml", shell_toml)

shell_lock_toml = f"""text             = "{fg}"
placeholder      = "#8B90A0"
text-error       = "{sem['red']}"
border           = "{accent}"
border-active    = "{accent}"
border-error     = "{sem['red']}"
"""
write_both("shell.lock.toml", shell_lock_toml)

# ══════════════════════════════════════════════════════════════════════════════
# 3 · KITTY Terminal (No Inversion, Dark BG, True ANSI Mapping)
# ══════════════════════════════════════════════════════════════════════════════
kitty = f"""# DANDADAN Kitty — Wallpaper {active_idx}: {vibe}
background {bg}
foreground {fg}

cursor            {accent}
cursor_text_color {get_fg_for_bg(accent)}

selection_background {selection_bg}
selection_foreground {selection_fg}

url_color {sem['cyan']}
url_style curly

active_border_color   {accent}
inactive_border_color {bg_mid}
bell_border_color     {sem['red']}

active_tab_background   {accent}
active_tab_foreground   {get_fg_for_bg(accent)}
inactive_tab_background {bg_mid}
inactive_tab_foreground {muted}
tab_bar_background      {darker_bg}

# Search and mark highlights
mark1_foreground {darker_bg}
mark1_background {accent}
mark2_foreground {darker_bg}
mark2_background {sem['cyan']}
mark3_foreground {darker_bg}
mark3_background {sem['yellow']}

# Normal ANSI Colors
color0  {ansi_black}
color1  {sem['red']}
color2  {sem['green']}
color3  {sem['yellow']}
color4  {sem['blue']}
color5  {sem['magenta']}
color6  {sem['cyan']}
color7  {fg}

# Bright ANSI Colors
color8  {muted}
color9  {sem['bright_red']}
color10 {sem['bright_green']}
color11 {sem['bright_yellow']}
color12 {sem['bright_blue']}
color13 {sem['bright_magenta']}
color14 {sem['bright_cyan']}
color15 {bright_fg}
"""
write_both("kitty.conf", kitty)

# ══════════════════════════════════════════════════════════════════════════════
# 4 · ALACRITTY Terminal
# ══════════════════════════════════════════════════════════════════════════════
alacritty = f"""[colors.primary]
background = "{bg}"
foreground = "{fg}"

[colors.cursor]
cursor = "{accent}"
text   = "{get_fg_for_bg(accent)}"

[colors.vi_mode_cursor]
cursor = "{highlight}"
text   = "{get_fg_for_bg(highlight)}"

[colors.selection]
background = "{selection_bg}"
text       = "{selection_fg}"

[colors.search.matches]
foreground = "{darker_bg}"
background = "{sem['yellow']}"

[colors.search.focused_match]
foreground = "{get_fg_for_bg(accent)}"
background = "{accent}"

[colors.hints.start]
foreground = "{darker_bg}"
background = "{sem['yellow']}"

[colors.hints.end]
foreground = "{darker_bg}"
background = "{sem['green']}"

[colors.footer_bar]
background = "{bg_mid}"
foreground = "{fg}"

[colors.normal]
black   = "{ansi_black}"
red     = "{sem['red']}"
green   = "{sem['green']}"
yellow  = "{sem['yellow']}"
blue    = "{sem['blue']}"
magenta = "{sem['magenta']}"
cyan    = "{sem['cyan']}"
white   = "{fg}"

[colors.bright]
black   = "{muted}"
red     = "{sem['bright_red']}"
green   = "{sem['bright_green']}"
yellow  = "{sem['bright_yellow']}"
blue    = "{sem['bright_blue']}"
magenta = "{sem['bright_magenta']}"
cyan    = "{sem['bright_cyan']}"
white   = "{bright_fg}"
"""
write_both("alacritty.toml", alacritty)

# ══════════════════════════════════════════════════════════════════════════════
# 5 · FOOT Terminal
# ══════════════════════════════════════════════════════════════════════════════
foot = f"""[colors]
background={bg.lstrip('#')}
foreground={fg.lstrip('#')}
cursor={accent.lstrip('#')} {get_fg_for_bg(accent).lstrip('#')}
selection-target={selection_bg.lstrip('#')} {selection_fg.lstrip('#')}

regular0={ansi_black.lstrip('#')}
regular1={sem['red'].lstrip('#')}
regular2={sem['green'].lstrip('#')}
regular3={sem['yellow'].lstrip('#')}
regular4={sem['blue'].lstrip('#')}
regular5={sem['magenta'].lstrip('#')}
regular6={sem['cyan'].lstrip('#')}
regular7={fg.lstrip('#')}

bright0={muted.lstrip('#')}
bright1={sem['bright_red'].lstrip('#')}
bright2={sem['bright_green'].lstrip('#')}
bright3={sem['bright_yellow'].lstrip('#')}
bright4={sem['bright_blue'].lstrip('#')}
bright5={sem['bright_magenta'].lstrip('#')}
bright6={sem['bright_cyan'].lstrip('#')}
bright7={bright_fg.lstrip('#')}
"""
write_both("foot.ini", foot)

# ══════════════════════════════════════════════════════════════════════════════
# 6 · GHOSTTY Terminal
# ══════════════════════════════════════════════════════════════════════════════
ghostty = f"""# DANDADAN Ghostty — Wallpaper {active_idx}: {vibe}
background           = {bg.lstrip('#')}
foreground           = {fg.lstrip('#')}
cursor-color         = {accent.lstrip('#')}
cursor-text          = {get_fg_for_bg(accent).lstrip('#')}
selection-background = {selection_bg.lstrip('#')}
selection-foreground = {selection_fg.lstrip('#')}

palette = 0=#{ansi_black.lstrip('#')}
palette = 1=#{sem['red'].lstrip('#')}
palette = 2=#{sem['green'].lstrip('#')}
palette = 3=#{sem['yellow'].lstrip('#')}
palette = 4=#{sem['blue'].lstrip('#')}
palette = 5=#{sem['magenta'].lstrip('#')}
palette = 6=#{sem['cyan'].lstrip('#')}
palette = 7=#{fg.lstrip('#')}

palette = 8=#{muted.lstrip('#')}
palette = 9=#{sem['bright_red'].lstrip('#')}
palette = 10=#{sem['bright_green'].lstrip('#')}
palette = 11=#{sem['bright_yellow'].lstrip('#')}
palette = 12=#{sem['bright_blue'].lstrip('#')}
palette = 13=#{sem['bright_magenta'].lstrip('#')}
palette = 14=#{sem['bright_cyan'].lstrip('#')}
palette = 15=#{bright_fg.lstrip('#')}
"""
write_both("ghostty.conf", ghostty)

# ══════════════════════════════════════════════════════════════════════════════
# 7 · HYPRLAND Lua & Conf
# ══════════════════════════════════════════════════════════════════════════════
border_c2 = accent_comp.lstrip('#') if accent_comp != accent else cursor.lstrip('#')
hyprland_lua = f"""local active_border_color = {{ colors = {{ "rgb({accent.lstrip('#')})", "rgb({border_c2})" }}, angle = 45 }}
local inactive_border_color = "rgba(61636780)"
local active_shadow_color = "rgba({accent.lstrip('#')}66)"
local inactive_shadow_color = "rgba(00000044)"


hl.config({{
  general = {{
    col = {{
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    }},
  }},
  group = {{
    col = {{
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    }},
  }},
  decoration = {{
    shadow = {{
      enabled = true,
      range = 10,
      render_power = 4,
      color = active_shadow_color,
      color_inactive = inactive_shadow_color,
    }},
  }},
}})
"""
write_both("hyprland.lua", hyprland_lua)

hyprland_conf = f"""# DANDADAN Hyprland — Wallpaper {active_idx}: {vibe}
$active_border_color = rgb({accent.lstrip('#')}) rgb({border_c2}) 45deg
$inactive_border_color = rgba(61636780)
$shadow_color = rgba({accent.lstrip('#')}66)
"""
write_both("hyprland.conf", hyprland_conf)

hyprlock_conf = f"""$color           = rgb({bg.lstrip('#')})
$inner_color     = rgba(20, 22, 30, 0.88)
$outer_color     = rgb({accent.lstrip('#')})
$accent_color    = rgb({accent.lstrip('#')})
$font_color      = rgb({fg.lstrip('#')})
$placeholder_color = rgba(240, 244, 252, 0.50)
$check_color     = rgb({sem['blue'].lstrip('#')})

background {{
    blur_passes = 3
    blur_size   = 8
    vibrancy    = 0.85
    vibrancy_darkness = 0.3
}}
"""
write_both("hyprlock.conf", hyprlock_conf)

# ══════════════════════════════════════════════════════════════════════════════
# 8 · BTOP Resource Monitor
# ══════════════════════════════════════════════════════════════════════════════
btop = f"""# DANDADAN Btop — Wallpaper {active_idx}: {vibe}
theme[main_bg]="{bg}"
theme[main_fg]="{fg}"
theme[title]="{accent}"
theme[hi_fg]="{accent}"
theme[selected_bg]="{selection_bg}"
theme[selected_fg]="{bright_fg}"
theme[inactive_fg]="{muted}"
theme[proc_misc]="{sem['magenta']}"
theme[cpu_box]="{bg_mid}"
theme[mem_box]="{bg_mid}"
theme[net_box]="{bg_mid}"
theme[proc_box]="{bg_mid}"
theme[div_line]="{bg_mid}"
theme[temp_start]="{sem['green']}"
theme[temp_mid]="{sem['yellow']}"
theme[temp_end]="{sem['red']}"
theme[cpu_start]="{sem['green']}"
theme[cpu_mid]="{sem['yellow']}"
theme[cpu_end]="{sem['red']}"
theme[free_start]="{sem['green']}"
theme[free_mid]="{sem['yellow']}"
theme[free_end]="{sem['cyan']}"
theme[cached_start]="{sem['blue']}"
theme[cached_mid]="{sem['magenta']}"
theme[cached_end]="{accent}"
theme[available_start]="{sem['cyan']}"
theme[available_mid]="{sem['green']}"
theme[available_end]="{accent}"
theme[used_start]="{sem['green']}"
theme[used_mid]="{sem['yellow']}"
theme[used_end]="{sem['red']}"
theme[download_start]="{sem['cyan']}"
theme[download_mid]="{sem['blue']}"
theme[download_end]="{sem['magenta']}"
theme[upload_start]="{sem['yellow']}"
theme[upload_mid]="{sem['orange']}"
theme[upload_end]="{sem['red']}"
theme[graph_text]="{fg}"
theme[meter_bg]="{bg_mid}"
theme[process_start]="{accent}"
theme[process_mid]="{sem['yellow']}"
theme[process_end]="{sem['red']}"
"""
write_both("btop.theme", btop)

# ══════════════════════════════════════════════════════════════════════════════
# 9 · VS CODE / Antigravity IDE
# ══════════════════════════════════════════════════════════════════════════════
vscode_path = f"{THEME_DIR}/vscode.json"
try:
    with open(vscode_path) as f:
        vscode_data = json.load(f)
except Exception:
    vscode_data = {"name": "Dandadan", "type": "dark", "colors": {}, "tokenColors": []}

c = vscode_data.get("colors", {})
updates = {
    "activityBar.background": bg,
    "activityBar.foreground": fg,
    "activityBar.activeBorder": accent,
    "activityBar.inactiveForeground": muted,
    "activityBarBadge.background": accent,
    "activityBarBadge.foreground": get_fg_for_bg(accent),
    "badge.background": accent,
    "badge.foreground": get_fg_for_bg(accent),
    "button.background": accent,
    "button.foreground": get_fg_for_bg(accent),
    "button.hoverBackground": darken(accent),
    "button.secondaryBackground": highlight,
    "button.secondaryForeground": fg,
    "checkbox.background": bg_mid,
    "checkbox.border": accent,
    "checkbox.foreground": fg,
    "editor.background": bg,
    "editor.foreground": fg,
    "editor.lineHighlightBackground": bg_mid,
    "editor.selectionBackground": with_alpha(accent, "44"),
    "editor.wordHighlightBackground": with_alpha(accent_comp, "22"),
    "editor.findMatchBackground": with_alpha(sem['yellow'], "55"),
    "editor.findMatchHighlightBackground": with_alpha(sem['cyan'], "33"),
    "editorCursor.foreground": accent,
    "editorLineNumber.activeForeground": accent,
    "editorLineNumber.foreground": muted,
    "editorIndentGuide.activeBackground": with_alpha(accent, "60"),
    "editorIndentGuide.background": with_alpha(accent, "22"),
    "editorGroupHeader.tabsBackground": bg,
    "tab.activeBackground": bg_mid,
    "tab.activeForeground": fg,
    "tab.activeBorderTop": accent,
    "tab.inactiveBackground": bg,
    "tab.inactiveForeground": muted,
    "tab.border": bg_mid,
    "titleBar.activeBackground": bg,
    "titleBar.activeForeground": fg,
    "titleBar.inactiveBackground": bg,
    "titleBar.border": bg_mid,
    "statusBar.background": accent,
    "statusBar.foreground": get_fg_for_bg(accent),
    "statusBar.border": accent,
    "statusBarItem.remoteBackground": accent,
    "statusBarItem.remoteForeground": get_fg_for_bg(accent),
    "sideBar.background": bg,
    "sideBar.foreground": fg,
    "sideBar.border": bg_mid,
    "sideBarSectionHeader.background": bg_mid,
    "sideBarSectionHeader.foreground": accent,
    "list.activeSelectionBackground": with_alpha(accent, "33"),
    "list.activeSelectionForeground": fg,
    "list.hoverBackground": with_alpha(accent, "18"),
    "list.focusBackground": with_alpha(accent, "33"),
    "list.highlightForeground": accent,
    "focusBorder": accent,
    "selection.background": with_alpha(accent, "44"),
    "input.background": bg_mid,
    "input.foreground": fg,
    "input.border": with_alpha(accent, "60"),
    "inputOption.activeBorder": accent,
    "dropdown.background": bg_mid,
    "dropdown.border": with_alpha(accent, "60"),
    "dropdown.foreground": fg,
    "scrollbarSlider.background": with_alpha(accent, "30"),
    "scrollbarSlider.hoverBackground": with_alpha(accent, "55"),
    "scrollbarSlider.activeBackground": with_alpha(accent, "77"),
    "panel.background": bg,
    "panel.border": bg_mid,
    "panelTitle.activeForeground": accent,
    "panelTitle.activeBorder": accent,
    "terminal.background": bg,
    "terminal.foreground": fg,
    "terminal.ansiBlack": bg,
    "terminal.ansiRed": sem["red"],
    "terminal.ansiGreen": sem["green"],
    "terminal.ansiYellow": sem["yellow"],
    "terminal.ansiBlue": sem["blue"],
    "terminal.ansiMagenta": sem["magenta"],
    "terminal.ansiCyan": sem["cyan"],
    "terminal.ansiWhite": fg,
    "terminal.ansiBrightBlack": muted,
    "terminal.ansiBrightRed": sem["bright_red"],
    "terminal.ansiBrightGreen": sem["bright_green"],
    "terminal.ansiBrightYellow": sem["bright_yellow"],
    "terminal.ansiBrightBlue": sem["bright_blue"],
    "terminal.ansiBrightMagenta": sem["bright_magenta"],
    "terminal.ansiBrightCyan": sem["bright_cyan"],
    "terminal.ansiBrightWhite": bright_fg,
    "gitDecoration.addedResourceForeground": sem["green"],
    "gitDecoration.modifiedResourceForeground": sem["yellow"],
    "gitDecoration.deletedResourceForeground": sem["red"],
    "gitDecoration.untrackedResourceForeground": sem["cyan"],
    "gitDecoration.ignoredResourceForeground": muted,
    "notifications.background": bg_mid,
    "notifications.border": accent,
    "notificationCenterHeader.background": bg,
    "notificationCenterHeader.foreground": accent,
    "extensionButton.prominentBackground": accent,
    "extensionButton.prominentForeground": get_fg_for_bg(accent),
    "extensionButton.prominentHoverBackground": darken(accent),
    "progressBar.background": accent,
    "breadcrumb.foreground": "#A0A5B5",
    "breadcrumb.activeSelectionForeground": accent,
    "breadcrumbPicker.background": bg_mid,
    "peekView.border": accent,
    "peekViewEditor.background": bg_mid,
    "peekViewEditor.matchHighlightBackground": with_alpha(accent, "44"),
    "peekViewResult.background": bg,
    "peekViewResult.selectionBackground": with_alpha(accent, "33"),
    "peekViewTitle.background": bg,
    "peekViewTitleLabel.foreground": accent,
    "peekViewTitleDescription.foreground": "#A0A5B5",
    "merge.currentHeaderBackground": with_alpha(sem["green"], "44"),
    "merge.currentContentBackground": with_alpha(sem["green"], "22"),
    "merge.incomingHeaderBackground": with_alpha(accent, "44"),
    "merge.incomingContentBackground": with_alpha(accent, "22"),
    "widget.shadow": "#00000066",
}
c.update(updates)
vscode_data["colors"] = c
vscode_json_str = json.dumps(vscode_data, indent=2)
write_both("vscode.json", vscode_json_str)

# Sync Antigravity IDE / VS Code / Cursor extensions
for ext_dir in [
    f"{HOME}/.vscode/extensions/dandadan-theme",
    f"{HOME}/.antigravity-ide/extensions/dandadan-theme",
    f"{HOME}/.antigravity/extensions/dandadan-theme",
    f"{HOME}/.config/VSCodium/User/extensions/dandadan-theme",
    f"{HOME}/.cursor/extensions/dandadan-theme",
]:
    if os.path.exists(os.path.dirname(ext_dir)):
        themes_dir = f"{ext_dir}/themes"
        os.makedirs(themes_dir, exist_ok=True)
        write(f"{themes_dir}/dandadan-color-theme.json", vscode_json_str)

# ══════════════════════════════════════════════════════════════════════════════
# 10 · GTK CSS (GTK 3.0 & GTK 4.0)
# ══════════════════════════════════════════════════════════════════════════════
gtk_css = f"""/* DANDADAN GTK Theme — Wallpaper {active_idx}: {vibe} */
@define-color accent_color {accent};
@define-color accent_bg_color {accent};
@define-color accent_fg_color {get_fg_for_bg(accent)};
@define-color destructive_color {sem['red']};
@define-color destructive_bg_color {sem['red']};
@define-color destructive_fg_color #FFFFFF;
@define-color success_color {sem['green']};
@define-color warning_color {sem['yellow']};
@define-color error_color {sem['red']};
@define-color window_bg_color {bg};
@define-color window_fg_color {fg};
@define-color view_bg_color {bg_mid};
@define-color view_fg_color {fg};
@define-color headerbar_bg_color {bg};
@define-color headerbar_fg_color {fg};
@define-color headerbar_border_color {with_alpha(accent,'55')};
@define-color headerbar_backdrop_color {bg};
@define-color headerbar_shade_color rgba(0,0,0,0.2);
@define-color card_bg_color {bg_mid2};
@define-color card_fg_color {fg};
@define-color card_shade_color rgba(0,0,0,0.15);
@define-color dialog_bg_color {bg_mid};
@define-color dialog_fg_color {fg};
@define-color popover_bg_color {bg_mid};
@define-color popover_fg_color {fg};
@define-color shade_color rgba(0,0,0,0.2);
@define-color scrollbar_outline_color rgba(0,0,0,0.5);
@define-color sidebar_bg_color {bg};
@define-color sidebar_fg_color {fg};
@define-color sidebar_backdrop_color {bg};
@define-color sidebar_shade_color rgba(0,0,0,0.15);
@define-color thumbnail_bg_color {bg_mid};
@define-color thumbnail_fg_color {fg};

/* ── Selection highlight ─── */
selection {{ background-color: {with_alpha(accent,'55')}; color: {fg}; }}
"""
write_both("gtk.css", gtk_css)
os.makedirs(f"{THEME_DIR}/gtk-3.0", exist_ok=True)
os.makedirs(f"{THEME_DIR}/gtk-4.0", exist_ok=True)
write(f"{THEME_DIR}/gtk-3.0/gtk.css", f'@import "../gtk.css";\n')
write(f"{THEME_DIR}/gtk-4.0/gtk.css", f'@import "../gtk.css";\n')

# ══════════════════════════════════════════════════════════════════════════════
# 11 · ZED Editor
# ══════════════════════════════════════════════════════════════════════════════
zed_theme = {
    "$schema": "https://zed.dev/schema/themes/v0.1.0.json",
    "name": "Dandadan",
    "author": "misternegative21",
    "themes": [{
        "name": "Dandadan",
        "appearance": "dark",
        "style": {
            "background": bg + "F0",
            "editor.background": bg + "F0",
            "editor.foreground": fg,
            "text": fg,
            "text.muted": with_alpha(fg, "99"),
            "text.placeholder": with_alpha(fg, "66"),
            "text.disabled": with_alpha(fg, "44"),
            "text.accent": accent,
            "icon": fg,
            "icon.muted": muted,
            "icon.disabled": with_alpha(fg, "44"),
            "icon.placeholder": with_alpha(fg, "55"),
            "icon.accent": accent,
            "border": with_alpha(accent, "55"),
            "border.variant": with_alpha(accent, "33"),
            "border.focused": accent,
            "border.selected": accent,
            "border.transparent": "#00000000",
            "border.disabled": with_alpha(fg, "22"),
            "elevated_surface.background": bg_mid,
            "surface.background": bg,
            "element.background": bg_mid,
            "element.hover": with_alpha(accent, "1A"),
            "element.active": with_alpha(accent, "33"),
            "element.selected": with_alpha(accent, "22"),
            "element.disabled": with_alpha(bg_mid, "99"),
            "drop_target.background": with_alpha(accent, "1A"),
            "ghost_element.background": "#00000000",
            "ghost_element.hover": with_alpha(accent, "15"),
            "ghost_element.active": with_alpha(accent, "28"),
            "ghost_element.selected": with_alpha(accent, "1F"),
            "ghost_element.disabled": "#00000000",
            "link_text.hover": accent,
            "conflict": sem["red"],
            "conflict.background": with_alpha(sem["red"], "15"),
            "conflict.border": with_alpha(sem["red"], "55"),
            "created": sem["green"],
            "created.background": with_alpha(sem["green"], "15"),
            "created.border": with_alpha(sem["green"], "55"),
            "deleted": sem["red"],
            "deleted.background": with_alpha(sem["red"], "15"),
            "deleted.border": with_alpha(sem["red"], "55"),
            "error": sem["red"],
            "error.background": with_alpha(sem["red"], "15"),
            "error.border": with_alpha(sem["red"], "55"),
            "warning": sem["yellow"],
            "warning.background": with_alpha(sem["yellow"], "15"),
            "warning.border": with_alpha(sem["yellow"], "55"),
            "info": sem["blue"],
            "info.background": with_alpha(sem["blue"], "15"),
            "info.border": with_alpha(sem["blue"], "55"),
            "players": [
                {"cursor": accent, "background": accent, "selection": with_alpha(accent, "33")},
                {"cursor": sem["blue"], "background": sem["blue"], "selection": with_alpha(sem["blue"], "33")},
            ],
            "syntax": {
                "keyword": {"color": sem["magenta"], "weight": 700},
                "function": {"color": sem["cyan"]},
                "type": {"color": sem["yellow"]},
                "variable": {"color": fg},
                "string": {"color": sem["green"]},
                "number": {"color": sem["orange"]},
                "comment": {"color": muted, "font_style": "italic"},
                "operator": {"color": accent},
                "punctuation": {"color": light_fg},
                "tag": {"color": sem["red"]},
                "attribute": {"color": sem["yellow"]},
            }
        }
    }]
}
write_both("zed.json", json.dumps(zed_theme, indent=2))

# ══════════════════════════════════════════════════════════════════════════════
# 12 · SWAYOSD & MAKO
# ══════════════════════════════════════════════════════════════════════════════
swayosd_css = f"""window {{
  background: alpha({bg}, 0.92);
  border-radius: 16px;
  border: 2px solid {accent};
}}
image, label {{
  color: {fg};
}}
progressbar:disabled, image:disabled {{
  opacity: 0.5;
}}
progressbar {{
  background: alpha({fg}, 0.15);
  border-radius: 8px;
}}
trough {{
  border-radius: 8px;
}}
progress {{
  background: {accent};
  border-radius: 8px;
}}
"""
write_both("swayosd.css", swayosd_css)

mako_ini = f"""background-color={bg}F2
text-color={fg}
border-color={accent}
border-size=2
border-radius=10
progress-color=over {accent}

[urgency=low]
border-color={sem['blue']}

[urgency=normal]
border-color={accent}

[urgency=critical]
border-color={sem['red']}
text-color={bright_fg}
default-timeout=0
"""
write_both("mako.ini", mako_ini)

# ══════════════════════════════════════════════════════════════════════════════
# 13 · WALKER & WOFI Launchers
# ══════════════════════════════════════════════════════════════════════════════
walker_css = f"""/* DANDADAN Walker — Wallpaper {active_idx}: {vibe} */
#window {{
  background: transparent;
}}
#box {{
  background-color: alpha({bg}, 0.95);
  border: 2px solid {accent};
  border-radius: 16px;
  padding: 16px;
}}
#search {{
  background-color: {bg_mid};
  color: {fg};
  border: 1px solid alpha({accent}, 0.4);
  border-radius: 10px;
  padding: 10px 14px;
}}
#item:selected {{
  background-color: alpha({accent}, 0.22);
  border-radius: 8px;
  color: {bright_fg};
}}
"""
write_both("walker.css", walker_css)

wofi_css = f"""/* DANDADAN Wofi — Wallpaper {active_idx}: {vibe} */
window {{
  background-color: alpha({bg}, 0.95);
  border: 2px solid {accent};
  border-radius: 16px;
  color: {fg};
}}
#input {{
  background-color: {bg_mid};
  color: {fg};
  border: 1px solid alpha({accent}, 0.4);
  border-radius: 10px;
  margin: 12px;
}}
#entry:selected {{
  background-color: alpha({accent}, 0.25);
  border-radius: 8px;
}}
"""
write_both("wofi.css", wofi_css)

# ══════════════════════════════════════════════════════════════════════════════
# 14 · WARP & ZELLIJ Terminals
# ══════════════════════════════════════════════════════════════════════════════
warp_yaml = f"""accent: '{accent}'
background: '{bg}'
details: darker
foreground: '{fg}'
terminal_colors:
  bright:
    black: '{muted}'
    blue: '{sem['bright_blue']}'
    cyan: '{sem['bright_cyan']}'
    green: '{sem['bright_green']}'
    magenta: '{sem['bright_magenta']}'
    red: '{sem['bright_red']}'
    white: '{bright_fg}'
    yellow: '{sem['bright_yellow']}'
  normal:
    black: '{ansi_black}'
    blue: '{sem['blue']}'
    cyan: '{sem['cyan']}'
    green: '{sem['green']}'
    magenta: '{sem['magenta']}'
    red: '{sem['red']}'
    white: '{fg}'
    yellow: '{sem['yellow']}'
"""
write_both("warp.yaml", warp_yaml)

zellij_kdl = f"""// DANDADAN Zellij Theme — Wallpaper {active_idx}: {vibe}
themes {{
    dandadan {{
        fg "{fg}"
        bg "{bg}"
        black "{ansi_black}"
        red "{sem['red']}"
        green "{sem['green']}"
        yellow "{sem['yellow']}"
        blue "{sem['blue']}"
        magenta "{sem['magenta']}"
        cyan "{sem['cyan']}"
        white "{fg}"
        orange "{sem['orange']}"
    }}
}}
"""
write_both("zellij.kdl", zellij_kdl)
os.makedirs(f"{HOME}/.config/zellij/themes", exist_ok=True)
write(f"{HOME}/.config/zellij/themes/dandadan.kdl", zellij_kdl)

# ══════════════════════════════════════════════════════════════════════════════
# 15 · VENCORD, CHROMIUM, FIREFOX, TELEGRAM, NEOVIM
# ══════════════════════════════════════════════════════════════════════════════
vencord_css = f"""/**
 * @name Dandadan
 * @description Dynamic Dandadan theme — Wallpaper {active_idx}: {vibe}
 * @version 2.0.0
 * @author misternegative21
*/
@import url("https://refact0r.github.io/system24/build/system24.css");

body {{
    --font: "JetBrainsMono Nerd Font";
    --code-font: "JetBrainsMono Nerd Font";
    --text-0: {fg};
    --text-1: {fg};
    --text-5: {muted};
    --bg-1: {darken(bg_mid)};
    --bg-2: {bg_mid};
    --bg-3: {bg};
    --accent-1: {accent};
    --accent-2: {darken(accent)};
    --border: {with_alpha(accent,'55')};
    --status-positive-text: {sem['green']};
    --status-warning-text: {sem['yellow']};
    --status-danger-text: {sem['red']};
}}
"""
write_both("vencord.theme.css", vencord_css)

write_both("chromium.theme", f"{hex_to_rgb_str(accent)}\n")

firefox_css = f"""/* DANDADAN Firefox/Zen — Wallpaper {active_idx}: {vibe} */
:root {{
  --lwt-accent-color: {accent};
  --lwt-toolbar-field-focus: {accent};
  --toolbar-field-border-color: {accent};
  --toolbar-field-background-color: {bg};
  --toolbar-field-color: {fg};
  --lwt-tab-text: {fg};
  --lwt-selected-tab-background-color: {selection_bg};
  --tab-line-color: {accent};
}}
"""
write_both("firefox.css", firefox_css)

telegram = f"""// DANDADAN Telegram — Wallpaper {active_idx}: {vibe}
windowBg: {bg};
windowFg: {fg};
windowBgOver: {bg_mid};
windowBgRipple: {bg_mid2};
windowFgActive: #FFFFFF;
activeButtonBg: {accent};
activeButtonBgOver: {darken(accent)};
activeButtonBgRipple: {sem['magenta']};
activeButtonFg: #FFFFFF;
dialogsBg: {bg};
dialogsNameFg: {fg};
dialogsChatIconFg: {accent};
dialogsDateFg: {muted};
dialogsTextFg: #A0A5B5;
dialogsTextFgService: {accent};
dialogsUnreadBg: {accent};
dialogsUnreadBgMuted: {muted};
dialogsUnreadFg: #FFFFFF;
"""
write_both("telegram.palette", telegram)

neovim_lua = f"""-- DANDADAN Neovim — Wallpaper {active_idx}: {vibe}
return {{
    {{ "tahayvr/sunset-drive.nvim", lazy = false, priority = 1000 }},
    {{
        "LazyVim/LazyVim",
        opts = {{
            colorscheme = "sunsetdrive",
        }},
    }},
    {{
        "LazyVim/LazyVim",
        opts = function(_, opts)
            vim.api.nvim_set_hl(0, "Normal",          {{ bg = "{bg}", fg = "{fg}" }})
            vim.api.nvim_set_hl(0, "Visual",          {{ bg = "{selection_bg}", fg = "{bright_fg}", bold = true }})
            vim.api.nvim_set_hl(0, "Search",          {{ bg = "{sem['yellow']}", fg = "{darker_bg}", bold = true }})
            vim.api.nvim_set_hl(0, "CurSearch",       {{ bg = "{accent}", fg = "{get_fg_for_bg(accent)}", bold = true }})
            vim.api.nvim_set_hl(0, "IncSearch",       {{ bg = "{accent}", fg = "{get_fg_for_bg(accent)}", bold = true }})
            vim.api.nvim_set_hl(0, "CursorLine",      {{ bg = "{bg_mid}" }})
            vim.api.nvim_set_hl(0, "CursorLineNr",    {{ fg = "{accent}", bold = true }})
            vim.api.nvim_set_hl(0, "LineNr",          {{ fg = "{muted}" }})
            vim.api.nvim_set_hl(0, "Comment",         {{ fg = "{muted}", italic = true }})
            vim.api.nvim_set_hl(0, "StatusLine",      {{ bg = "{bg_mid}", fg = "{fg}" }})
            vim.api.nvim_set_hl(0, "StatusLineNC",    {{ bg = "{dark_bg}", fg = "{muted}" }})
            vim.api.nvim_set_hl(0, "Pmenu",           {{ bg = "{bg_mid}", fg = "{fg}" }})
            vim.api.nvim_set_hl(0, "PmenuSel",        {{ bg = "{selection_bg}", fg = "{bright_fg}", bold = true }})
            vim.api.nvim_set_hl(0, "PmenuThumb",      {{ bg = "{accent}" }})
            vim.api.nvim_set_hl(0, "DiagnosticError", {{ fg = "{sem['red']}" }})
            vim.api.nvim_set_hl(0, "DiagnosticWarn",  {{ fg = "{sem['yellow']}" }})
            vim.api.nvim_set_hl(0, "DiagnosticInfo",  {{ fg = "{sem['blue']}" }})
            vim.api.nvim_set_hl(0, "DiagnosticHint",  {{ fg = "{sem['cyan']}" }})
        end,
    }},
}}
"""
write_both("neovim.lua", neovim_lua)

write_both("icons.theme", f"{icon_theme_name}\n")

# ══════════════════════════════════════════════════════════════════════════════
# 16 · WAYBAR CSS (Legacy & Dual Fallback)
# ══════════════════════════════════════════════════════════════════════════════
waybar_css = f"""/* DANDADAN Waybar — Wallpaper {active_idx}: {vibe} */
@define-color background  {bg};
@define-color foreground  {fg};
@define-color accent      {accent};
@define-color cursor      {accent};
@define-color highlight   {highlight};
@define-color comp        {accent_comp};

* {{
  border: none;
  border-radius: 0;
  min-height: 0;
  font-family: 'JetBrainsMono Nerd Font', 'CaskaydiaMono Nerd Font', monospace;
  font-size: 13px;
  font-weight: bold;
}}

window#waybar {{
  background-color: alpha(@background, 0.40);
  border-bottom: 1px solid alpha(@accent, 0.40);
  transition: background-color 0.5s ease, border-color 0.5s ease;
}}

#group-left-container, #group-center-container, #group-right-container {{
  background-color: alpha(white, 0.07);
  border: 1px solid alpha(@accent, 0.35);
  border-top: none;
  border-radius: 0 0 20px 20px;
  padding: 4px 20px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.38);
}}
"""
write_both("waybar.css", waybar_css)

# Wallpapers CSS
wallpapers_css = f"""/* Dandadan Wallpaper {active_idx} - {vibe} */
@define-color background {bg};
@define-color foreground {fg};
@define-color accent {accent};
@define-color cursor {cursor};
@define-color highlight {highlight};
"""
write_both("wallpapers.css", wallpapers_css)
write(f"{HOME}/.config/waybar/wallpapers.css", wallpapers_css)
write(f"{HOME}/.config/waybar/style.css", f'@import "{HOME}/.config/omarchy/current/theme/waybar.css";\n')

# Sync Dandadan Quickshell layout and ensure opaque bar for high visibility
try:
    curr_theme_name = ""
    for name_file in [f"{HOME}/.local/state/omarchy/current/theme.name", f"{HOME}/.config/omarchy/current/theme.name"]:
        if os.path.exists(name_file):
            with open(name_file) as nf:
                curr_theme_name = nf.read().strip()
            break
    if curr_theme_name in ["dandadan", "dandadan-theme"]:
        theme_shell_json = f"{THEME_DIR}/shell.json"
        user_shell_json = f"{HOME}/.config/omarchy/shell.json"
        if os.path.exists(theme_shell_json):
            with open(theme_shell_json) as sf:
                sj_data = json.load(sf)
            sj_data.setdefault("bar", {})["transparent"] = False
            write_both("shell.json", json.dumps(sj_data, indent=2) + "\n")
            need_user_update = True
            if os.path.exists(user_shell_json):
                with open(user_shell_json) as uf:
                    try:
                        u_data = json.load(uf)
                        if u_data.get("bar", {}).get("transparent") is False:
                            need_user_update = False
                    except Exception:
                        pass
            if need_user_update:
                write(user_shell_json, json.dumps(sj_data, indent=2) + "\n")
except Exception:
    pass

# ══════════════════════════════════════════════════════════════════════════════
# 17 · LIVE QUICKSHELL IPC & APP RELOADS
# ══════════════════════════════════════════════════════════════════════════════
def is_process_running(proc_name: str) -> bool:
    try:
        res = subprocess.run(["pgrep", "-x", proc_name], capture_output=True)
        if res.returncode == 0:
            return True
        res2 = subprocess.run(["pgrep", "-f", proc_name], capture_output=True)
        return res2.returncode == 0
    except Exception:
        return False

# Live Quickshell IPC
if is_process_running("quickshell") or is_process_running("omarchy-shell"):
    try:
        colors_b64 = base64.b64encode(colors_toml.encode("utf-8")).decode("utf-8")
        shell_b64  = base64.b64encode(shell_toml.encode("utf-8")).decode("utf-8")
        subprocess.run(["omarchy-shell", "-q", "shell", "applyTheme", colors_b64, shell_b64], capture_output=True)
        subprocess.run(["omarchy-shell", "-q", "shell", "reloadConfig"], capture_output=True)
    except Exception:
        pass

# Ensure live background watcher is running if Dandadan is current theme
watch_script = f"{THEME_DIR}/scripts/dandadan-bg-watch.sh"
if os.path.exists(watch_script) and not is_process_running("dandadan-bg-watch"):
    try:
        subprocess.Popen(["bash", watch_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    except Exception:
        pass

# Waybar reload signal if waybar is running
if is_process_running("waybar"):
    try:
        subprocess.run(["pkill", "-SIGUSR2", "waybar"], capture_output=True)
    except Exception:
        pass

for cmd in [
    ["omarchy-restart-terminal"],
    ["omarchy-theme-set-foot"],
    ["omarchy-theme-set-browser"],
    ["omarchy-theme-set-gnome"],
    ["makoctl", "reload"],
]:
    try:
        subprocess.run(cmd, capture_output=True)
    except Exception:
        pass

print(f"✓ Dynamic recoloring engine updated for wallpaper {active_idx}: {vibe}")
print(f"  Strict semantic ANSI channels active (no inverted terminal colors)")
print(f"  Quickshell surface tokens and Omarchy 4.0 colors.toml updated")
