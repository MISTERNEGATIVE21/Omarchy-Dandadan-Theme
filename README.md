# 🎌 Dandadan – Omarchy Theme

> **Dynamic anime-inspired dark theme for [Omarchy](https://github.com/basecamp/omarchy)**  
> Auto-adapting accent colors per wallpaper • Apple glassmorphism Waybar • Full app theming

![Dandadan Theme Preview](https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/main/preview.png)

---

## ✨ Features

- **39 unique wallpapers** from the Dandadan anime series
- **Dynamic accent colors** auto-extracted from each wallpaper – Waybar, Hyprland borders, terminals, browsers, and Telegram all morph to match
- **Apple-style glassmorphic Waybar** – Left (workspaces + active window), Center (media player + notifications), Right (clock, weather, CPU, RAM, battery)
- **Per-wallpaper theming** for:
  - 🖥️ Waybar (GTK CSS)
  - 🪟 Hyprland window borders (gradient)
  - 🖤 Kitty, Alacritty, Ghostty, Foot terminals
  - 🌐 Firefox / Zen Browser, Chromium / Brave / Vivaldi / Chrome
  - 📱 Telegram Desktop
  - 💻 VS Code / Codium / Antigravity IDE
  - 🔔 Mako notifications, Walker launcher, SwayOSD, Btop

---

## 🚀 Install

### Via omarchy-theme-install (Recommended)

```bash
omarchy-theme-install https://github.com/misternegative21/omarchy-Dandadan-Theme
```

### Via install script

```bash
curl -fsSL https://raw.githubusercontent.com/misternegative21/omarchy-Dandadan-Theme/main/install.sh | bash
```

Or clone manually:

```bash
git clone https://github.com/misternegative21/omarchy-Dandadan-Theme ~/.config/omarchy/themes/dandadan
bash ~/.config/omarchy/themes/dandadan/install.sh
```

### Update

```bash
bash ~/.config/omarchy/themes/dandadan/install.sh --update
```

### Uninstall

```bash
bash ~/.config/omarchy/themes/dandadan/install.sh --uninstall
```

---

## 🎨 Dynamic Wallpaper Accents

When you switch wallpapers, all app accents update automatically:

```bash
omarchy theme bg next        # cycle to next wallpaper → colors update everywhere
```

To manually regenerate colors from wallpapers:

```bash
python3 ~/.config/omarchy/themes/dandadan/extract_wallpaper_colors.py
python3 ~/.config/omarchy/themes/dandadan/update_wallpaper_colors.py
```

---

## 💻 VS Code / Codium / Antigravity IDE

The theme is auto-installed during setup. To activate manually:

1. Open VS Code → `Cmd/Ctrl+Shift+P` → **Preferences: Color Theme**
2. Select **Dandadan**

Or via settings.json:

```json
{
  "workbench.colorTheme": "Dandadan"
}
```

---

## 🌈 Wallpaper Palette (39 Scenes)

| # | Vibe | Accent | Highlight |
|---|------|--------|-----------|
| 01 | Okarun & Turbo Granny Golden Spark | `#08F503` | `#EA0B08` |
| 05 | Seiko Shrine Magenta Magic | `#C71275` | `#AB38C8` |
| 06 | Serpo Alien Cyan & Magenta Blast | `#CE0438` | `#07D8E4` |
| 07 | High Octane Electric Cyan & Crimson | `#0DCAF9` | `#DC121A` |
| 10 | Alien Tech Deep Sapphire & Pink | `#1B35D1` | `#D41E38` |
| 14 | Kamo Cursed Gold & Emerald Glow | `#0DE1E5` | `#F6F65F` |
| 19 | Dandadan Iconic Pastel & Magenta | `#3E3E40` | `#403E3F` |
| 25 | Pyrotechnic Spark Amber & Purple | `#5203D9` | `#F9EF0A` |
| 26 | Masterpiece Action Splash Neon | `#F1C81D` | `#3C44B2` |
| 27 | Cursed Realm Shadow & Ruby | `#7016D2` | `#3292CB` |
| … | … | … | … |

---

## 🗂 File Structure

```
dandadan/
├── backgrounds/          # 39 Dandadan wallpapers (01–39.webp)
├── config.jsonc          # Waybar layout (Left / Center / Right)
├── style.css             # Waybar Apple glassmorphic CSS
├── wallpaper_highlights.json  # Per-wallpaper accent palette
├── extract_wallpaper_colors.py  # Re-extract colors from wallpapers
├── update_wallpaper_colors.py   # Apply dynamic accents to all apps
├── install.sh            # One-command installer
├── vscode.json           # VS Code / Codium theme
├── kitty.conf            # Kitty terminal theme
├── alacritty.toml        # Alacritty terminal theme
├── ghostty.conf          # Ghostty terminal theme
├── foot.ini              # Foot terminal theme
├── telegram.palette      # Telegram Desktop theme
├── firefox.css           # Firefox / Zen Browser CSS
├── chromium.theme        # Chromium / Brave / Vivaldi theme
├── hyprland.conf         # Hyprland border & decoration config
├── hyprlock.conf         # Hyprlock lockscreen config
├── mako.ini              # Mako notification style
├── walker.css            # Walker launcher style
├── swayosd.css           # SwayOSD popup style
└── btop.theme            # Btop system monitor theme
```

---

## 📜 License

MIT – Made with ❤️ by [misternegative21](https://github.com/misternegative21)
