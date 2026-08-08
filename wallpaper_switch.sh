#!/usr/bin/env bash
set -e

THEME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BG_DIR="${THEME_DIR}/backgrounds"
HIGHLIGHTS_JSON="${THEME_DIR}/wallpaper_highlights.json"
WAYBAR_CSS="${THEME_DIR}/waybar.css"
HYPR_CONF="${THEME_DIR}/hyprland.conf"
SYMLINK_PATH="/home/mister/.config/omarchy/current/background"

INPUT="$1"

if [[ -z "$INPUT" ]]; then
    echo "Usage: $0 <01-39|random>" >&2
    exit 1
fi

if [[ "${INPUT,,}" == "random" ]]; then
    RAND_NUM=$(( (RANDOM % 39) + 1 ))
    INDEX=$(printf "%02d" "$RAND_NUM")
else
    if [[ "$INPUT" =~ ^[0-9]+$ ]]; then
        NUM=$((10#$INPUT))
        if (( NUM >= 1 && NUM <= 39 )); then
            INDEX=$(printf "%02d" "$NUM")
        else
            echo "Error: Wallpaper index must be between 01 and 39 (got: '$INPUT')" >&2
            exit 1
        fi
    else
        echo "Error: Invalid argument '$INPUT'. Expected 01..39 or 'random'." >&2
        exit 1
    fi
fi

TARGET_BG="${BG_DIR}/${INDEX}.webp"

if [[ ! -f "$TARGET_BG" ]]; then
    echo "Error: Background file not found: $TARGET_BG" >&2
    exit 1
fi

# 1. Update symlink
mkdir -p "$(dirname "$SYMLINK_PATH")"
ln -nsf "$TARGET_BG" "$SYMLINK_PATH"

# 2. Update swaybg if running
if pgrep -x swaybg >/dev/null 2>&1; then
    pkill -x swaybg 2>/dev/null || true
    setsid swaybg -i "$SYMLINK_PATH" -m fill >/dev/null 2>&1 &
fi

# 3. Update waybar.css and hyprland.conf using Python
python3 - "$INDEX" "$HIGHLIGHTS_JSON" "$WAYBAR_CSS" "$HYPR_CONF" << 'EOF'
import sys, json, re

index = sys.argv[1]
highlights_path = sys.argv[2]
waybar_css_path = sys.argv[3]
hypr_conf_path = sys.argv[4]

with open(highlights_path, 'r') as f:
    highlights = json.load(f)

if index not in highlights:
    print(f"Error: Index '{index}' not found in highlights JSON", file=sys.stderr)
    sys.exit(1)

item = highlights[index]
accent = item["accent"]
highlight = item["highlight"]
bg = item["background"]
fg = item["foreground"]
border = item["border"]
glow = item["glow"]
vibe = item.get("vibe", "")

# Update waybar.css
new_waybar_block = f"""/* Active Wallpaper Class: .wallpaper-{index} ({vibe}) */
#waybar,
.wallpaper-{index} {{
  --wp-accent: {accent};
  --wp-highlight: {highlight};
  --wp-bg: {bg};
  --wp-fg: {fg};
  --wp-border: {border};
  --wp-glow: {glow};
}}"""

with open(waybar_css_path, 'r') as f:
    css_content = f.read()

pattern = r"/\* (?:Default|Active) Wallpaper Class:.*?\*/\n#waybar,\n\.wallpaper-\d+ \{[^}]*\}"
if re.search(pattern, css_content, re.DOTALL):
    css_updated = re.sub(pattern, new_waybar_block, css_content, flags=re.DOTALL)
else:
    css_updated = css_content

with open(waybar_css_path, 'w') as f:
    f.write(css_updated)

# Update hyprland.conf
highlight_clean = highlight.lstrip('#')
accent_clean = accent.lstrip('#')

with open(hypr_conf_path, 'r') as f:
    hypr_content = f.read()

new_border_line = f"    col.active_border = rgb({highlight_clean}) rgb({accent_clean}) 45deg"
hypr_updated = re.sub(r"^\s*col\.active_border\s*=.*$", new_border_line, hypr_content, flags=re.MULTILINE)

with open(hypr_conf_path, 'w') as f:
    f.write(hypr_updated)

print(f"Updated waybar.css and hyprland.conf for wallpaper {index} ({vibe})")
EOF

# 4. Trigger Waybar reload
if pgrep -x waybar >/dev/null 2>&1; then
    pkill -SIGUSR2 waybar 2>/dev/null || killall -SIGUSR2 waybar 2>/dev/null || omarchy-restart-waybar >/dev/null 2>&1 || true
fi

# 5. Trigger Hyprland reload
if command -v hyprctl >/dev/null 2>&1; then
    hyprctl reload >/dev/null 2>&1 || true
fi

echo "Successfully set wallpaper ${INDEX}.webp (/home/mister/.config/omarchy/current/background) and reloaded Waybar / Hyprland."
