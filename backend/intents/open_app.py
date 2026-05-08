"""
open_app intent handler for Friday AI
Opens applications on Windows using AppOpener with subprocess fallback.
"""

import subprocess
import sys
from typing import Optional

try:
    from AppOpener import open as _app_open
    _HAS_APPOPENER = True
except ImportError:
    _HAS_APPOPENER = False

# Well-known app shortcuts for Windows fallback
_KNOWN_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "microsoft edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "spotify": r"C:\Users\Public\Desktop\Spotify.lnk",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
    "cmd": "cmd.exe",
    "terminal": "wt.exe",
}


def open_application(app_name: str) -> str:
    """
    Attempt to open an application by name.

    Strategy:
      1. AppOpener fuzzy match (if installed)
      2. Known apps dict → subprocess
      3. subprocess.Popen(app_name) direct

    Returns a descriptive string for TTS/display.
    """
    app_lower = app_name.lower().strip()

    # ---- Strategy 1: AppOpener ----
    if _HAS_APPOPENER:
        try:
            _app_open(app_name, match_closest=True, throw_error=True)
            return f"Opening {app_name}."
        except Exception as e:
            pass  # fall through

    # ---- Strategy 2: Known apps dict ----
    exe = _KNOWN_APPS.get(app_lower)
    if exe:
        try:
            subprocess.Popen(exe, shell=True)
            return f"Opening {app_name}."
        except Exception as e:
            return f"Found {app_name} but could not launch it: {e}"

    # ---- Strategy 3: Direct subprocess ----
    try:
        subprocess.Popen(app_lower, shell=True)
        return f"Trying to open {app_name}."
    except Exception as e:
        return (
            f"I could not find or open '{app_name}'. "
            "Please check the application name and try again."
        )


# ---------------------------------------------------------------------------
# Standalone test — run:  python -m backend.intents.open_app
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_app = "notepad"
    print(f"=== open_app Test: '{test_app}' ===")
    result = open_application(test_app)
    print(f"Result: {result}")
