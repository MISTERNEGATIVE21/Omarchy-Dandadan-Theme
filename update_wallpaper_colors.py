#!/usr/bin/env python3
import json, os, sys, subprocess

theme_dir = "/home/mister/.config/omarchy/themes/dandadan"
manifest_path = os.path.join(theme_dir, "wallpaper_highlights.json")
wallpapers_css_path = os.path.join(theme_dir, "wallpapers.css")
current_bg_link = os.path.expanduser("~/.config/omarchy/current/background")

if not os.path.exists(manifest_path):
    sys.exit(0)

with open(manifest_path, "r") as f:
    data = json.load(f)

active_idx = "19"
if os.path.islink(current_bg_link) or os.path.exists(current_bg_link):
    target = os.readlink(current_bg_link) if os.path.islink(current_bg_link) else current_bg_link
    base = os.path.basename(target)
    idx = base.split(".")[0].zfill(2)
    if idx in data:
        active_idx = idx

colors = data.get(active_idx, data["19"])
accent = colors.get("accent", "#D8B3FE")
cursor = colors.get("border", colors.get("glow", "#E1477A"))
highlight = colors.get("highlight", "#E8759B")
bg = colors.get("background", "#14161E")
fg = colors.get("foreground", "#F0F4FC")

css_content = f"""/* Dynamic Wallpaper Highlight Colors (Wallpaper {active_idx} - {colors.get("vibe", "")}) */
@define-color background {bg};
@define-color foreground {fg};
@define-color accent {accent};
@define-color cursor {cursor};
@define-color highlight {highlight};
"""

# Write to theme dir wallpapers.css
with open(wallpapers_css_path, "w") as f:
    f.write(css_content)

# Write to active theme wallpapers.css
current_theme_wallpapers = os.path.expanduser("~/.config/omarchy/current/theme/wallpapers.css")
if os.path.exists(os.path.dirname(current_theme_wallpapers)):
    with open(current_theme_wallpapers, "w") as f:
        f.write(css_content)

# Write to waybar dir wallpapers.css
waybar_wallpapers = os.path.expanduser("~/.config/waybar/wallpapers.css")
with open(waybar_wallpapers, "w") as f:
    f.write(css_content)

# Update Hyprland active border colors dynamically
try:
    c1 = cursor.replace("#", "")
    c2 = accent.replace("#", "")
    subprocess.run(["hyprctl", "keyword", "general:col.active_border", f"rgb({c1}) rgb({c2}) 45deg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
    pass

# Signal Waybar to reload CSS
subprocess.run(["pkill", "-SIGUSR2", "waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
