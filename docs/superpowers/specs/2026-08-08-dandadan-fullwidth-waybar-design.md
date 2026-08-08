# Design Specification: DANDADAN Full-Width Waybar & Center Music Controls

**Date:** 2026-08-08  
**Theme:** DANDADAN  
**Target Files:** `waybar_config.jsonc`, `waybar.css`  

---

## 1. Overview & Goal
Transform the Waybar layout for the DANDADAN theme into a full-width header bar (`width: 100%`) with:
1. Glassmorphic translucent dark background (`rgba(20, 22, 30, 0.90)`) with a glowing bottom accent border (`border-bottom: 2px solid @cursor;`).
2. Left Section: Omarchy brand button with neon magenta badge (`#custom-omarchy`), and workspace bar (`#workspaces`) with active workspace highlight pills (`box-shadow: 0 0 12px @cursor; background: @cursor; color: #FFFFFF;`).
3. Center Section: Music player controls (`mpris`) with track info, play/pause toggle, and scroll control, beside the date and time clock card (`#clock`).
4. Right Section: Rich status badges for CPU utilization (`󰍛 12%`), Audio volume (` 75%`), Network Wi-Fi/Ethernet (`󰤨  SSID`), Bluetooth (``), Battery capacity (`󰁹 90%`), and Tray expander.

---

## 2. Configuration & Layout Specification

### 2.1 `waybar_config.jsonc`
```jsonc
{
  "layer": "top",
  "position": "top",
  "height": 34,
  "spacing": 0,
  "modules-left": [
    "custom/omarchy",
    "hyprland/workspaces"
  ],
  "modules-center": [
    "mpris",
    "clock#horizontal",
    "custom/weather"
  ],
  "modules-right": [
    "cpu",
    "pulseaudio",
    "network",
    "bluetooth",
    "battery",
    "group/tray-expander"
  ],
  "mpris": {
    "format": "󰎈 {artist} - {title}",
    "format-paused": "󰏤 <i>{artist} - {title}</i>",
    "player-icons": {
      "default": "󰎈",
      "spotify": ""
    },
    "status-icons": {
      "paused": "󰏤"
    },
    "max-length": 32,
    "on-click": "playerctl play-pause",
    "on-scroll-up": "playerctl next",
    "on-scroll-down": "playerctl previous"
  },
  "cpu": {
    "interval": 3,
    "format": "󰍛 {usage}%",
    "on-click": "omarchy-launch-or-focus-tui btop"
  },
  "pulseaudio": {
    "format": "{icon} {volume}%",
    "format-muted": "  Muted",
    "format-icons": {
      "headphone": "",
      "headset": "",
      "default": ["", "", ""]
    },
    "on-click": "omarchy-launch-audio",
    "on-click-right": "pamixer -t"
  },
  "network": {
    "format-wifi": "󰤨  {essid}",
    "format-ethernet": "󰀂  Ethernet",
    "format-disconnected": "󰤮  Disconnected",
    "on-click": "omarchy-launch-wifi"
  },
  "battery": {
    "format": "{icon} {capacity}%",
    "format-charging": "󰂄 {capacity}%",
    "format-plugged": " {capacity}%",
    "format-icons": ["󰁺", "󰁻", "󰁼", "󰁽", "󰁾", "󰁿", "󰂀", "󰂁", "󰂂", "󰁹"]
  }
}
```

### 2.2 `waybar.css`
- `window#waybar`: Full width header bar, `background: rgba(20, 22, 30, 0.90)`, `border-bottom: 2px solid @cursor`.
- Center Mpris Module (`#mpris`): Pill card container with subtle translucent tint (`background: rgba(255, 255, 255, 0.07); border: 1px solid @accent; border-radius: 10px; padding: 2px 12px; color: @foreground; font-weight: bold;`).
- Module Pills: Rounded capsule modules (`border-radius: 10px; padding: 3px 12px; margin: 3px 4px;`).
- Workspace Buttons: Active workspace button (`background: @cursor; color: #FFFFFF; font-weight: bold; border-radius: 6px; box-shadow: 0 0 10px @cursor;`).

---

## 3. Verification Strategy
1. Validate `waybar_config.jsonc` syntax using Python regex comment stripper + JSON parser.
2. Validate `waybar.css` GTK CSS syntax.
3. Test running `omarchy-theme-set DANDADAN` and launch `waybar`.
4. Verify `pgrep -a waybar` returns process ID 0 exit code.
