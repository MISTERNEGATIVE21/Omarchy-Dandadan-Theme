#!/bin/bash
# Dandadan Theme — Shell Auto-Detection Engine
# Detects whether the current environment uses Quickshell (Omarchy 4.0+), Waybar, dual, or none.
# Priority: Quickshell > Waybar

is_quickshell_running() {
  pgrep -x quickshell >/dev/null 2>&1 || \
  pgrep -f "quickshell.*omarchy" >/dev/null 2>&1 || \
  pgrep -f "omarchy-shell" >/dev/null 2>&1
}

is_waybar_running() {
  pgrep -x waybar >/dev/null 2>&1
}

detect_shell() {
  local has_quickshell=0
  local has_waybar=0
  local primary_only=0

  if [[ "$1" == "--primary" || "$1" == "--mode=primary" ]]; then
    primary_only=1
  fi

  # Check running processes
  if is_quickshell_running; then
    has_quickshell=1
  fi

  if is_waybar_running; then
    has_waybar=1
  fi

  # If neither process is actively running, check system installation & Omarchy version
  if (( !has_quickshell && !has_waybar )); then
    if command -v quickshell >/dev/null 2>&1 || \
       command -v omarchy-shell >/dev/null 2>&1 || \
       [[ -d "/usr/share/omarchy/shell" ]] || \
       [[ -d "$HOME/.local/state/omarchy" ]] || \
       [[ -f "/usr/share/omarchy/version" && $(cat /usr/share/omarchy/version 2>/dev/null) =~ ^4\. ]]; then
      has_quickshell=1
    fi
    if command -v waybar >/dev/null 2>&1; then
      has_waybar=1
    fi
  fi

  if (( has_quickshell && has_waybar )); then
    if (( primary_only )); then
      echo "quickshell"
    else
      echo "dual"
    fi
  elif (( has_quickshell )); then
    echo "quickshell"
  elif (( has_waybar )); then
    echo "waybar"
  else
    echo "none"
  fi
}

# Execute main function if run as script rather than sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  detect_shell "$@"
fi
