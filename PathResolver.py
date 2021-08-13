import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    if sys.platform.startswith('linux'):
        path = relative_path
    else:
        path = relative_path.replace("/", "\\")

    return os.path.join(base_path, path)

