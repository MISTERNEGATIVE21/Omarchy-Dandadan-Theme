# Design Specification: DANDADAN Theme Wallpaper Highlights & Waybar Customization

**Date:** 2026-08-08  
**Theme:** DANDADAN  
**Workspace:** `/home/mister/.config/omarchy/themes/DANDADAN`  

---

## 1. Overview & Objectives

The goal of this project is to create a complete, high-energy customization system for the **DANDADAN** Omarchy theme, featuring:
1. **Per-Wallpaper Highlight & Color Schemes** for all 39 wallpaper backgrounds (`01.webp` to `39.webp`) located in `backgrounds/`.
2. **Dynamic Wallpaper CSS Classes (`wallpapers.css`)** and a **Unified JSON Manifest (`wallpaper_highlights.json`)** defining primary accent, highlight, background, foreground, border, and glow hex codes for every background.
3. **Floating Capsule / Pill Style Waybar Configuration** (`waybar_config.jsonc`, `waybar.css`) featuring custom modules, animated workspace icons, system controls, and wallpaper-reactive highlight accents.
4. **Desktop App Customizations** across Hyprland, Hyprlock, Kitty, Ghostty, Alacritty, Mako notifications, Walker launcher, SwayOSD, Btop system monitor, Chromium, VSCode, and Neovim.
5. **Wallpaper Switcher Helper Script (`wallpaper_switch.sh`)** for seamless switching between wallpapers with instant theme and CSS highlight reloads.

---

## 2. Architecture & Data Structures

### 2.1 Per-Wallpaper Highlight Manifest (`wallpaper_highlights.json`)
A structured manifest mapping every background index (`01` through `39`) to tailored color tokens:
* `accent`: Primary vibrant hex code (e.g. Dandadan Pink `#E1477A`, Alien Teal `#30A69D`, Spirit Violet `#D8B3FE`, Turbo Amber `#FFA726`).
* `highlight`: Secondary accent hex code for active states and badges.
* `background`: Base background color tuned for contrast (`rgba(EEEDEE, 0.85)` or dark translucent variants).
* `foreground`: Main text color (`#2C393B` or light text `#EEEDEE`).
* `border`: Border color with subtle alpha glow.
* `glow`: High-intensity neon color for active workspace indicator and focused window borders.
* `vibe`: Descriptor (e.g., `"Neon occult"`, `"Spirit teal"`, `"Cyberpunk pink"`, `"Sunset golden"`).

### 2.2 Dynamic CSS Highlights (`wallpapers.css`)
Generates CSS rules `.wallpaper-01` through `.wallpaper-39` defining GTK / Waybar custom variables:
```css
.wallpaper-01 {
  --wp-accent: #E1477A;
  --wp-highlight: #D8B3FE;
  --wp-bg: rgba(238, 237, 238, 0.88);
  --wp-fg: #2C393B;
  --wp-border: rgba(225, 71, 122, 0.45);
  --wp-glow: #E1477A;
}
/* ... 02 through 39 ... */
```

---

## 3. Waybar Configuration & Styling

### 3.1 Waybar Module Layout (`waybar_config.jsonc`)
* **Modules Left**:
  * `custom/omarchy`: Custom Dandadan logo icon (`\ue900`) with click trigger for `omarchy-menu`.
  * `hyprland/workspaces`: Interactive floating pill buttons with active workspace indicators (`󱓻`, ``).
* **Modules Center**:
  * `clock#horizontal`: Date and time format (`%A %H:%M`).
  * `custom/weather`: Weather status script integration.
  * `custom/update`: System update indicator.
  * `custom/screenrecording-indicator` & `custom/idle-indicator`.
* **Modules Right**:
  * `group/tray-expander`: Collapsible tray expander drawer.
  * `bluetooth`, `network`, `pulseaudio`, `cpu`, `battery`.

### 3.2 Waybar Floating Pill CSS (`waybar.css`)
* Capsule/Pill structure: `border-radius: 12px; margin: 4px 6px; padding: 2px 10px;`.
* Background glassmorphism: `background: var(--wp-bg); shadow: 0 4px 12px rgba(0,0,0,0.3);`.
* Hover and active states: Highlight glow, border color transition using `var(--wp-accent)` and `var(--wp-border)`.

---

## 4. Desktop App Customizations

1. **Hyprland (`hyprland.conf`)**:
   * Active window border: `col.active_border = rgb(E1477A) rgb(D8B3FE) 45deg`
   * Inactive window border: `col.inactive_border = rgb(DADADA)`
2. **Hyprlock (`hyprlock.conf`)**:
   * Background wallpaper blur, matching highlight text ring, input field accent colors.
3. **Terminals (`kitty.conf`, `alacritty.toml`, `ghostty.conf`)**:
   * Full 16-color Dandadan palette with custom cursor `#E1477A` and selection background `#E8759B`.
4. **Mako (`mako.ini`)**:
   * Notification popups styled as floating pills with 12px border-radius and highlight borders.
5. **Walker Launcher (`walker.css`)**:
   * Floating capsule modal with highlighted selection pill and neon border.
6. **SwayOSD (`swayosd.css`)**:
   * Volume/brightness OSD formatted as floating pills.
7. **Btop (`btop.theme`)**:
   * Gradient graph themes for CPU, Memory, Net, and Temp monitors.

---

## 5. Wallpaper Switcher Script (`wallpaper_switch.sh`)

A bash script to switch wallpapers seamlessly:
* Usage: `./wallpaper_switch.sh [01..39]` or `./wallpaper_switch.sh random`.
* Updates `/home/mister/.config/omarchy/current/background` symlink.
* Re-applies active `.wallpaper-XX` CSS class in `waybar.css` / GTK stylesheet.
* Sends reload signals to Waybar (`killall -SIGUSR2 waybar` or `omarchy-restart-waybar`) and Hyprland.

---

## 6. Verification & Self-Review Checklist

- [x] All 39 wallpapers accounted for in `wallpaper_highlights.json` and `wallpapers.css`.
- [x] Waybar layout syntax validated for JSONC compliance.
- [x] No missing variable references or undefined fallback styles.
- [x] Complete coverage across desktop applications in the DANDADAN theme.
