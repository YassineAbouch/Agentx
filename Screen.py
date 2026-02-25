# Screen.py
# Windows: list open windows + active window + take screenshot
# Optional: list Chrome tabs if Chrome is started with --remote-debugging-port=9222

import os
import time
import json
from datetime import datetime

import psutil
import win32gui
import win32process
import win32con

import mss
from PIL import Image

# Optional (for Chrome tabs)
try:
    import requests
except Exception:
    requests = None


def _is_visible_window(hwnd: int) -> bool:
    """Return True if the window is visible and has a title."""
    if not win32gui.IsWindowVisible(hwnd):
        return False
    title = win32gui.GetWindowText(hwnd).strip()
    if not title:
        return False
    # Filter out tool windows / tiny helper windows if needed:
    # style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    # if style & win32con.WS_EX_TOOLWINDOW:
    #     return False
    return True


def list_open_windows():
    """Enumerate top-level visible windows and return structured data."""
    windows = []

    def enum_handler(hwnd, _):
        if not _is_visible_window(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()
        rect = win32gui.GetWindowRect(hwnd)  # (left, top, right, bottom)
        left, top, right, bottom = rect
        width = max(0, right - left)
        height = max(0, bottom - top)

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        proc_name = "unknown"
        exe = None
        try:
            p = psutil.Process(pid)
            proc_name = p.name()
            exe = p.exe()
        except Exception:
            pass

        windows.append(
            {
                "hwnd": int(hwnd),
                "title": title,
                "pid": int(pid),
                "process": proc_name,
                "exe": exe,
                "bounds": {"x": left, "y": top, "w": width, "h": height},
            }
        )

    win32gui.EnumWindows(enum_handler, None)
    return windows


def get_active_window():
    """Return active window info or None."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None

    title = win32gui.GetWindowText(hwnd).strip()
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = max(0, right - left)
    height = max(0, bottom - top)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    proc_name = "unknown"
    exe = None
    try:
        p = psutil.Process(pid)
        proc_name = p.name()
        exe = p.exe()
    except Exception:
        pass

    return {
        "hwnd": int(hwnd),
        "title": title,
        "pid": int(pid),
        "process": proc_name,
        "exe": exe,
        "bounds": {"x": left, "y": top, "w": width, "h": height},
    }


def take_screenshot(output_path="screenshot.png"):
    """Take a full-screen screenshot and save it."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        shot = sct.grab(monitor)
        img = Image.frombytes("RGB", shot.size, shot.rgb)
        img.save(output_path)
    return os.path.abspath(output_path)


def list_chrome_tabs(debug_port=9222):
    """
    List Chrome tabs using the remote debugging endpoint.
    Chrome must be started with: --remote-debugging-port=9222
    """
    if requests is None:
        return {"error": "requests not installed. Run: pip install requests"}

    url = f"http://127.0.0.1:{debug_port}/json"
    try:
        r = requests.get(url, timeout=2)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {
            "error": "Could not connect to Chrome remote debugging. "
                     "Start Chrome with --remote-debugging-port=9222",
            "details": str(e),
        }

    tabs = []
    for item in data:
        if item.get("type") == "page":
            tabs.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "id": item.get("id"),
                    "webSocketDebuggerUrl": item.get("webSocketDebuggerUrl"),
                }
            )
    return {"debug_port": debug_port, "tabs": tabs}


def main():
    print("Starting Screen.py ...")
    time.sleep(1)

    windows = list_open_windows()
    active = get_active_window()
    screenshot_path = take_screenshot("screenshot.png")

    # Optional Chrome tabs
    chrome_tabs = list_chrome_tabs(9222)

    report = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "active_window": active,
        "open_windows": windows,
        "screenshot_file": screenshot_path,
        "chrome_tabs": chrome_tabs,
    }

    # Save a JSON report
    with open("screen_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Screenshot saved: {screenshot_path}")
    print("✅ Report saved: screen_report.json")

    # Quick console summary
    print(f"\nActive window: {active['process']} — {active['title']}" if active else "\nActive window: None")
    print(f"Open windows found: {len(windows)}")

    if isinstance(chrome_tabs, dict) and "tabs" in chrome_tabs:
        print(f"Chrome tabs found: {len(chrome_tabs['tabs'])}")
        for i, t in enumerate(chrome_tabs["tabs"][:10], 1):
            print(f"  {i}. {t.get('title')}  |  {t.get('url')}")
    else:
        # error message if any
        if isinstance(chrome_tabs, dict) and chrome_tabs.get("error"):
            print(f"\nChrome tabs: ❌ {chrome_tabs['error']}")
            if chrome_tabs.get("details"):
                print(f"Details: {chrome_tabs['details']}")


if __name__ == "__main__":
    main()
