#!/usr/bin/env python3
"""
Extract dominant accent colors from each dandadan wallpaper and rebuild
wallpaper_highlights.json with accurate, per-wallpaper accent palettes.
Handles all 48 wallpapers.
"""

import os, json, colorsys
from PIL import Image

THEME_DIR     = os.path.expanduser("~/.config/omarchy/themes/dandadan-theme")
WALLPAPER_DIR = os.path.join(THEME_DIR, "backgrounds")
OUTPUT_PATH   = os.path.join(THEME_DIR, "wallpaper_highlights.json")

# Vibe labels per wallpaper (narrative)
VIBES = {
    "01": "Okarun & Turbo Granny Golden Spark",
    "02": "Turbo Granny Crimson Curse",
    "03": "Momo Astral Pink & Blood Red",
    "04": "Curse Transformation Scarlet",
    "05": "Seiko Shrine Magenta Magic",
    "06": "Serpo Alien Cyan & Magenta Blast",
    "07": "High Octane Electric Cyan & Crimson",
    "08": "St. Germain Vermilion Mystery",
    "09": "Acrobat Silky Scarlet Tears",
    "10": "Alien Tech Deep Sapphire & Pink",
    "11": "Subterranean Neon Violet & Turquoise",
    "12": "Golden Hour Okamomo Warmth",
    "13": "Yokai Night Midnight Teal & Bronze",
    "14": "Kamo Cursed Gold & Emerald Glow",
    "15": "Turbo Form Azure Lightning",
    "16": "Sunset Showdown Orange & Cobalt",
    "17": "Flatwoods Monster Blood Crimson",
    "18": "Evil Eye Wrathful Carmine",
    "19": "Dandadan Iconic Pastel & Magenta",
    "20": "Spiritual Energy Flame Red",
    "21": "Hyperdrive Neon Cyan & Coral",
    "22": "Vintage Manga Sepia & Vermilion",
    "23": "Astral Projection Violet Aura",
    "24": "Abyssal Alien Void Indigo",
    "25": "Pyrotechnic Spark Amber & Purple",
    "26": "Masterpiece Action Splash Neon",
    "27": "Cursed Realm Shadow & Ruby",
    "28": "Giant Kaiju Battle Emerald & Gold",
    "29": "Chiquitita Micro-Cosmos Pastel",
    "30": "Spectral Haunting Ghostly Jade",
    "31": "Invasion Mothership Electric Blue",
    "32": "Momo & Okarun Midnight Starlight",
    "33": "Unidentified Flying Object Glow",
    "34": "Subterranean Sub-surface Lava",
    "35": "Turbo Sprint Crimson Spark",
    "36": "Classroom Commotion Warm Amber",
    "37": "Dimensional Rift Ultra Violet",
    "38": "Battlefield Destruction Fiery Ochre",
    "39": "Curse Unleashed Dark Ruby",
    "40": "Possessed Spirit Crimson Tide",
    "41": "Thunder God Battle Scarlet",
    "42": "Alien Queen Neon Rose & Aqua",
    "43": "Deep Sea Ghost Electric Blue",
    "44": "Yokai Summoning Blood & Violet",
    "45": "Spirit Burst Ember & Sky",
    "46": "Supernatural Stand-off Teal Blaze",
    "47": "Paranormal Rift Magenta Spark",
    "48": "Final Form Crimson & Cyber Teal",
    "49": "Chaos Rift Turbo Overdrive",
    "52": "Spirit World Neon Invasion",
    "53": "Yokai Clash Midnight Scarlet",
    "54": "Astral Dimension Shadow Burst",
    "56": "Ghost Protocol Crimson Edge",
    "57": "Alien Surge Violet Static",
    "58": "Cursed Veil Ember & Abyss",
}

BG = "#14161E"
FG = "#F0F4FC"

def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

def rgb_to_hsv(r, g, b):
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)

def extract_palette(path, n_colors=8, resize=150):
    """Resize, quantize, return top n_colors sorted by saturation*value (vivid first)."""
    try:
        img = Image.open(path).convert("RGB").resize((resize, resize))
        img_q = img.quantize(colors=32, method=Image.Quantize.FASTOCTREE).convert("RGB")
        pixels = list(img_q.getdata())
        freq = {}
        for p in pixels:
            freq[p] = freq.get(p, 0) + 1
        # Sort by saturation * value descending (most vivid first)
        sorted_colors = sorted(freq.keys(),
                               key=lambda c: rgb_to_hsv(*c)[1] * rgb_to_hsv(*c)[2],
                               reverse=True)
        return sorted_colors[:n_colors]
    except Exception as e:
        print(f"  Error: {e}")
        return []

def pick_accent_and_contrast(colors):
    """
    Pick the most saturated vivid color as accent,
    pick the most contrasting vivid color as highlight/cursor.
    """
    if not colors:
        return "#D8B3FE", "#E1477A", "#E1477A"

    # Filter out near-black and near-white
    vivid = []
    for c in colors:
        h, s, v = rgb_to_hsv(*c)
        if s > 0.25 and v > 0.2 and v < 0.98:
            vivid.append((c, s, v))

    if not vivid:
        vivid = [(c, *rgb_to_hsv(*c)[1:]) for c in colors[:3]]

    # Sort by saturation desc
    vivid.sort(key=lambda x: x[1], reverse=True)

    accent_rgb = vivid[0][0]
    accent_hex = rgb_to_hex(*accent_rgb)

    # Pick a highlight: max hue distance from accent
    accent_h = rgb_to_hsv(*accent_rgb)[0]
    best_contrast = None
    best_dist = 0
    for (c, s, v) in vivid[1:]:
        h = rgb_to_hsv(*c)[0]
        dist = abs(h - accent_h)
        if dist > 0.5:
            dist = 1.0 - dist
        if dist > best_dist and s > 0.2:
            best_dist = dist
            best_contrast = c

    if best_contrast is None:
        best_contrast = vivid[min(1, len(vivid)-1)][0]

    highlight_hex = rgb_to_hex(*best_contrast)
    glow_hex      = highlight_hex

    return accent_hex, highlight_hex, glow_hex

result = {}

# Discover all wallpapers — handles both 2-digit (01.webp) and 3-digit (049.webp) names
webp_files = {}
for fname in sorted(os.listdir(WALLPAPER_DIR)):
    if fname.endswith(".webp"):
        num_str = fname.replace(".webp", "")        # e.g. '049'
        num_int = int(num_str)                       # 49
        key     = f"{num_int:02d}"                   # '49'
        webp_files[key] = os.path.join(WALLPAPER_DIR, fname)

print(f"Found {len(webp_files)} wallpapers in {WALLPAPER_DIR}")
print(f"Keys: {sorted(webp_files.keys(), key=int)}")

for idx in sorted(webp_files.keys(), key=int):
    path = webp_files[idx]
    print(f"Processing {idx} ({os.path.basename(path)})...", end=" ", flush=True)
    colors = extract_palette(path)
    accent, highlight, glow = pick_accent_and_contrast(colors)
    print(f"accent={accent}  highlight={highlight}")

    result[idx] = {
        "accent":     accent,
        "highlight":  highlight,
        "background": BG,
        "foreground": FG,
        "border":     accent,
        "glow":       glow,
        "vibe":       VIBES.get(idx, f"Dandadan Scene {idx}"),
    }

# Sort by int value
result_sorted = dict(sorted(result.items(), key=lambda x: int(x[0])))

with open(OUTPUT_PATH, "w") as f:
    json.dump(result_sorted, f, indent=2)

print(f"\n✓ Wrote {len(result_sorted)} wallpaper palettes to {OUTPUT_PATH}")
