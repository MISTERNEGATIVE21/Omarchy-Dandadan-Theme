# 🎌 Dandadan – Omarchy Theme

> **Dynamic anime-inspired dark theme for [Omarchy](https://github.com/basecamp/omarchy)**  
> 52 wallpapers · 21 app targets · per-image accent + complementary color theming

![Dandadan Theme Preview](https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/main/preview.png)

---

## ✨ Features

- **52 unique wallpapers** from the Dandadan anime series (001–058, zero-padded)
- **Dynamic per-image accent system** — PIL extracts the dominant vivid color from each wallpaper; a complementary/triadic palette is computed and applied live to every app
- **Apple-style glassmorphic Waybar** — 3-island pill layout:
  - **Left** — Omarchy logo · workspaces · active window title
  - **Center** — media player (MPRIS) · idle · DND · screen recording · update indicator
  - **Right** — clock · weather · CPU · RAM · audio · battery · network · Bluetooth · tray
- **21 fully themed targets** updated automatically on every wallpaper switch

---

## 🎯 Themed Applications

| Category | Apps |
|----------|------|
| **Shell / WM** | Hyprland borders (gradient) · Hyprlock lockscreen |
| **Bar** | Waybar (full per-image GTK CSS) · SwayOSD |
| **Terminals** | Kitty · Alacritty · Ghostty · Foot · Warp · Zellij |
| **Editors** | VS Code · Codium · Antigravity IDE · Zed · Neovim |
| **Browsers** | Firefox / Zen Browser · Chromium / Brave / Vivaldi |
| **Launchers** | Walker · Wofi |
| **Notifications** | Mako |
| **System** | Btop · GTK 3 & 4 |
| **Communication** | Telegram Desktop · Vencord / Vesktop (Discord) |
| **Icons** | Yaru icon theme (hue-matched to accent) |

---

## 🚀 Install

### Method 1 — omarchy-theme-install (Recommended)

```bash
omarchy-theme-install https://github.com/misternegative21/omarchy-Dandadan-Theme
```

Then activate:

```bash
omarchy-theme-set dandadan-theme
```

---

### Method 2 — One-liner install script

```bash
curl -fsSL https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/main/install.sh | bash
```

---

### Method 3 — Manual clone

```bash
git clone https://github.com/misternegative21/omarchy-Dandadan-Theme \
  ~/.config/omarchy/themes/dandadan-theme

bash ~/.config/omarchy/themes/dandadan-theme/install.sh
```

---

### Update

```bash
bash ~/.config/omarchy/themes/dandadan-theme/install.sh --update
```

Or via git + re-apply:

```bash
git -C ~/.config/omarchy/themes/dandadan-theme pull --ff-only
omarchy-theme-set dandadan-theme
```

---

### Uninstall

```bash
bash ~/.config/omarchy/themes/dandadan-theme/install.sh --uninstall
```

---

## 🎨 Dynamic Wallpaper Accents

Switching wallpapers automatically updates all 21 app targets:

```bash
omarchy theme bg next        # → accent colors update everywhere instantly
omarchy theme bg prev        # ← go back
```

To manually regenerate colors for the current wallpaper:

```bash
python3 ~/.config/omarchy/current/theme/update_wallpaper_colors.py
```

To re-extract accent palettes from all wallpaper images:

```bash
python3 ~/.config/omarchy/themes/dandadan-theme/extract_wallpaper_colors.py
```

---

## 💻 VS Code / Codium / Antigravity IDE

Auto-installed during setup. To activate manually:

1. `Ctrl+Shift+P` → **Preferences: Color Theme** → select **Dandadan**

Or via `settings.json`:

```json
{
  "workbench.colorTheme": "Dandadan"
}
```

---

## 🌀 Zed Editor

Auto-installed to `~/.config/zed/themes/dandadan.json`. To activate:

1. Open Zed → `Ctrl+K Ctrl+T` → select **Dandadan**

---

## 🌈 Wallpaper Palette (52 Scenes)

| # | Vibe | Accent | Highlight |
|---|------|--------|-----------|
| 01 | Okarun & Turbo Granny Golden Spark | `#08F503` | `#EA0B08` |
| 02 | Turbo Granny Crimson Curse | `#690001` | `#C05F58` |
| 03 | Momo Astral Pink & Blood Red | `#F70102` | `#E24B36` |
| 04 | Curse Transformation Scarlet | `#E80202` | `#E3847B` |
| 05 | Seiko Shrine Magenta Magic | `#C71275` | `#AB38C8` |
| 07 | High Octane Electric Cyan & Crimson | `#0DCAF9` | `#DC121A` |
| 08 | St. Germain Vermilion Mystery | `#DE0909` | `#903F41` |
| 10 | Alien Tech Deep Sapphire & Pink | `#1B35D1` | `#D41E38` |
| 11 | Subterranean Neon Violet & Turquoise | `#0B3996` | `#E618E7` |
| 14 | Kamo Cursed Gold & Emerald Glow | `#0DE1E5` | `#F6F65F` |
| 16 | Sunset Showdown Orange & Cobalt | `#F54603` | `#2D87F2` |
| 19 | Dandadan Iconic Pastel & Magenta | `#3E3E40` | `#403E3F` |
| 21 | Hyperdrive Neon Cyan & Coral | `#D8381B` | `#F5CB67` |
| 25 | Pyrotechnic Spark Amber & Purple | `#5203D9` | `#F9EF0A` |
| 26 | Masterpiece Action Splash Neon | `#F1C81D` | `#3C44B2` |
| 27 | Cursed Realm Shadow & Ruby | `#7016D2` | `#3292CB` |
| 35 | Turbo Sprint Crimson Spark | `#06F502` | `#E90C09` |
| 40 | Possessed Spirit Crimson Tide | `#E8304A` | `#4A8FD4` |
| 42 | Alien Queen Neon Rose & Aqua | `#D42055` | `#2BC4C8` |
| 43 | Deep Sea Ghost Electric Blue | `#0E9FD8` | `#E82040` |
| 47 | Paranormal Rift Magenta Spark | `#D91060` | `#F0C020` |
| 48 | Final Form Crimson & Cyber Teal | `#E62828` | `#28C4E6` |
| 49 | Chaos Rift Turbo Overdrive | `#9E03F9` | `#F9EB54` |
| 52 | Spirit World Neon Invasion | `#730C09` | `#C72825` |
| 56 | Ghost Protocol Crimson Edge | `#BEC13D` | `#7DB0F9` |
| 57 | Alien Surge Violet Static | `#2659C7` | `#654721` |
| 58 | Cursed Veil Ember & Abyss | `#E40BA1` | `#55DFB0` |
| … | *(52 total — see wallpaper_highlights.json)* | … | … |

---

## 🗂 File Structure

```
dandadan-theme/
├── backgrounds/               # 52 wallpapers (001–058.webp, zero-padded)
├── wallpaper_highlights.json  # Per-wallpaper accent + highlight palette (55 entries)
├── extract_wallpaper_colors.py  # Re-extracts colors from wallpaper images via PIL
├── update_wallpaper_colors.py   # Applies dynamic accents to all 21 app targets
├── install.sh                 # One-command installer
│
├── waybar_config.jsonc        # Waybar 3-island layout config
├── waybar.css                 # Waybar glassmorphic CSS (per-image regenerated)
├── style.css                  # Waybar style entry point (@import waybar.css)
├── wallpapers.css             # CSS color variable bridge for waybar
│
├── config.jsonc               # Waybar config (omarchy canonical)
├── colors.toml                # Omarchy terminal color palette
├── hyprland.conf              # Hyprland active/inactive border colors
├── hyprland.lua               # Hyprland Lua config overrides
├── hyprlock.conf              # Hyprlock lockscreen palette
│
├── alacritty.toml             # Alacritty terminal theme
├── kitty.conf                 # Kitty terminal theme
├── foot.ini                   # Foot terminal theme
├── ghostty.conf               # Ghostty terminal theme
├── warp.yaml                  # Warp terminal theme
├── zellij.kdl                 # Zellij multiplexer theme
│
├── vscode.json                # VS Code / Codium / AGY IDE theme
├── zed.json                   # Zed editor theme
├── neovim.lua                 # Neovim colorscheme overrides (LazyVim)
│
├── gtk.css                    # GTK 3 & 4 color variables
├── gtk-3.0/gtk.css            # GTK3 import shim
├── gtk-4.0/gtk.css            # GTK4 import shim
├── icons.theme                # Yaru icon theme selection (hue-matched)
│
├── firefox.css                # Firefox / Zen Browser userChrome
├── chromium.theme             # Chromium / Brave accent RGB
│
├── mako.ini                   # Mako notification daemon style
├── swayosd.css                # SwayOSD OSD popup style
├── walker.css                 # Walker launcher style
├── wofi.css                   # Wofi launcher style
│
├── vencord.theme.css          # Vencord / Vesktop (Discord) theme
├── telegram.palette           # Telegram Desktop palette
├── btop.theme                 # Btop system monitor theme
│
├── clock.sh                   # Waybar custom clock script
├── window.sh                  # Waybar active window script
└── scrolling-mpris.py         # Waybar scrolling MPRIS media script
```

---

## ⚙️ How the Dynamic Color Engine Works

```
wallpaper change
      │
      ▼
 omarchy bg-set hook
      │
      ▼
 update_wallpaper_colors.py
      │
      ├── reads wallpaper_highlights.json  (accent, highlight, background, foreground)
      ├── computes: complement (180°) · triadic (±120°) · analogous (±30°) · darken/lighten
      │
      ├── writes per-image configs for all 21 targets
      │     Waybar CSS · Mako · SwayOSD · Hyprlock · Hyprland · Alacritty
      │     Kitty · Foot · Ghostty · Btop · VS Code · GTK · Zed · Walker
      │     Wofi · Warp · Zellij · Vencord · Chromium · Firefox · Neovim
      │
      └── live-reloads: hyprctl · waybar SIGUSR2 · makoctl
```

To re-extract accent palettes from wallpaper images (uses PIL dominant color analysis):

```bash
python3 ~/.config/omarchy/themes/dandadan-theme/extract_wallpaper_colors.py
```

---

## 👥 Credits & Acknowledgments

Special thanks and appreciation to the creators, libraries, and platforms that made this theme possible:

- **[WallpaperHaven](https://whv.rs / https://wallpaperhaven.org)** — High-resolution anime wallpapers & community artwork catalog
- **Shahid Library** — Dandadan manga & anime artwork repository & media assets
- **[Omarchy](https://github.com/basecamp/omarchy)** — Modern Linux desktop environment & theme framework
- **Yukinobu Tatsu / Science SARU** — The legendary creators and animation studio behind *Dandadan* (ダンダダン)

---

## 📜 License

MIT – Made with ❤️ by [misternegative21](https://github.com/misternegative21)
