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
