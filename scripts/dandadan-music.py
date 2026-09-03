#!/usr/bin/env python3
"""
Dandadan Anime Music & Media Controller
Manages playback via playerctl and provides a built-in Dandadan Lo-Fi & Anime OST radio stream.
"""

import os
import sys
import subprocess
import json

RADIO_STREAM_URL = "https://stream.zeno.fm/f3wvbbqmdg8uv" # High quality Anime / Lo-Fi 24/7 stream
PID_FILE = "/tmp/dandadan-music.pid"

def run_cmd(args):
    try:
        res = subprocess.run(args, capture_output=True, text=True)
        return res.returncode, res.stdout.strip()
    except Exception as e:
        return 1, str(e)

def is_radio_playing():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            # Check if process is still running
            os.kill(pid, 0)
            return True, pid
        except Exception:
            if os.path.exists(PID_FILE):
                try: os.remove(PID_FILE)
                except Exception: pass
    return False, None

def stop_radio():
    playing, pid = is_radio_playing()
    if playing and pid:
        try:
            os.kill(pid, 15)
        except Exception:
            pass
    if os.path.exists(PID_FILE):
        try: os.remove(PID_FILE)
        except Exception: pass
    # Also kill any orphaned mpv anime radio process
    subprocess.run(["pkill", "-f", "dandadan-anime-radio"], capture_output=True)

def start_radio():
    stop_radio()
    cmd = [
        "mpv",
        "--no-video",
        "--title=dandadan-anime-radio",
        RADIO_STREAM_URL
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        with open(PID_FILE, "w") as f:
            f.write(str(proc.pid))
        send_notification("󰝚 Dandadan Anime Radio", "Playing: 24/7 Anime & Lo-Fi Beats")
        return True
    except Exception as e:
        print(f"Failed to start radio: {e}", file=sys.stderr)
        return False

def get_mpris_status():
    code, status = run_cmd(["playerctl", "status"])
    if code != 0:
        return "Stopped", "", ""
    code_t, title = run_cmd(["playerctl", "metadata", "title"])
    code_a, artist = run_cmd(["playerctl", "metadata", "artist"])
    return status, title, artist

def send_notification(title, msg):
    try:
        subprocess.run(["notify-send", "-a", "Dandadan Music", "-t", "2500", title, msg], capture_output=True)
    except Exception:
        pass

def main():
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "status"

    radio_on, _ = is_radio_playing()
    mpris_status, title, artist = get_mpris_status()

    if action == "status":
        if radio_on:
            print(json.dumps({
                "status": "Playing",
                "title": "Anime & Lo-Fi Beats",
                "artist": "Dandadan Radio",
                "isRadio": True
            }))
        elif mpris_status in ("Playing", "Paused"):
            print(json.dumps({
                "status": mpris_status,
                "title": title or "Unknown Track",
                "artist": artist or "Unknown Artist",
                "isRadio": False
            }))
        else:
            print(json.dumps({
                "status": "Stopped",
                "title": "No media playing",
                "artist": "Idle",
                "isRadio": False
            }))

    elif action == "toggle":
        if radio_on:
            stop_radio()
            send_notification("󰝚 Dandadan Music", "Radio Paused")
            print("Radio stopped")
        elif mpris_status in ("Playing", "Paused"):
            run_cmd(["playerctl", "play-pause"])
            print("Toggled MPRIS player")
        else:
            start_radio()
            print("Started Anime Radio")

    elif action == "play":
        if mpris_status in ("Playing", "Paused"):
            run_cmd(["playerctl", "play"])
        else:
            start_radio()

    elif action == "stop":
        stop_radio()
        run_cmd(["playerctl", "stop"])
        send_notification("󰝚 Dandadan Music", "Playback stopped")

    elif action == "next":
        if mpris_status in ("Playing", "Paused"):
            run_cmd(["playerctl", "next"])
        else:
            # Restart/cycle stream
            start_radio()

    elif action == "prev":
        if mpris_status in ("Playing", "Paused"):
            run_cmd(["playerctl", "previous"])

    elif action == "radio":
        if radio_on:
            stop_radio()
            send_notification("󰝚 Dandadan Music", "Radio stopped")
        else:
            start_radio()

    else:
        print(f"Usage: {sys.argv[0]} [status|toggle|play|stop|next|prev|radio]")
        sys.exit(1)

if __name__ == "__main__":
    main()
