import subprocess, os, json, colorsys

def h2r(hex_code: str):
    h = hex_code.strip().lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def hex_to_hsv(hex_code: str):
    r, g, b = h2r(hex_code)
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)

def test_engine_execution():
    result = subprocess.run(["python3", "update_wallpaper_colors.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Engine failed: {result.stderr}"

    # Verify generated files exist and contain updated tokens
    for fname in ["shell.toml", "shell.lock.toml", "colors.toml", "hyprland.lua", "waybar.css", "wallpapers.css", "icons.theme", "gtk.css", "kitty.conf", "alacritty.toml", "ghostty.conf", "foot.ini"]:
        assert os.path.exists(fname), f"{fname} was not created"
        with open(fname) as f:
            content = f.read()
            assert len(content) > 0, f"{fname} is empty"

    # Verify wallpapers.css contains valid colors
    with open("wallpapers.css") as f:
        wallpapers_css = f.read()
    assert "@define-color accent" in wallpapers_css
    assert "@define-color background" in wallpapers_css

    # Verify icon theme exists on disk
    with open("icons.theme") as f:
        icon_theme = f.read().strip()
    home = os.path.expanduser("~")
    exists_on_disk = any(
        os.path.exists(f"{prefix}/{icon_theme}")
        for prefix in ["/usr/share/icons", f"{home}/.local/share/icons", f"{home}/.icons"]
    )
    assert exists_on_disk, f"Generated icon theme '{icon_theme}' does not exist on disk!"

    # Verify GTK CSS contrast definition
    with open("gtk.css") as f:
        gtk_css = f.read()
    assert "@define-color accent_fg_color" in gtk_css
    assert "@define-color accent_bg_color" in gtk_css

    # Verify Quickshell shell.toml contrast, visibility & active border tokens
    with open("shell.toml") as f:
        shell_toml = f.read()
    assert "selected-background" in shell_toml
    assert "selected-text" in shell_toml
    assert "placeholder" in shell_toml
    assert "text-error" in shell_toml
    assert "border-error" in shell_toml
    assert "hyprland.active-border" in shell_toml
    assert "background-alpha = 0.95" in shell_toml

    # Verify Omarchy 4.0 colors.toml specification & true ANSI hue channels
    with open("colors.toml") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    colors = {}
    for line in lines:
        if "=" in line:
            k, v = line.split("=", 1)
            colors[k.strip()] = v.strip().strip('"')

    assert colors.get("mode") == "dark", "mode must be dark in colors.toml"
    assert "accent" in colors
    assert "selection" in colors
    assert "muted" in colors
    assert "background" in colors
    assert "hyprland_active_border" in colors
    assert "foreground" in colors

    # Strict ANSI hue verification (NO INVERTED CHANNELS)
    red_h = hex_to_hsv(colors["red"])[0]
    green_h = hex_to_hsv(colors["green"])[0]
    yellow_h = hex_to_hsv(colors["yellow"])[0]
    blue_h = hex_to_hsv(colors["blue"])[0]
    cyan_h = hex_to_hsv(colors["cyan"])[0]
    magenta_h = hex_to_hsv(colors["magenta"])[0]

    assert red_h < 0.08 or red_h > 0.92, f"ANSI Red ({colors['red']}, hue={red_h}) is not in Red hue range!"
    assert 0.20 <= green_h <= 0.45, f"ANSI Green ({colors['green']}, hue={green_h}) is not in Green hue range!"
    assert 0.10 <= yellow_h <= 0.22, f"ANSI Yellow ({colors['yellow']}, hue={yellow_h}) is not in Yellow hue range!"
    assert 0.55 <= blue_h <= 0.72, f"ANSI Blue ({colors['blue']}, hue={blue_h}) is not in Blue hue range!"
    assert 0.43 <= cyan_h <= 0.55, f"ANSI Cyan ({colors['cyan']}, hue={cyan_h}) is not in Cyan hue range!"
    assert 0.73 <= magenta_h <= 0.95, f"ANSI Magenta ({colors['magenta']}, hue={magenta_h}) is not in Magenta hue range!"

    # Verify Kitty terminal config
    with open("kitty.conf") as f:
        kitty_conf = f.read()
    assert "background #14161E" in kitty_conf, "Kitty must use clean dark background #14161E"
    assert "foreground #F0F4FC" in kitty_conf, "Kitty must use clean crisp foreground #F0F4FC"
    assert f"color1  {colors['red']}" in kitty_conf, "Kitty color1 must map to true red"
    assert f"color2  {colors['green']}" in kitty_conf, "Kitty color2 must map to true green"

    print(f"PASS: Dynamic color engine executed successfully (strict non-inverted ANSI channels verified)")

if __name__ == "__main__":
    test_engine_execution()
