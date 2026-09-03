#!/bin/bash
# Dandadan Theme — Live Wallpaper Change Watcher
# Automatically recolors Quickshell and all 21 desktop targets when wallpaper changes.

CURRENT_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/omarchy/current"
THEME_DIR="$HOME/.config/omarchy/themes/dandadan-theme"
SCRIPT="$THEME_DIR/update_wallpaper_colors.py"

# Prevent duplicate instances
PIDFILE="${XDG_RUNTIME_DIR:-/tmp}/dandadan-bg-watch.pid"
if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE" 2>/dev/null)" 2>/dev/null; then
  exit 0
fi
echo "$$" > "$PIDFILE"
trap 'rm -f "$PIDFILE"; exit 0' SIGINT SIGTERM EXIT

last_bg=""

recolor_if_dandadan() {
  local theme_name=""
  if [[ -f "$CURRENT_DIR/theme.name" ]]; then
    theme_name=$(cat "$CURRENT_DIR/theme.name" 2>/dev/null)
  elif [[ -f "$HOME/.config/omarchy/current/theme.name" ]]; then
    theme_name=$(cat "$HOME/.config/omarchy/current/theme.name" 2>/dev/null)
  fi

  # Only process if Dandadan theme is currently active
  if [[ "$theme_name" != "dandadan" && "$theme_name" != "dandadan-theme" ]]; then
    return 0
  fi

  local current_bg=""
  if [[ -e "$CURRENT_DIR/background" ]]; then
    current_bg=$(readlink -f "$CURRENT_DIR/background" 2>/dev/null)
  fi

  if [[ -n "$current_bg" && "$current_bg" != "$last_bg" ]]; then
    last_bg="$current_bg"
    if [[ -f "$SCRIPT" ]]; then
      python3 "$SCRIPT" >/dev/null 2>&1
    fi
  fi
}

# Initial trigger
recolor_if_dandadan

# Event-driven watcher via inotifywait with poll fallback
if command -v inotifywait >/dev/null 2>&1 && [[ -d "$CURRENT_DIR" ]]; then
  while inotifywait -q -e create,moved_to,attrib "$CURRENT_DIR" >/dev/null 2>&1; do
    sleep 0.15 # Brief debounce for atomic symlink creation/replacement
    recolor_if_dandadan
  done
else
  while true; do
    sleep 1
    recolor_if_dandadan
  done
fi
