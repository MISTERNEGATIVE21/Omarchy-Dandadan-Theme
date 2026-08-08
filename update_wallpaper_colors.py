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

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return f"{int(hex_code[0:2], 16)},{int(hex_code[2:4], 16)},{int(hex_code[4:6], 16)}"

# 1. Update GTK CSS wallpapers.css
css_content = f"""/* Dynamic Wallpaper Highlight Colors (Wallpaper {active_idx} - {colors.get("vibe", "")}) */
@define-color background {bg};
@define-color foreground {fg};
@define-color accent {accent};
@define-color cursor {cursor};
@define-color highlight {highlight};
"""

for p in [wallpapers_css_path,
          os.path.expanduser("~/.config/omarchy/current/theme/wallpapers.css"),
          os.path.expanduser("~/.config/waybar/wallpapers.css")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w") as f:
            f.write(css_content)

# 2. Update Telegram Desktop Palette
telegram_content = f"""// DANDADAN Dynamic Telegram Desktop Theme Palette (Wallpaper {active_idx})
windowBg: {bg};
windowFg: {fg};
windowBgOver: #1D212F;
windowBgRipple: #2A2F42;
windowFgActive: #FFFFFF;

activeButtonBg: {cursor};
activeButtonBgOver: {highlight};
activeButtonBgRipple: {cursor};
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

msgInBg: #1E2230;
msgInBgSelected: #2A2F42;
msgInFg: {fg};
msgInDateFg: #A0A5B5;

msgOutBg: {cursor};
msgOutBgSelected: {highlight};
msgOutFg: #FFFFFF;
msgOutDateFg: #FCE4EC;

historyTextInFg: {fg};
historyTextOutFg: #FFFFFF;
historyLinkInFg: {accent};
historyLinkOutFg: #FFFFFF;

sideBarBg: {bg};
sideBarTextFg: {fg};
sideBarIconFg: {accent};
"""

for p in [os.path.join(theme_dir, "telegram.palette"),
          os.path.expanduser("~/.config/omarchy/current/theme/telegram.palette")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w") as f:
            f.write(telegram_content)

# 3. Update Chromium / Brave / Vivaldi / Chrome Theme Config (RGB format: r,g,b)
chrom_rgb = hex_to_rgb(cursor)
for p in [os.path.join(theme_dir, "chromium.theme"),
          os.path.expanduser("~/.config/omarchy/current/theme/chromium.theme")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w") as f:
            f.write(f"{chrom_rgb}\n")

# 4. Update Firefox / Zen Browser User CSS
firefox_content = f"""/* DANDADAN Dynamic Firefox / Zen Browser CSS (Wallpaper {active_idx}) */
:root {{
  --lwt-accent-color: {accent};
  --lwt-toolbar-field-focus: {cursor};
  --toolbar-field-border-color: {cursor};
  --toolbar-field-background-color: {bg};
  --toolbar-field-color: {fg};
  --lwt-tab-text: {fg};
  --lwt-selected-tab-background-color: {cursor};
}}
"""
for p in [os.path.join(theme_dir, "firefox.css"),
          os.path.expanduser("~/.config/omarchy/current/theme/firefox.css")]:
    if os.path.exists(os.path.dirname(p)):
        with open(p, "w") as f:
            f.write(firefox_content)

# 5. Update Hyprland active border colors dynamically
try:
    c1 = cursor.replace("#", "")
    c2 = accent.replace("#", "")
    subprocess.run(["hyprctl", "keyword", "general:col.active_border", f"rgb({c1}) rgb({c2}) 45deg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception:
    pass

# 6. Trigger Omarchy Browser Theme Sync & Waybar CSS Reload
subprocess.run(["omarchy-theme-set-browser"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["pkill", "-SIGUSR2", "waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
