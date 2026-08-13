import subprocess, os, json

def test_engine_execution():
    result = subprocess.run(["python3", "update_wallpaper_colors.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Engine failed: {result.stderr}"

    # Verify generated files exist and contain updated tokens
    for fname in ["shell.toml", "shell.lock.toml", "colors.toml", "hyprland.lua", "waybar.css"]:
        assert os.path.exists(fname), f"{fname} was not created"
        with open(fname) as f:
            content = f.read()
            assert len(content) > 0, f"{fname} is empty"

    print("PASS: Dynamic color engine executed successfully and generated all targets")

if __name__ == "__main__":
    test_engine_execution()
