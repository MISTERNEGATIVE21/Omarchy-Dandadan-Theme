import os, json

try:
    import tomllib
except ImportError:
    import tomli as tomllib

def test_dotfiles_exist_and_valid():
    assert os.path.exists("shell.toml"), "shell.toml missing"
    assert os.path.exists("shell.lock.toml"), "shell.lock.toml missing"
    assert os.path.exists("shell.json"), "shell.json missing"
    assert os.path.exists("hyprland.lua"), "hyprland.lua missing"

    with open("shell.json") as f:
        shell_json = json.load(f)
    assert "bar" in shell_json
    assert "layout" in shell_json["bar"]
    assert "left" in shell_json["bar"]["layout"]
    assert "center" in shell_json["bar"]["layout"]
    assert "right" in shell_json["bar"]["layout"]

    with open("shell.toml", "rb") as f:
        shell_toml = tomllib.load(f)
    assert "bar" in shell_toml
    assert "controls" in shell_toml
    assert "notifications" in shell_toml

    with open("hyprland.lua") as f:
        lua_content = f.read()
    # Verify Quickshell extensions and plugin manifest
    assert os.path.exists("plugins/dandadan.theme-control/manifest.json"), "manifest.json missing"
    assert os.path.exists("plugins/dandadan.theme-control/Widget.qml"), "Widget.qml missing"
    assert os.path.exists("plugins/dandadan.theme-control/Panel.qml"), "Panel.qml missing"
    assert os.path.exists("extensions/omarchy-menu.jsonc"), "omarchy-menu.jsonc missing"
    assert os.path.exists("scripts/cycle-wallpaper.py"), "cycle-wallpaper.py missing"
    assert os.access("scripts/cycle-wallpaper.py", os.X_OK), "cycle-wallpaper.py not executable"

    with open("plugins/dandadan.theme-control/manifest.json") as f:
        manifest = json.load(f)
    assert manifest.get("schemaVersion") == 1
    assert manifest.get("id") == "dandadan.theme-control"
    assert "bar-widget" in manifest.get("kinds", [])
    assert manifest.get("entryPoints", {}).get("barWidget") == "Widget.qml"

    # Verify shell.json enables extension
    assert "dandadan.theme-control" in shell_json.get("plugins", [])
    right_ids = [w.get("id") for w in shell_json["bar"]["layout"]["right"] if isinstance(w, dict)]
    assert "dandadan.theme-control" in right_ids, "dandadan.theme-control must be in bar.layout.right"

    print("PASS: GUI dotfiles and Quickshell extensions valid")

if __name__ == "__main__":
    test_dotfiles_exist_and_valid()
