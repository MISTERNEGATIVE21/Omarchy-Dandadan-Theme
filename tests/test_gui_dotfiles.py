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
    assert "hl.config" in lua_content
    assert "active_border" in lua_content
    assert "shadow" in lua_content

    print("PASS: GUI dotfiles valid")

if __name__ == "__main__":
    test_dotfiles_exist_and_valid()
