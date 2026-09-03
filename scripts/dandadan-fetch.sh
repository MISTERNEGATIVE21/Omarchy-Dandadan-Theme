#!/bin/bash
CONFIG_PATH="$HOME/.local/state/omarchy/current/theme/fastfetch/config.jsonc"
if [[ ! -f "$CONFIG_PATH" ]]; then
  CONFIG_PATH="$(dirname "$(dirname "$(realpath "$0")")")/fastfetch/config.jsonc"
fi

if [[ -f "$CONFIG_PATH" ]]; then
  fastfetch -c "$CONFIG_PATH" "$@"
else
  fastfetch "$@"
fi
