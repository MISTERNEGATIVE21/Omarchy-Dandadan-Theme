#!/usr/bin/env python3
"""
DANDADAN OMARCHY THEME — Universal Dynamic Color Engine
═══════════════════════════════════════════════════════
Updates ALL 21 config targets on every wallpaper change.
Uses complementary color theory for accent/highlight pairing.
Supports 52 wallpapers (001-058, with gaps).

Targets: Neovim · GTK · Zed · VS Code · Alacritty · Btop · Chromium
         Foot · Ghostty · Hyprland · Hyprlock · Icons · Kitty · Mako
         SwayOSD · Vencord · Walker · Warp · Waybar · Wofi · Zellij
"""

import json, os, sys, subprocess, colorsys, math

# ─── Paths ─────────────────────────────────────────────────────────────────────
HOME      = os.path.expanduser("~")
THEME_DIR = f"{HOME}/.config/omarchy/themes/dandadan-theme"
CURR_DIR  = f"{HOME}/.config/omarchy/current/theme"

manifest_path   = f"{THEME_DIR}/wallpaper_highlights.json"
current_bg_link = f"{HOME}/.config/omarchy/current/background"

if not os.path.exists(manifest_path):
    sys.exit(0)

with open(manifest_path) as f:
    data = json.load(f)

# ─── Detect active wallpaper ────────────────────────────────────────────────────
active_idx = "32"
if os.path.islink(current_bg_link) or os.path.exists(current_bg_link):
    try:
        target = os.readlink(current_bg_link) if os.path.islink(current_bg_link) else current_bg_link
        base   = os.path.basename(target)
        # handles "032.webp", "32.webp", "1-name.jpg" etc.
        num    = base.split(".")[0].split("-")[0].lstrip("0") or "0"
        idx    = num.zfill(2)
        if idx in data:
            active_idx = idx
        # Try 3-digit zero-padded too (033.webp → 33 → "33" not in data → "33".zfill(2)="33" ✓)
    except Exception:
        pass

colors    = data.get(active_idx, data.get("32", {}))
accent    = colors.get("accent",    "#C12719")
cursor    = colors.get("border",    colors.get("glow", accent))
highlight = colors.get("highlight", "#3043AE")
bg        = colors.get("background","#14161E")
fg        = colors.get("foreground","#F0F4FC")
vibe      = colors.get("vibe",      f"Dandadan Scene {active_idx}")

# ─── Color math helpers ─────────────────────────────────────────────────────────
def h2r(hex_code: str):
    h = hex_code.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def r2h(r, g, b) -> str:
    return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

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

def analogous(hex_code: str, offset: float = 0.083) -> tuple:
    """Return two analogous colors (±30° offset)."""
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    r1, g1, b1 = colorsys.hsv_to_rgb((h + offset) % 1, s, v)
    r2, g2, b2 = colorsys.hsv_to_rgb((h - offset) % 1, s, v)
    return r2h(r1*255, g1*255, b1*255), r2h(r2*255, g2*255, b2*255)

def darken(hex_code: str, factor: float = 0.65) -> str:
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v * factor)
    return r2h(r2*255, g2*255, b2*255)

def lighten(hex_code: str, factor: float = 1.3, max_v: float = 0.95) -> str:
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    r2, g2, b2 = colorsys.hsv_to_rgb(h, max(s*0.7, 0), min(v * factor, max_v))
    return r2h(r2*255, g2*255, b2*255)

def with_alpha(hex_code: str, alpha_hex: str = "AA") -> str:
    return hex_code + alpha_hex

def triadic(hex_code: str) -> tuple:
    r, g, b = h2r(hex_code)
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    r1,g1,b1 = colorsys.hsv_to_rgb((h+1/3)%1, s, v)
    r2,g2,b2 = colorsys.hsv_to_rgb((h+2/3)%1, s, v)
    return r2h(r1*255,g1*255,b1*255), r2h(r2*255,g2*255,b2*255)

# Computed palette
accent_comp  = complementary(accent)     # 180° complement of accent
accent_dark  = darken(accent, 0.7)
accent_light = lighten(accent)
cursor_comp  = complementary(cursor)
highlight_comp = complementary(highlight)
tri1, tri2   = triadic(accent)
ana1, ana2   = analogous(accent)

# Mid-tone bg variants
bg_mid  = "#1A1C26"   # slightly lighter bg
bg_mid2 = "#1E2030"   # card/panel bg
bg_sel  = "#252840"   # selection bg

# Accent with alpha for GTK/CSS backgrounds
accent_12 = with_alpha(accent, "1F")
accent_22 = with_alpha(accent, "38")
accent_44 = with_alpha(accent, "70")

print(f"[dandadan] wallpaper {active_idx} — {vibe}")
print(f"  accent={accent}  cursor={cursor}  highlight={highlight}")
print(f"  complement={accent_comp}  triadic=({tri1},{tri2})")

def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def write_both(filename: str, content: str):
    """Write to both theme dir and current/theme dir."""
    write(f"{THEME_DIR}/{filename}", content)
    write(f"{CURR_DIR}/{filename}", content)


# ══════════════════════════════════════════════════════════════════════════════
# 1 · WAYBAR — per-wallpaper full CSS (not just variables)
# ══════════════════════════════════════════════════════════════════════════════
waybar_css = f"""/* DANDADAN Waybar — Wallpaper {active_idx}: {vibe}
   accent={accent}  cursor={cursor}  highlight={highlight}  comp={accent_comp}
*/

/* ── Core color variables ─────────────────────────────────────────── */
@define-color background  {bg};
@define-color foreground  {fg};
@define-color accent      {accent};
@define-color cursor      {cursor};
@define-color highlight   {highlight};
@define-color comp        {accent_comp};
@define-color accent_dark {accent_dark};

* {{
  border: none;
  border-radius: 0;
  min-height: 0;
  font-family: 'JetBrainsMono Nerd Font', 'CaskaydiaMono Nerd Font', monospace;
  font-size: 13px;
  font-weight: bold;
}}

/* ── Bar window ──────────────────────────────────────────────────── */
window#waybar {{
  background-color: alpha(@background, 0.40);
  border-bottom: 1px solid alpha(@accent, 0.40);
  transition: background-color 0.5s ease, border-color 0.5s ease;
}}

window#waybar.hidden {{ opacity: 0.2; }}

/* ── Floating Island Pill Containers ────────────────────────────── */
#group-left-container {{
  background-color: alpha(white, 0.07);
  border: 1px solid alpha(@accent, 0.35);
  border-top: none;
  border-radius: 0 0 20px 20px;
  margin: 0 10px 4px 14px;
  padding: 4px 20px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.38),
              inset 0 1px 0 alpha(@accent, 0.15);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}}

#group-center-container {{
  background-color: alpha(white, 0.07);
  border: 1px solid alpha(@accent, 0.35);
  border-top: none;
  border-radius: 0 0 20px 20px;
  margin: 0 10px 4px 10px;
  padding: 4px 20px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.38),
              inset 0 1px 0 alpha(@accent, 0.15);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}}

#group-right-container {{
  background-color: alpha(white, 0.07);
  border: 1px solid alpha(@accent, 0.35);
  border-top: none;
  border-radius: 0 0 20px 20px;
  margin: 0 14px 4px 10px;
  padding: 4px 24px 4px 20px;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.38),
              inset 0 1px 0 alpha(@accent, 0.15);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}}

#group-left-container:hover,
#group-center-container:hover,
#group-right-container:hover {{
  background-color: alpha(@accent, 0.11);
  border-color: alpha(@accent, 0.60);
  box-shadow: 0 0 28px alpha(@accent, 0.35),
              inset 0 1px 0 alpha(@accent, 0.25);
}}

/* ── Omarchy logo ────────────────────────────────────────────────── */
#custom-omarchy {{
  color: {accent};
  font-size: 17px;
  padding: 0 12px 0 4px;
  margin-right: 8px;
  border-right: 1px solid alpha(white, 0.20);
  transition: color 0.2s, text-shadow 0.2s;
}}
#custom-omarchy:hover {{
  color: {cursor};
  text-shadow: 0 0 14px {cursor}, 0 0 28px {accent};
}}

/* ── Workspaces ──────────────────────────────────────────────────── */
#workspaces {{ padding: 0 6px; margin: 0 4px; background: transparent; }}

#workspaces button {{
  color: alpha(white, 0.65);
  font-size: 14px;
  padding: 0 6px; margin: 0 2px;
  background: transparent;
  border: none; box-shadow: none;
  transition: all 0.2s ease;
  border-radius: 6px;
}}
#workspaces button:hover {{
  color: white;
  background: alpha({accent}, 0.12);
}}
#workspaces button.active {{
  color: {accent};
  font-size: 15px; font-weight: 900;
  text-shadow: 0 0 12px {accent}, 0 0 24px {cursor};
}}
#workspaces button.urgent {{
  color: #FF454F;
  text-shadow: 0 0 10px #FF454F;
}}
#workspaces button.empty {{ opacity: 0.40; }}

/* ── Active window ───────────────────────────────────────────────── */
#custom-active_window, #hyprland-window {{
  color: alpha(white, 0.88);
  padding-left: 12px;
  margin-left: 4px;
  border-left: 1px solid alpha({accent}, 0.35);
  font-size: 12px; font-weight: 400;
}}

/* ── Media / MPRIS ───────────────────────────────────────────────── */
#custom-mpris, #mpris {{
  color: {highlight};
  font-style: italic;
  font-weight: 600;
  padding: 0 14px;
  transition: color 0.3s;
}}
#custom-mpris:hover, #mpris:hover {{ color: {accent}; }}

/* ── Indicators ──────────────────────────────────────────────────── */
#custom-idle-indicator,
#custom-notification-silencing-indicator,
#custom-update {{
  color: {accent_comp};
  padding: 0 6px;
  margin: 0 1px;
}}
#custom-screenrecording-indicator {{
  color: #FF454F;
  padding: 0 6px;
  margin: 0 1px;
  text-shadow: 0 0 8px #FF454F;
}}

/* ── Clock (Single Line Horizontal) ──────────────────────────────── */
#clock, #custom-clock {{
  color: {accent};
  padding: 0 12px;
  margin: 0 4px;
  font-weight: bold;
  font-size: 13px;
  transition: color 0.3s;
}}
#clock:hover, #custom-clock:hover {{ color: {cursor}; }}

/* ── Weather ─────────────────────────────────────────────────────── */
#custom-weather {{
  color: {accent_comp};
  padding: 0 8px;
  margin: 0 2px;
}}

/* ── CPU ─────────────────────────────────────────────────────────── */
#cpu {{
  color: {highlight};
  margin: 0 6px;
  transition: color 0.3s;
}}
#cpu.warning {{ color: #FFA726; }}
#cpu.critical {{ color: #FF454F; text-shadow: 0 0 6px #FF454F; }}

/* ── Memory ──────────────────────────────────────────────────────── */
#memory {{
  color: {cursor};
  margin: 0 6px;
  transition: color 0.3s;
}}
#memory.warning {{ color: #FFA726; }}
#memory.critical {{ color: #FF454F; }}

/* ── Audio ───────────────────────────────────────────────────────── */
#pulseaudio, #wireplumber {{
  color: {accent};
  margin: 0 6px;
  transition: color 0.3s;
}}
#pulseaudio.muted, #wireplumber.muted {{ color: alpha(white, 0.35); }}

/* ── Battery ─────────────────────────────────────────────────────── */
#battery {{
  color: {cursor};
  margin: 0 6px;
  transition: color 0.4s;
}}
#battery.charging {{ color: #4CAF50; text-shadow: 0 0 8px #4CAF50; }}
#battery.warning:not(.charging) {{ color: #FFA726; }}
#battery.critical:not(.charging) {{
  color: #FF454F;
  text-shadow: 0 0 8px #FF454F;
  animation: blink 1s step-end infinite;
}}
@keyframes blink {{ 50% {{ opacity: 0; }} }}

/* ── Network & Bluetooth Icons (Generous Spacing & Centered Icons) ── */
#network, #bluetooth {{
  color: {fg};
  padding: 0 8px;
  margin: 0 4px;
  min-width: 18px;
}}
#network.disconnected {{ color: alpha(white, 0.3); }}
#bluetooth.connected {{ color: {accent}; }}
#bluetooth.disabled {{ color: alpha(white, 0.28); }}

/* ── Tray ────────────────────────────────────────────────────────── */
#tray {{ margin: 0 8px 0 6px; padding: 0 6px; }}
#tray > .passive {{ -gtk-icon-effect: dim; }}
#tray > .needs-attention {{
  -gtk-icon-effect: highlight;
  background-color: alpha({cursor}, 0.18);
  border-radius: 4px;
}}

/* ── Tooltip ─────────────────────────────────────────────────────── */
tooltip {{
  background: alpha({bg}, 0.96);
  border: 1px solid {accent};
  border-radius: 10px;
  box-shadow: 0 6px 22px rgba(0,0,0,0.5);
}}
tooltip label {{ color: {fg}; }}
"""

write_both("waybar.css", waybar_css)
write(f"{HOME}/.config/waybar/wallpapers.css",
    f"/* Dandadan Wallpaper {active_idx} - {vibe} */\n"
    f"@define-color background {bg};\n"
    f"@define-color foreground {fg};\n"
    f"@define-color accent {accent};\n"
    f"@define-color cursor {cursor};\n"
    f"@define-color highlight {highlight};\n"
)
# Also update the omarchy current/theme wallpapers.css (the canonical one)
write(f"{CURR_DIR}/wallpapers.css",
    f"/* Dandadan Wallpaper {active_idx} - {vibe} */\n"
    f"@define-color background {bg};\n"
    f"@define-color foreground {fg};\n"
    f"@define-color accent {accent};\n"
    f"@define-color cursor {cursor};\n"
    f"@define-color highlight {highlight};\n"
)
# Deploy style.css to waybar
write(f"{HOME}/.config/waybar/style.css",
    f'@import "/home/mister/.config/omarchy/current/theme/waybar.css";\n')


# ══════════════════════════════════════════════════════════════════════════════
# 2 · MAKO notifications
# ══════════════════════════════════════════════════════════════════════════════
mako = f"""text-color={fg}
border-color={accent}
background-color={bg}
border-radius=14
width=420
height=110
padding=12
border-size=2
font=Liberation Sans 11
anchor=top-right
outer-margin=20
default-timeout=5000
max-icon-size=32
[app-name=Spotify]
invisible=1
[mode=do-not-disturb]
invisible=true
[mode=do-not-disturb app-name=notify-send]
invisible=false
"""
write_both("mako.ini", mako)


# ══════════════════════════════════════════════════════════════════════════════
# 3 · SWAYOSD OSD overlay
# ══════════════════════════════════════════════════════════════════════════════
swayosd = f"""@define-color background-color {bg};
@define-color border-color {accent};
@define-color label {fg};
@define-color image {cursor};
@define-color progress {accent};

window {{
  border-radius: 14px;
  border: 2px solid @border-color;
  background-color: alpha(@background-color, 0.92);
  box-shadow: 0 8px 30px rgba(0,0,0,0.45);
  padding: 10px;
}}
label  {{ color: @label; }}
image  {{ color: @image; }}
progressbar {{ border-radius: 12px; }}
progress {{ background-color: @progress; border-radius: 12px; }}
"""
write_both("swayosd.css", swayosd)


# ══════════════════════════════════════════════════════════════════════════════
# 4 · HYPRLOCK lock screen
# ══════════════════════════════════════════════════════════════════════════════
br, bg2, bb = h2r(bg)
fr, fg2, fb = h2r(fg)
hyprlock = f"""$color           = rgb({bg.lstrip('#')})
$inner_color     = rgba({br}, {bg2}, {bb}, 0.88)
$outer_color     = rgb({accent.lstrip('#')})
$accent_color    = rgb({cursor.lstrip('#')})
$font_color      = rgb({fg.lstrip('#')})
$placeholder_color = rgba({fr}, {fg2}, {fb}, 0.50)
$check_color     = rgb({highlight.lstrip('#')})

background {{
    blur_passes = 3
    blur_size   = 8
    vibrancy    = 0.85
    vibrancy_darkness = 0.3
}}
"""
write_both("hyprlock.conf", hyprlock)


# ══════════════════════════════════════════════════════════════════════════════
# 5 · HYPRLAND borders + hyprland.lua
# ══════════════════════════════════════════════════════════════════════════════
hyprland_conf = f"""general {{
    col.active_border   = rgb({accent.lstrip('#')}) rgb({cursor.lstrip('#')}) 45deg
    col.inactive_border = rgba(97,99,103,0.45)
}}
"""
write_both("hyprland.conf", hyprland_conf)

# hyprland.lua — Hyprland Lua config (new parser)
hyprland_lua = f"""local active_border_color = "rgb({accent.lstrip('#')})"
local inactive_border_color = "rgba(61636780)"

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
}})
"""
write_both("hyprland.lua", hyprland_lua)

try:
    c1, c2 = accent.lstrip("#"), cursor.lstrip("#")
    subprocess.run(["hyprctl", "keyword", "general:col.active_border",
                    f"rgb({c1}) rgb({c2}) 45deg"],
                   capture_output=True)
except Exception:
    pass


# ══════════════════════════════════════════════════════════════════════════════
# 6 · ALACRITTY terminal
# ══════════════════════════════════════════════════════════════════════════════
# Build a vivid 16-color palette derived from accent + complement
r1, g1, b1 = h2r(accent)
r2, g2, b2 = h2r(accent_comp)
# Normal colors: bg, red(cursor), green(highlight), yellow(ana1), blue(tri1), magenta(accent), cyan(tri2), fg
# Bright: brighter variants
alacritty = f"""[colors.primary]
background = "{bg}"
foreground = "{fg}"

[colors.cursor]
cursor = "{cursor}"
text   = "#FFFFFF"

[colors.selection]
background = "{with_alpha(accent,'66')}"
foreground = "{fg}"

[colors.search.matches]
foreground = "#FFFFFF"
background = "{cursor}"

[colors.search.focused_match]
foreground = "{bg}"
background = "{accent}"

[colors.footer_bar]
background = "{bg_mid}"
foreground = "{fg}"

[colors.normal]
black   = "{bg}"
red     = "{cursor}"
green   = "{highlight}"
yellow  = "{ana1}"
blue    = "{tri1}"
magenta = "{accent}"
cyan    = "{tri2}"
white   = "{fg}"

[colors.bright]
black   = "#616367"
red     = "{lighten(cursor)}"
green   = "{lighten(highlight)}"
yellow  = "{lighten(ana1)}"
blue    = "{lighten(tri1)}"
magenta = "{lighten(accent)}"
cyan    = "{lighten(tri2)}"
white   = "#FFFFFF"
"""
write_both("alacritty.toml", alacritty)


# ══════════════════════════════════════════════════════════════════════════════
# 7 · KITTY terminal
# ══════════════════════════════════════════════════════════════════════════════
kitty = f"""# DANDADAN Kitty — Wallpaper {active_idx}: {vibe}
background {bg}
foreground {fg}

cursor            {cursor}
cursor_text_color #FFFFFF

selection_background {with_alpha(accent,'66')}
selection_foreground {fg}

url_color {accent_comp}

active_border_color   {accent}
inactive_border_color #616367
bell_border_color     {cursor}

active_tab_background   {accent}
active_tab_foreground   #FFFFFF
inactive_tab_background {bg_mid}
inactive_tab_foreground #A0A5B5
tab_bar_background      {bg}

color0  {bg}
color1  {cursor}
color2  {highlight}
color3  {ana1}
color4  {tri1}
color5  {accent}
color6  {tri2}
color7  {fg}

color8  #616367
color9  {lighten(cursor)}
color10 {lighten(highlight)}
color11 {lighten(ana1)}
color12 {lighten(tri1)}
color13 {lighten(accent)}
color14 {lighten(tri2)}
color15 #FFFFFF
"""
write_both("kitty.conf", kitty)


# ══════════════════════════════════════════════════════════════════════════════
# 8 · FOOT terminal
# ══════════════════════════════════════════════════════════════════════════════
foot = f"""[colors]
background={bg.lstrip('#')}
foreground={fg.lstrip('#')}
cursor={cursor.lstrip('#')} FFFFFF
selection-target={accent.lstrip('#')}66 {fg.lstrip('#')}

regular0={bg.lstrip('#')}
regular1={cursor.lstrip('#')}
regular2={highlight.lstrip('#')}
regular3={ana1.lstrip('#')}
regular4={tri1.lstrip('#')}
regular5={accent.lstrip('#')}
regular6={tri2.lstrip('#')}
regular7={fg.lstrip('#')}

bright0=616367
bright1={lighten(cursor).lstrip('#')}
bright2={lighten(highlight).lstrip('#')}
bright3={lighten(ana1).lstrip('#')}
bright4={lighten(tri1).lstrip('#')}
bright5={lighten(accent).lstrip('#')}
bright6={lighten(tri2).lstrip('#')}
bright7=FFFFFF
"""
write_both("foot.ini", foot)


# ══════════════════════════════════════════════════════════════════════════════
# 9 · GHOSTTY terminal
# ══════════════════════════════════════════════════════════════════════════════
ghostty = f"""# DANDADAN Ghostty — Wallpaper {active_idx}: {vibe}
background           = {bg.lstrip('#')}
foreground           = {fg.lstrip('#')}
cursor-color         = {cursor.lstrip('#')}
cursor-text          = FFFFFF
selection-background = {accent.lstrip('#')}66
selection-foreground = {fg.lstrip('#')}

palette = 0=#{bg.lstrip('#')}
palette = 1=#{cursor.lstrip('#')}
palette = 2=#{highlight.lstrip('#')}
palette = 3=#{ana1.lstrip('#')}
palette = 4=#{tri1.lstrip('#')}
palette = 5=#{accent.lstrip('#')}
palette = 6=#{tri2.lstrip('#')}
palette = 7=#{fg.lstrip('#')}

palette = 8=#616367
palette = 9=#{lighten(cursor).lstrip('#')}
palette = 10=#{lighten(highlight).lstrip('#')}
palette = 11=#{lighten(ana1).lstrip('#')}
palette = 12=#{lighten(tri1).lstrip('#')}
palette = 13=#{lighten(accent).lstrip('#')}
palette = 14=#{lighten(tri2).lstrip('#')}
palette = 15=#FFFFFF
"""
write_both("ghostty.conf", ghostty)


# ══════════════════════════════════════════════════════════════════════════════
# 10 · BTOP resource monitor
# ══════════════════════════════════════════════════════════════════════════════
btop = f"""# DANDADAN Btop — Wallpaper {active_idx}: {vibe}
theme[main_bg]="{bg}"
theme[main_fg]="{fg}"
theme[title]="{accent}"
theme[hi_fg]="{cursor}"
theme[selected_bg]="{cursor}"
theme[selected_fg]="#FFFFFF"
theme[inactive_fg]="#616367"
theme[proc_misc]="{accent_comp}"
theme[cpu_box]="{bg_mid}"
theme[mem_box]="{bg_mid}"
theme[net_box]="{bg_mid}"
theme[proc_box]="{bg_mid}"
theme[div_line]="{bg_mid}"
theme[temp_start]="{highlight}"
theme[temp_mid]="{cursor}"
theme[temp_end]="{accent}"
theme[cpu_start]="{highlight}"
theme[cpu_mid]="{cursor}"
theme[cpu_end]="{accent}"
theme[free_start]="{highlight}"
theme[free_mid]="{cursor}"
theme[free_end]="{accent}"
theme[cached_start]="{tri1}"
theme[cached_mid]="{accent}"
theme[cached_end]="{cursor}"
theme[available_start]="{tri2}"
theme[available_mid]="{highlight}"
theme[available_end]="{accent}"
theme[used_start]="{cursor}"
theme[used_mid]="{accent}"
theme[used_end]="{darken(accent)}"
theme[download_start]="{accent_comp}"
theme[download_mid]="{highlight}"
theme[download_end]="{cursor}"
theme[upload_start]="{tri1}"
theme[upload_mid]="{accent}"
theme[upload_end]="{cursor}"
theme[graph_text]="{fg}"
theme[meter_bg]="{bg_mid}"
theme[process_start]="{accent}"
theme[process_mid]="{cursor}"
theme[process_end]="{highlight}"
"""
write_both("btop.theme", btop)


# ══════════════════════════════════════════════════════════════════════════════
# 11 · VS CODE / Antigravity IDE
# ══════════════════════════════════════════════════════════════════════════════
# Read existing vscode.json structure and update color keys only
vscode_path = f"{THEME_DIR}/vscode.json"
try:
    with open(vscode_path) as f:
        vscode_data = json.load(f)
except Exception:
    vscode_data = {"name": "Dandadan", "type": "dark", "colors": {}, "tokenColors": []}

c = vscode_data.get("colors", {})
# Update key colors
updates = {
    "activityBar.background": bg,
    "activityBar.foreground": fg,
    "activityBar.activeBorder": accent,
    "activityBar.inactiveForeground": "#616367",
    "activityBarBadge.background": cursor,
    "activityBarBadge.foreground": "#FFFFFF",
    "badge.background": cursor,
    "badge.foreground": "#FFFFFF",
    "button.background": accent,
    "button.foreground": "#FFFFFF",
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
    "editor.findMatchBackground": with_alpha(cursor, "55"),
    "editor.findMatchHighlightBackground": with_alpha(highlight, "33"),
    "editorCursor.foreground": cursor,
    "editorLineNumber.activeForeground": accent,
    "editorLineNumber.foreground": "#616367",
    "editorIndentGuide.activeBackground": with_alpha(accent, "60"),
    "editorIndentGuide.background": with_alpha(accent, "22"),
    "editorGroupHeader.tabsBackground": bg,
    "tab.activeBackground": bg_mid,
    "tab.activeForeground": fg,
    "tab.activeBorderTop": accent,
    "tab.inactiveBackground": bg,
    "tab.inactiveForeground": "#616367",
    "tab.border": bg_mid,
    "titleBar.activeBackground": bg,
    "titleBar.activeForeground": fg,
    "titleBar.inactiveBackground": bg,
    "titleBar.border": bg_mid,
    "statusBar.background": accent,
    "statusBar.foreground": "#FFFFFF",
    "statusBar.border": accent,
    "statusBarItem.remoteBackground": cursor,
    "statusBarItem.remoteForeground": "#FFFFFF",
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
    "terminal.ansiRed": cursor,
    "terminal.ansiGreen": highlight,
    "terminal.ansiYellow": ana1,
    "terminal.ansiBlue": tri1,
    "terminal.ansiMagenta": accent,
    "terminal.ansiCyan": tri2,
    "terminal.ansiWhite": fg,
    "terminal.ansiBrightBlack": "#616367",
    "terminal.ansiBrightRed": lighten(cursor),
    "terminal.ansiBrightGreen": lighten(highlight),
    "terminal.ansiBrightYellow": lighten(ana1),
    "terminal.ansiBrightBlue": lighten(tri1),
    "terminal.ansiBrightMagenta": lighten(accent),
    "terminal.ansiBrightCyan": lighten(tri2),
    "terminal.ansiBrightWhite": "#FFFFFF",
    "gitDecoration.addedResourceForeground": highlight,
    "gitDecoration.modifiedResourceForeground": accent_comp,
    "gitDecoration.deletedResourceForeground": cursor,
    "gitDecoration.untrackedResourceForeground": tri1,
    "gitDecoration.ignoredResourceForeground": "#616367",
    "notifications.background": bg_mid,
    "notifications.border": accent,
    "notificationCenterHeader.background": bg,
    "notificationCenterHeader.foreground": accent,
    "extensionButton.prominentBackground": accent,
    "extensionButton.prominentForeground": "#FFFFFF",
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
    "merge.currentHeaderBackground": with_alpha(highlight, "44"),
    "merge.currentContentBackground": with_alpha(highlight, "22"),
    "merge.incomingHeaderBackground": with_alpha(accent, "44"),
    "merge.incomingContentBackground": with_alpha(accent, "22"),
    "widget.shadow": "#00000066",
}
c.update(updates)
vscode_data["colors"] = c
vscode_json_str = json.dumps(vscode_data, indent=2)
write_both("vscode.json", vscode_json_str)

# Sync Antigravity IDE, VS Code, VSCodium, Cursor theme extensions & settings.json
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
        pkg_json = {
            "name": "dandadan-theme",
            "displayName": "Dandadan Theme",
            "description": "Dynamic Dandadan anime-inspired dark theme",
            "version": "2.0.0",
            "publisher": "misternegative21",
            "engines": {"vscode": "^1.60.0"},
            "categories": ["Themes"],
            "contributes": {
                "themes": [{
                    "label": "Dandadan",
                    "uiTheme": "vs-dark",
                    "path": "./themes/dandadan-color-theme.json"
                }]
            }
        }
        write(f"{ext_dir}/package.json", json.dumps(pkg_json, indent=2))

for user_settings in [
    f"{HOME}/.config/Antigravity IDE/User/settings.json",
    f"{HOME}/.config/Antigravity/User/settings.json",
    f"{HOME}/.config/Code/User/settings.json",
    f"{HOME}/.config/VSCodium/User/settings.json",
    f"{HOME}/.config/Cursor/User/settings.json",
]:
    if os.path.exists(os.path.dirname(user_settings)):
        try:
            st = {}
            if os.path.exists(user_settings):
                try:
                    with open(user_settings, "r") as sf:
                        st = json.load(sf)
                except Exception:
                    st = {}
            st["workbench.colorTheme"] = "Dandadan"
            write(user_settings, json.dumps(st, indent=2))
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
# 12 · GTK — gtk.css (GTK3 & GTK4)
# ══════════════════════════════════════════════════════════════════════════════
gtk_css = f"""/* DANDADAN GTK Theme — Wallpaper {active_idx}: {vibe} */
@define-color accent_color {accent};
@define-color accent_bg_color {accent};
@define-color accent_fg_color #ffffff;
@define-color destructive_color {cursor};
@define-color destructive_bg_color {cursor};
@define-color destructive_fg_color #ffffff;
@define-color success_color {highlight};
@define-color warning_color {ana1};
@define-color error_color {cursor};
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
# Also write to gtk-3.0 and gtk-4.0 subdirs
os.makedirs(f"{THEME_DIR}/gtk-3.0", exist_ok=True)
os.makedirs(f"{THEME_DIR}/gtk-4.0", exist_ok=True)
write(f"{THEME_DIR}/gtk-3.0/gtk.css", f'@import "../gtk.css";\n')
write(f"{THEME_DIR}/gtk-4.0/gtk.css", f'@import "../gtk.css";\n')


# ══════════════════════════════════════════════════════════════════════════════
# 13 · ZED editor
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
            "icon.muted": "#616367",
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
            "background": bg,
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
            "conflict": cursor,
            "conflict.background": with_alpha(cursor, "15"),
            "conflict.border": with_alpha(cursor, "55"),
            "created": highlight,
            "created.background": with_alpha(highlight, "15"),
            "created.border": with_alpha(highlight, "55"),
            "deleted": cursor,
            "deleted.background": with_alpha(cursor, "15"),
            "deleted.border": with_alpha(cursor, "55"),
            "error": cursor,
            "error.background": with_alpha(cursor, "15"),
            "error.border": with_alpha(cursor, "55"),
            "hidden": "#616367",
            "hidden.background": with_alpha(bg_mid, "99"),
            "hidden.border": with_alpha(bg_mid, "99"),
            "hint": with_alpha(fg, "66"),
            "hint.background": with_alpha(bg_mid, "99"),
            "hint.border": with_alpha(bg_mid, "88"),
            "ignored": with_alpha(fg, "44"),
            "ignored.background": with_alpha(bg_mid, "88"),
            "ignored.border": with_alpha(bg_mid, "88"),
            "info": accent_comp,
            "info.background": with_alpha(accent_comp, "15"),
            "info.border": with_alpha(accent_comp, "55"),
            "modified": accent,
            "modified.background": with_alpha(accent, "15"),
            "modified.border": with_alpha(accent, "55"),
            "predictive": with_alpha(highlight, "99"),
            "predictive.background": with_alpha(highlight, "11"),
            "predictive.border": with_alpha(highlight, "33"),
            "renamed": tri1,
            "renamed.background": with_alpha(tri1, "15"),
            "renamed.border": with_alpha(tri1, "55"),
            "success": highlight,
            "success.background": with_alpha(highlight, "15"),
            "success.border": with_alpha(highlight, "55"),
            "unreachable": "#616367",
            "unreachable.background": with_alpha(bg_mid, "99"),
            "unreachable.border": with_alpha(bg_mid, "88"),
            "warning": ana1,
            "warning.background": with_alpha(ana1, "15"),
            "warning.border": with_alpha(ana1, "55"),
            "panel.background": bg + "E0",
            "pane.focused_border": accent,
            "tab_bar.background": bg,
            "tab.inactive_background": bg,
            "tab.active_background": bg_mid,
            "search.match_background": with_alpha(cursor, "44"),
            "title_bar.background": bg,
            "title_bar.inactive_background": bg,
            "toolbar.background": bg_mid,
            "status_bar.background": bg,
            "scrollbar.thumb.background": with_alpha(accent, "33"),
            "scrollbar.thumb.hover_background": with_alpha(accent, "55"),
            "scrollbar.thumb.border": with_alpha(accent, "55"),
            "scrollbar.track.background": "#00000000",
            "scrollbar.track.border": "#00000000",
            "editor.foreground": fg,
            "editor.background": bg + "F0",
            "editor.gutter.background": bg + "F0",
            "editor.active_line.background": with_alpha(accent, "0F"),
            "editor.highlighted_line.background": with_alpha(accent, "15"),
            "editor.line_number": "#616367",
            "editor.active_line_number": accent,
            "editor.invisible": with_alpha(fg, "22"),
            "editor.wrap_guide": with_alpha(fg, "0D"),
            "editor.active_wrap_guide": with_alpha(accent, "33"),
            "editor.document_highlight.read_background": with_alpha(accent, "22"),
            "editor.document_highlight.write_background": with_alpha(cursor, "22"),
            "terminal.background": bg,
            "terminal.foreground": fg,
            "terminal.bright_foreground": "#FFFFFF",
            "terminal.dim_foreground": "#616367",
            "terminal.ansi.black": bg,
            "terminal.ansi.red": cursor,
            "terminal.ansi.green": highlight,
            "terminal.ansi.yellow": ana1,
            "terminal.ansi.blue": tri1,
            "terminal.ansi.magenta": accent,
            "terminal.ansi.cyan": tri2,
            "terminal.ansi.white": fg,
            "terminal.ansi.bright_black": "#616367",
            "terminal.ansi.bright_red": lighten(cursor),
            "terminal.ansi.bright_green": lighten(highlight),
            "terminal.ansi.bright_yellow": lighten(ana1),
            "terminal.ansi.bright_blue": lighten(tri1),
            "terminal.ansi.bright_magenta": lighten(accent),
            "terminal.ansi.bright_cyan": lighten(tri2),
            "terminal.ansi.bright_white": "#FFFFFF",
            "players": [
                {"cursor": cursor, "background": with_alpha(cursor, "22"), "selection": with_alpha(cursor, "33")},
                {"cursor": accent, "background": with_alpha(accent, "22"), "selection": with_alpha(accent, "33")},
                {"cursor": highlight, "background": with_alpha(highlight, "22"), "selection": with_alpha(highlight, "33")},
                {"cursor": tri1, "background": with_alpha(tri1, "22"), "selection": with_alpha(tri1, "33")},
            ],
        }
    }]
}
write_both("zed.json", json.dumps(zed_theme, indent=2))


# ══════════════════════════════════════════════════════════════════════════════
# 14 · WALKER launcher
# ══════════════════════════════════════════════════════════════════════════════
walker_css = f"""/* DANDADAN Walker — Wallpaper {active_idx}: {vibe} */
@define-color selected-text {accent};
@define-color text          {fg};
@define-color base          {bg};
@define-color border        {accent};
@define-color foreground    {fg};
@define-color background    {bg};
@define-color hover         {accent_comp};
@define-color selected-box  {cursor};

* {{
  font-family: 'JetBrainsMono Nerd Font', 'CaskaydiaMono Nerd Font', monospace;
}}

window {{ background: transparent; }}

window .search-container,
window .search {{
  background: alpha(@base, 0.96);
  box-shadow: 0 10px 36px rgba(0,0,0,0.5),
              0 0 0 1px alpha(@border, 0.6);
  color: @foreground;
  border: 2px solid @border;
  border-radius: 14px;
  padding: 8px 18px;
  margin-top: 1px;
  font-size: 14px;
}}

.box-wrapper {{
  background: alpha(@base, 0.96);
  border: 2px solid @border;
  border-radius: 18px;
  box-shadow: 0 14px 44px rgba(0,0,0,0.5),
              0 0 0 1px alpha(@border, 0.4);
  padding: 10px;
}}

child:selected {{
  border-radius: 12px;
  background-color: alpha(@selected-box, 0.20);
  box-shadow: 0 4px 14px rgba(0,0,0,0.25);
  transition: background-color 0.22s cubic-bezier(0.22, 1, 0.36, 1);
}}
child:selected .item-box {{
  transition: transform 0.14s cubic-bezier(0.22, 1, 0.36, 1);
  transform: translateX(4px);
}}
child:selected .item-box * {{ color: @selected-text; }}
child:hover {{ background-color: alpha(@hover, 0.12); }}
"""
write_both("walker.css", walker_css)
os.makedirs(f"{HOME}/.config/walker", exist_ok=True)
write(f"{HOME}/.config/walker/style.css", walker_css)


# ══════════════════════════════════════════════════════════════════════════════
# 15 · WOFI launcher
# ══════════════════════════════════════════════════════════════════════════════
wofi_css = f"""/* DANDADAN Wofi — Wallpaper {active_idx}: {vibe} */
@define-color bg     {bg};
@define-color fg     {fg};
@define-color accent {accent};
@define-color hover  {with_alpha(accent,'22')};
@define-color border {with_alpha(accent,'66')};

window {{
  background-color: alpha(@bg, 0.95);
  border: 2px solid @border;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}}

#input {{
  background-color: alpha(@bg, 0.8);
  color: @fg;
  border: 1px solid @border;
  border-radius: 10px;
  padding: 8px 12px;
  margin: 8px;
  font-size: 14px;
}}

#input:focus {{ border-color: {accent}; }}

#inner-box {{
  background-color: transparent;
  margin: 4px;
}}

#outer-box {{
  padding: 6px;
  background: transparent;
}}

#entry {{
  color: @fg;
  background-color: transparent;
  padding: 6px 10px;
  margin: 2px 4px;
  border-radius: 10px;
}}

#entry:selected {{
  background-color: @hover;
  color: {accent};
  box-shadow: inset 0 0 0 1px {with_alpha(accent,'55')};
}}

#text {{ color: @fg; }}
#text:selected {{ color: {accent}; font-weight: bold; }}

scrollbar {{ background-color: transparent; }}
scrollbar slider {{
  background-color: {with_alpha(accent,'44')};
  border-radius: 6px;
}}
scrollbar slider:hover {{ background-color: {with_alpha(accent,'77')}; }}
"""
write_both("wofi.css", wofi_css)
# Deploy to live wofi config
os.makedirs(f"{HOME}/.config/wofi", exist_ok=True)
write(f"{HOME}/.config/wofi/style.css", wofi_css)


# ══════════════════════════════════════════════════════════════════════════════
# 16 · WARP terminal theme
# ══════════════════════════════════════════════════════════════════════════════
warp_yaml = f"""# DANDADAN Warp Theme — Wallpaper {active_idx}: {vibe}
name: Dandadan
accent: "{accent}"
cursor: "{cursor}"
background: "{bg}"
foreground: "{fg}"
details: darker

terminal_colors:
  normal:
    black:   "{bg}"
    red:     "{cursor}"
    green:   "{highlight}"
    yellow:  "{ana1}"
    blue:    "{tri1}"
    magenta: "{accent}"
    cyan:    "{tri2}"
    white:   "{fg}"
  bright:
    black:   "#616367"
    red:     "{lighten(cursor)}"
    green:   "{lighten(highlight)}"
    yellow:  "{lighten(ana1)}"
    blue:    "{lighten(tri1)}"
    magenta: "{lighten(accent)}"
    cyan:    "{lighten(tri2)}"
    white:   "#FFFFFF"
"""
write_both("warp.yaml", warp_yaml)
# Deploy to warp themes
os.makedirs(f"{HOME}/.local/share/warp-terminal/themes", exist_ok=True)
write(f"{HOME}/.local/share/warp-terminal/themes/dandadan.yaml", warp_yaml)


# ══════════════════════════════════════════════════════════════════════════════
# 17 · ZELLIJ terminal multiplexer
# ══════════════════════════════════════════════════════════════════════════════
zellij_theme = f"""# DANDADAN Zellij — Wallpaper {active_idx}: {vibe}
themes:
  dandadan:
    fg: "{fg}"
    bg: "{bg}"
    black: "{bg}"
    red: "{cursor}"
    green: "{highlight}"
    yellow: "{ana1}"
    blue: "{tri1}"
    magenta: "{accent}"
    cyan: "{tri2}"
    white: "{fg}"
    orange: "{ana2}"
"""
write_both("zellij.kdl", f"""// DANDADAN Zellij Theme — Wallpaper {active_idx}: {vibe}
themes {{
    dandadan {{
        fg "{fg}"
        bg "{bg}"
        black "{bg}"
        red "{cursor}"
        green "{highlight}"
        yellow "{ana1}"
        blue "{tri1}"
        magenta "{accent}"
        cyan "{tri2}"
        white "{fg}"
        orange "{ana2}"
    }}
}}
""")
os.makedirs(f"{HOME}/.config/zellij/themes", exist_ok=True)
write(f"{HOME}/.config/zellij/themes/dandadan.kdl",
f"""// DANDADAN Zellij Theme — Wallpaper {active_idx}: {vibe}
themes {{
    dandadan {{
        fg "{fg}"
        bg "{bg}"
        black "{bg}"
        red "{cursor}"
        green "{highlight}"
        yellow "{ana1}"
        blue "{tri1}"
        magenta "{accent}"
        cyan "{tri2}"
        white "{fg}"
        orange "{ana2}"
    }}
}}
""")


# ══════════════════════════════════════════════════════════════════════════════
# 18 · VENCORD / Vesktop Discord
# ══════════════════════════════════════════════════════════════════════════════
vencord_css = f"""/**
 * @name Dandadan
 * @description Dynamic Dandadan theme — Wallpaper {active_idx}: {vibe}
 * @version 1.0.0
 * @author misternegative21
*/
@import url("https://refact0r.github.io/system24/build/system24.css");

body {{
    --font: "JetBrainsMono Nerd Font";
    --code-font: "JetBrainsMono Nerd Font";
    font-weight: 400;
    letter-spacing: -0.02ch;

    --gap: 12px;
    --divider-thickness: 3px;
    --border-thickness: 2px;
    --border-hover-transition: 0.2s ease;
    --animations: on;
    --list-item-transition: 0.2s ease;

    --top-bar-height: var(--gap);
    --top-bar-button-position: titlebar;
    --top-bar-title-position: off;
    --colors: on;

    /* ── Dandadan palette ─────────────────────────────────── */
    --text-0: {fg};
    --text-1: {fg};
    --text-2: {with_alpha(fg,'DD')};
    --text-3: {with_alpha(fg,'BB')};
    --text-4: {with_alpha(fg,'88')};
    --text-5: #616367;

    --bg-1: {darken(bg_mid)};
    --bg-2: {bg_mid};
    --bg-3: {bg};
    --bg-4: {darken(bg, 0.85)};

    --accent-1: {accent};
    --accent-2: {darken(accent)};
    --accent-3: {accent};
    --accent-4: {darken(accent, 0.8)};
    --accent-5: {darken(accent, 0.7)};

    --mention: linear-gradient(to right, {with_alpha(accent,'22')} 40%, transparent);
    --mention-hover: linear-gradient(to right, {with_alpha(accent,'33')} 40%, transparent);
    --reply: linear-gradient(to right, {with_alpha(highlight,'22')} 40%, transparent);
    --reply-hover: linear-gradient(to right, {with_alpha(highlight,'33')} 40%, transparent);

    --border-light: {with_alpha(accent,'33')};
    --border: {with_alpha(accent,'55')};
    --border-hover: {with_alpha(accent,'88')};
    --active: {with_alpha(accent,'22')};
    --hover: {with_alpha(accent,'15')};
    --selected: {with_alpha(accent,'22')};

    --header-primary: {fg};
    --header-secondary: {with_alpha(fg,'BB')};
    --interactive-normal: {fg};
    --interactive-hover: {accent};
    --interactive-active: {accent};
    --interactive-muted: #616367;

    --background-primary: {bg};
    --background-secondary: {bg_mid};
    --background-secondary-alt: {bg_mid2};
    --background-tertiary: {darken(bg, 0.85)};
    --background-accent: {with_alpha(accent,'22')};
    --background-message-hover: {with_alpha(accent,'08')};

    --brand-experiment: {accent};
    --brand-experiment-100: {with_alpha(accent,'1A')};
    --brand-experiment-200: {with_alpha(accent,'33')};
    --brand-experiment-300: {with_alpha(accent,'4D')};
    --brand-experiment-400: {with_alpha(accent,'66')};
    --brand-experiment-500: {accent};
    --brand-experiment-600: {darken(accent, 0.85)};

    --status-positive-text: {highlight};
    --status-warning-text: {ana1};
    --status-danger-text: {cursor};

    --scrollbar-thin-thumb: {with_alpha(accent,'44')};
    --scrollbar-auto-thumb: {with_alpha(accent,'55')};
    --scrollbar-auto-track: transparent;
}}
"""
write_both("vencord.theme.css", vencord_css)
# Deploy to Vesktop if it exists
for vesktop_path in [
    f"{HOME}/.config/vesktop/themes",
    f"{HOME}/.var/app/dev.vencord.Vesktop/config/vesktop/themes",
]:
    if os.path.isdir(os.path.dirname(vesktop_path)):
        os.makedirs(vesktop_path, exist_ok=True)
        write(f"{vesktop_path}/dandadan.theme.css", vencord_css)


# ══════════════════════════════════════════════════════════════════════════════
# 19 · CHROMIUM / Brave / Vivaldi / Chrome
# ══════════════════════════════════════════════════════════════════════════════
chrom_rgb = hex_to_rgb_str(cursor)
for p in [f"{THEME_DIR}/chromium.theme", f"{CURR_DIR}/chromium.theme"]:
    write(p, f"{chrom_rgb}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 20 · FIREFOX / Zen Browser
# ══════════════════════════════════════════════════════════════════════════════
firefox_css = f"""/* DANDADAN Firefox/Zen — Wallpaper {active_idx}: {vibe} */
:root {{
  --lwt-accent-color: {accent};
  --lwt-toolbar-field-focus: {cursor};
  --toolbar-field-border-color: {cursor};
  --toolbar-field-background-color: {bg};
  --toolbar-field-color: {fg};
  --lwt-tab-text: {fg};
  --lwt-selected-tab-background-color: {cursor};
  --tab-line-color: {accent};
}}
"""
write_both("firefox.css", firefox_css)


# ══════════════════════════════════════════════════════════════════════════════
# 21 · TELEGRAM palette
# ══════════════════════════════════════════════════════════════════════════════
telegram = f"""// DANDADAN Telegram — Wallpaper {active_idx}: {vibe}
windowBg: {bg};
windowFg: {fg};
windowBgOver: {bg_mid};
windowBgRipple: {bg_mid2};
windowFgActive: #FFFFFF;
activeButtonBg: {cursor};
activeButtonBgOver: {darken(cursor)};
activeButtonBgRipple: {accent};
activeButtonFg: #FFFFFF;
dialogsBg: {bg};
dialogsNameFg: {fg};
dialogsChatIconFg: {accent};
dialogsDateFg: #616367;
dialogsTextFg: #A0A5B5;
dialogsTextFgService: {accent};
dialogsUnreadBg: {cursor};
dialogsUnreadBgMuted: #616367;
dialogsUnreadFg: #FFFFFF;
msgInBg: {bg_mid};
msgInBgSelected: {bg_mid2};
msgInFg: {fg};
msgInDateFg: #A0A5B5;
msgOutBg: {cursor};
msgOutBgSelected: {darken(cursor)};
msgOutFg: #FFFFFF;
msgOutDateFg: {with_alpha(fg,'BB')};
historyTextInFg: {fg};
historyTextOutFg: #FFFFFF;
historyLinkInFg: {accent};
historyLinkOutFg: #FFFFFF;
sideBarBg: {bg};
sideBarTextFg: {fg};
sideBarIconFg: {accent};
"""
write_both("telegram.palette", telegram)


# ══════════════════════════════════════════════════════════════════════════════
# 22 · NEOVIM colorscheme (dynamic via lua variable)
# ══════════════════════════════════════════════════════════════════════════════
neovim_lua = f"""-- DANDADAN Neovim — Wallpaper {active_idx}: {vibe}
-- Uses sunset-drive as base; overrides accent colors dynamically
return {{
    {{ "tahayvr/sunset-drive.nvim", lazy = false, priority = 1000 }},
    {{
        "LazyVim/LazyVim",
        opts = {{
            colorscheme = "sunsetdrive",
        }},
    }},
    -- Optional: override highlights for per-wallpaper accent
    {{
        "LazyVim/LazyVim",
        opts = function(_, opts)
            vim.api.nvim_set_hl(0, "Normal",        {{ bg = "{bg}",     fg = "{fg}"  }})
            vim.api.nvim_set_hl(0, "Visual",        {{ bg = "{with_alpha(accent,'44')}" }})
            vim.api.nvim_set_hl(0, "Search",        {{ bg = "{with_alpha(cursor,'55')}", fg = "#FFFFFF" }})
            vim.api.nvim_set_hl(0, "CursorLine",    {{ bg = "{bg_mid}" }})
            vim.api.nvim_set_hl(0, "StatusLine",    {{ bg = "{accent}",    fg = "#FFFFFF" }})
            vim.api.nvim_set_hl(0, "StatusLineNC",  {{ bg = "{bg_mid}",    fg = "#616367" }})
            vim.api.nvim_set_hl(0, "TabLineSel",    {{ bg = "{accent}",    fg = "#FFFFFF" }})
            vim.api.nvim_set_hl(0, "TabLine",       {{ bg = "{bg}",        fg = "#616367" }})
            vim.api.nvim_set_hl(0, "WinSeparator",  {{ fg = "{with_alpha(accent,'66')}" }})
            vim.api.nvim_set_hl(0, "FloatBorder",   {{ fg = "{accent}" }})
            vim.api.nvim_set_hl(0, "DiagnosticError",   {{ fg = "{cursor}"    }})
            vim.api.nvim_set_hl(0, "DiagnosticWarn",    {{ fg = "{ana1}"      }})
            vim.api.nvim_set_hl(0, "DiagnosticInfo",    {{ fg = "{accent_comp}" }})
            vim.api.nvim_set_hl(0, "DiagnosticHint",    {{ fg = "{highlight}" }})
            vim.api.nvim_set_hl(0, "TelescopeSelection", {{ bg = "{with_alpha(accent,'33')}", fg = "{fg}" }})
            vim.api.nvim_set_hl(0, "TelescopeBorder",    {{ fg = "{accent}" }})
            vim.api.nvim_set_hl(0, "TelescopePromptBorder", {{ fg = "{cursor}" }})
        end,
    }},
}}
"""
write_both("neovim.lua", neovim_lua)


# ══════════════════════════════════════════════════════════════════════════════
# 23 · COLORS.TOML (generic omarchy palette)
# ══════════════════════════════════════════════════════════════════════════════
colors_toml = f"""# DANDADAN Colors — Wallpaper {active_idx}: {vibe}
accent     = "{accent}"
cursor     = "{cursor}"
foreground = "{fg}"
background = "{bg}"
selection_foreground = "{fg}"
selection_background = "{with_alpha(accent,'66')}"

color0  = "{bg}"
color1  = "{cursor}"
color2  = "{highlight}"
color3  = "{ana1}"
color4  = "{tri1}"
color5  = "{accent}"
color6  = "{tri2}"
color7  = "{fg}"
color8  = "#616367"
color9  = "{lighten(cursor)}"
color10 = "{lighten(highlight)}"
color11 = "{lighten(ana1)}"
color12 = "{lighten(tri1)}"
color13 = "{lighten(accent)}"
color14 = "{lighten(tri2)}"
color15 = "#FFFFFF"
"""
write_both("colors.toml", colors_toml)


# ══════════════════════════════════════════════════════════════════════════════
# 24 · ICONS selection (keep Yaru accent from palette)
# ══════════════════════════════════════════════════════════════════════════════
# Pick icon theme based on dominant hue
r0, g0, b0 = h2r(accent)
h0, s0, v0 = colorsys.rgb_to_hsv(r0/255, g0/255, b0/255)
# Map hue to Yaru color variants
if 0.95 <= h0 or h0 < 0.05:      icon_color = "red"
elif 0.05 <= h0 < 0.12:           icon_color = "orange"
elif 0.12 <= h0 < 0.20:           icon_color = "yellow"
elif 0.20 <= h0 < 0.42:           icon_color = "green"
elif 0.42 <= h0 < 0.55:           icon_color = "cyan"
elif 0.55 <= h0 < 0.68:           icon_color = "blue"
elif 0.68 <= h0 < 0.78:           icon_color = "purple"
elif 0.78 <= h0 < 0.88:           icon_color = "magenta"
elif 0.88 <= h0 < 0.95:           icon_color = "red"
else:                              icon_color = "red"

write_both("icons.theme", f"Yaru-{icon_color}\n")


# ══════════════════════════════════════════════════════════════════════════════
# Live triggers
# ══════════════════════════════════════════════════════════════════════════════
subprocess.run(["omarchy-theme-set-browser"], capture_output=True)
subprocess.run(["pkill", "-SIGUSR2", "waybar"], capture_output=True)

# Reload mako
subprocess.run(["makoctl", "reload"], capture_output=True)

print(f"\n✓ All 21 targets updated for wallpaper {active_idx}: {vibe}")
print(f"  Wallpaper pool: 52 images (001-058 with gaps)")
print(f"  accent={accent}  comp={accent_comp}  cursor={cursor}")
print(f"  highlight={highlight}  tri1={tri1}  tri2={tri2}")
print(f"  icon-theme=Yaru-{icon_color}")
