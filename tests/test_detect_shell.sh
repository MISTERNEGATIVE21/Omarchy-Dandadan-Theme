#!/bin/bash
set -e

# Test 1: Script exists and is executable
if [[ ! -x "scripts/detect_shell.sh" ]]; then
  echo "FAIL: scripts/detect_shell.sh is not executable"
  exit 1
fi

# Test 2: Execution produces valid output token
OUTPUT=$(./scripts/detect_shell.sh)
if [[ "$OUTPUT" != "quickshell" && "$OUTPUT" != "waybar" && "$OUTPUT" != "dual" && "$OUTPUT" != "none" ]]; then
  echo "FAIL: Unexpected output '$OUTPUT'"
  exit 1
fi

echo "PASS: test_detect_shell.sh passed (Detected: $OUTPUT)"
