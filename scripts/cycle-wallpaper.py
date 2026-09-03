#!/usr/bin/env python3
"""
Dandadan Wallpaper Cycler & Selector
Provides 'next', 'prev', 'random', and 'set <idx>' functionality for Dandadan theme.
Integrates with Omarchy's background system and triggers dynamic recoloring.
"""

import os
import sys
import glob
import json
import random
import subprocess

HOME = os.path.expanduser("~")
CURRENT_THEME_DIR = f"{HOME}/.local/state/omarchy/current/theme"
CURRENT_BG_LINK = f"{HOME}/.local/state/omarchy/current/background"
BG_DIR = f"{CURRENT_THEME_DIR}/backgrounds"
HIGHLIGHTS_FILE = f"{CURRENT_THEME_DIR}/wallpaper_highlights.json"

def get_background_files():
    if not os.path.isdir(BG_DIR):
        # Fallback to local repo backgrounds if running unlinked
        local_bg = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backgrounds")
        if os.path.isdir(local_bg):
            files = sorted(glob.glob(os.path.join(local_bg, "*.[pP][nN][gG]")) +
                           glob.glob(os.path.join(local_bg, "*.[jJ][pP][gG]")) +
                           glob.glob(os.path.join(local_bg, "*.[jJ][pP][eE][gG]")))
            return files
        return []
    files = sorted(glob.glob(os.path.join(BG_DIR, "*.[pP][nN][gG]")) +
                   glob.glob(os.path.join(BG_DIR, "*.[jJ][pP][gG]")) +
                   glob.glob(os.path.join(BG_DIR, "*.[jJ][pP][eE][gG]")))
    return files

def get_current_background():
    if os.path.islink(CURRENT_BG_LINK) or os.path.exists(CURRENT_BG_LINK):
        try:
            return os.path.realpath(CURRENT_BG_LINK)
        except Exception:
            pass
    return ""

def load_vibe(idx_str):
    if os.path.exists(HIGHLIGHTS_FILE):
        try:
            with open(HIGHLIGHTS_FILE) as f:
                data = json.load(f)
                info = data.get(idx_str) or data.get(idx_str.lstrip("0")) or data.get(f"{int(idx_str):02d}")
                if info and "vibe" in info:
                    return info["vibe"]
        except Exception:
            pass
    return f"Wallpaper {idx_str}"

def set_background(target_path):
    if not os.path.exists(target_path):
        print(f"Error: background file not found: {target_path}", file=sys.stderr)
        return False

    # Use omarchy theme bg set if available
    res = subprocess.run(["omarchy", "theme", "bg", "set", target_path], capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback to atomic symlink update
        tmp_link = f"{CURRENT_BG_LINK}.tmp.{os.getpid()}"
        try:
            os.symlink(target_path, tmp_link)
            os.replace(tmp_link, CURRENT_BG_LINK)
        except Exception as e:
            print(f"Error updating symlink: {e}", file=sys.stderr)
            return False

    # Extract index from target filename
    basename = os.path.basename(target_path)
    digits = "".join([c for c in basename.split(".")[0] if c.isdigit()])
    vibe = load_vibe(digits) if digits else basename

    # Trigger recolor script if present
    recolor_script = f"{CURRENT_THEME_DIR}/update_wallpaper_colors.py"
    if os.path.exists(recolor_script):
        subprocess.run(["python3", recolor_script], capture_output=True)

    # Send desktop notification
    try:
        subprocess.run([
            "notify-send",
            "-a", "Dandadan Theme",
            "-i", target_path,
            "-t", "2500",
            f"󰄛 Wallpaper {digits or ''}",
            vibe
        ], capture_output=True)
    except Exception:
        pass

    print(f"Dandadan: switched to {target_path} ({vibe})")
    return True

def main():
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "next"
    files = get_background_files()
    if not files:
        print("No backgrounds found", file=sys.stderr)
        sys.exit(1)

    cur = get_current_background()
    cur_idx = 0
    if cur in files:
        cur_idx = files.index(cur)
    else:
        # Match by basename
        cur_base = os.path.basename(cur)
        for i, f in enumerate(files):
            if os.path.basename(f) == cur_base:
                cur_idx = i
                break

    if action == "next":
        next_idx = (cur_idx + 1) % len(files)
        target = files[next_idx]
    elif action in ("prev", "previous"):
        prev_idx = (cur_idx - 1 + len(files)) % len(files)
        target = files[prev_idx]
    elif action == "random":
        available = [f for f in files if f != cur] if len(files) > 1 else files
        target = random.choice(available)
    elif action == "set" and len(sys.argv) > 2:
        arg = sys.argv[2]
        if os.path.exists(arg):
            target = os.path.abspath(arg)
        else:
            # Try matching by index / number
            try:
                num = int("".join([c for c in arg if c.isdigit()]))
                matched = None
                for f in files:
                    f_digits = "".join([c for c in os.path.basename(f).split(".")[0] if c.isdigit()])
                    if f_digits and int(f_digits) == num:
                        matched = f
                        break
                if matched:
                    target = matched
                else:
                    print(f"No wallpaper matching index {arg}", file=sys.stderr)
                    sys.exit(1)
            except Exception:
                print(f"Invalid target: {arg}", file=sys.stderr)
                sys.exit(1)
    else:
        print(f"Usage: {sys.argv[0]} [next|prev|random|set <index|path>]")
        sys.exit(1)

    success = set_background(target)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
