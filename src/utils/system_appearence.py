import subprocess
import platform


def detect_system_appearance():
    system = platform.system()
    if system == "Windows":
        return get_windows_appearance()
    elif system == "Darwin":  # macOS
        return get_macos_appearance()
    elif system == "Linux":
        return get_linux_appearance()
    return "Unknown"


def get_linux_appearance():
    try:
        output = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        theme = output.stdout.strip().lower()
        return "Dark" if "dark" in theme else "Light"
    except Exception as e:
        return f"Error detecting appearance: {e}"


def get_macos_appearance():
    try:
        output = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return "Dark" if "Dark" in output.stdout else "Light"
    except Exception as e:
        return "Light"  # Defaults to Light if the key doesn't exist


def get_windows_appearance():
    import winreg
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "Light" if value == 1 else "Dark"
    except Exception as e:
        return f"Error detecting appearance: {e}"
