import json, os, sys, colorsys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from update_wallpaper_colors import build_semantic_palette

def h2r(hex_code: str):
    h = hex_code.strip().lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def hex_to_hsv(hex_code: str):
    r, g, b = h2r(hex_code)
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)

def test_all_52_wallpapers_palette_integrity():
    with open("wallpaper_highlights.json") as f:
        data = json.load(f)

    assert len(data) >= 50, f"Expected at least 50 wallpapers in manifest, found {len(data)}"

    for idx, colors in data.items():
        accent = colors.get("accent")
        highlight = colors.get("highlight")
        assert accent, f"Wallpaper {idx} missing accent"
        assert highlight, f"Wallpaper {idx} missing highlight"

        sem = build_semantic_palette(accent, highlight)

        # Check all 6 chromatic ANSI channels
        red_h = hex_to_hsv(sem["red"])[0]
        green_h = hex_to_hsv(sem["green"])[0]
        yellow_h = hex_to_hsv(sem["yellow"])[0]
        blue_h = hex_to_hsv(sem["blue"])[0]
        cyan_h = hex_to_hsv(sem["cyan"])[0]
        magenta_h = hex_to_hsv(sem["magenta"])[0]

        assert red_h < 0.08 or red_h > 0.92, f"Wallpaper {idx}: Red ({sem['red']}, hue={red_h:.3f}) inverted/wrong hue!"
        assert 0.20 <= green_h <= 0.45, f"Wallpaper {idx}: Green ({sem['green']}, hue={green_h:.3f}) inverted/wrong hue!"
        assert 0.10 <= yellow_h <= 0.22, f"Wallpaper {idx}: Yellow ({sem['yellow']}, hue={yellow_h:.3f}) inverted/wrong hue!"
        assert 0.55 <= blue_h <= 0.70, f"Wallpaper {idx}: Blue ({sem['blue']}, hue={blue_h:.3f}) inverted/wrong hue!"
        assert 0.43 <= cyan_h <= 0.55, f"Wallpaper {idx}: Cyan ({sem['cyan']}, hue={cyan_h:.3f}) inverted/wrong hue!"
        assert 0.70 <= magenta_h <= 0.95, f"Wallpaper {idx}: Magenta ({sem['magenta']}, hue={magenta_h:.3f}) inverted/wrong hue!"

    print(f"PASS: All {len(data)} wallpapers verified for strict ANSI channel non-inversion.")

if __name__ == "__main__":
    test_all_52_wallpapers_palette_integrity()
