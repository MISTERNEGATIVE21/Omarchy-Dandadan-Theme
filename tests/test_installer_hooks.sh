#!/bin/bash
set -e

echo "=== Running Installer & Hooks Test Suite ==="

# Test 1: Bash syntax check on install.sh
bash -n install.sh
echo "PASS: install.sh syntax valid"

# Test 2: Verify installer includes quickshell detection and path handling
grep -q "detect_shell.sh" install.sh || grep -q "quickshell" install.sh
grep -q "shell.json" install.sh

echo "PASS: install.sh includes Quickshell and shell detection integration"

# Test 3: Generate hooks into temporary directory and verify syntax
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

HOOKS_DIR="$TMP_DIR/hooks" ./install.sh --hooks-only >/dev/null

bash -n "$TMP_DIR/hooks/theme-set"
echo "PASS: generated theme-set hook syntax valid"

bash -n "$TMP_DIR/hooks/bg-set"
echo "PASS: generated bg-set hook syntax valid"

grep -q "shell.json" "$TMP_DIR/hooks/theme-set"
grep -q "waybar_config.jsonc" "$TMP_DIR/hooks/theme-set"
grep -q "dandadan-music" "$TMP_DIR/hooks/theme-set"
grep -q "dandadan-bg-watch" "$TMP_DIR/hooks/theme-set"
grep -q "fastfetch" "$TMP_DIR/hooks/theme-set"
grep -q "update_wallpaper_colors.py" "$TMP_DIR/hooks/bg-set"
echo "PASS: generated hooks contain expected Quickshell, Waybar, music & anime deactivation logic"

echo "ALL TESTS PASSED."
