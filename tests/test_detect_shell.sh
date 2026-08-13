#!/bin/bash
set -e

SCRIPT_PATH="scripts/detect_shell.sh"

# Test 1: Script exists and is executable
if [[ ! -x "$SCRIPT_PATH" ]]; then
  echo "FAIL: $SCRIPT_PATH is not executable"
  exit 1
fi

# Test 2: Execution produces valid output token
OUTPUT=$(./"$SCRIPT_PATH")
if [[ "$OUTPUT" != "quickshell" && "$OUTPUT" != "waybar" && "$OUTPUT" != "dual" && "$OUTPUT" != "none" ]]; then
  echo "FAIL: Unexpected output '$OUTPUT'"
  exit 1
fi
echo "Subtest 2 PASS: Basic execution output = $OUTPUT"

# Test 3: Sourcing script exposes functions
source ./"$SCRIPT_PATH"
if ! declare -f is_quickshell_running >/dev/null || ! declare -f is_waybar_running >/dev/null || ! declare -f detect_shell >/dev/null; then
  echo "FAIL: Helper functions not exposed when sourced"
  exit 1
fi
echo "Subtest 3 PASS: Sourced functions available"

# Test 4: Mocked environment logic tests
# Test 4a: Dual detection when both are running
is_quickshell_running() { return 0; }
is_waybar_running() { return 0; }

RESULT=$(detect_shell)
if [[ "$RESULT" != "dual" ]]; then
  echo "FAIL: Expected 'dual' when both are running, got '$RESULT'"
  exit 1
fi

RESULT_PRIMARY=$(detect_shell --primary)
if [[ "$RESULT_PRIMARY" != "quickshell" ]]; then
  echo "FAIL: Expected 'quickshell' for --primary when both running, got '$RESULT_PRIMARY'"
  exit 1
fi
echo "Subtest 4a PASS: Dual process detection and --primary flag"

# Test 4b: Only quickshell running
is_quickshell_running() { return 0; }
is_waybar_running() { return 1; }

RESULT=$(detect_shell)
if [[ "$RESULT" != "quickshell" ]]; then
  echo "FAIL: Expected 'quickshell' when only quickshell running, got '$RESULT'"
  exit 1
fi
echo "Subtest 4b PASS: Quickshell only process detection"

# Test 4c: Only waybar running
is_quickshell_running() { return 1; }
is_waybar_running() { return 0; }

RESULT=$(detect_shell)
if [[ "$RESULT" != "waybar" ]]; then
  echo "FAIL: Expected 'waybar' when only waybar running, got '$RESULT'"
  exit 1
fi
echo "Subtest 4c PASS: Waybar only process detection"

# Test 4d: Fallback installation checks (neither running)
is_quickshell_running() { return 1; }
is_waybar_running() { return 1; }

# Mock state dir fallback
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

HOME="$TEST_DIR"
mkdir -p "$HOME/.local/state/omarchy"

# Override command check to ensure waybar is not found
command() {
  if [[ "$2" == "waybar" ]]; then
    return 1
  fi
  builtin command "$@"
}

RESULT=$(detect_shell)
if [[ "$RESULT" != "quickshell" ]]; then
  echo "FAIL: Expected 'quickshell' via state dir fallback, got '$RESULT'"
  exit 1
fi
echo "Subtest 4d PASS: State dir installation fallback"

echo "PASS: test_detect_shell.sh passed (Detected: $OUTPUT)"
