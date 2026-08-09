#File of constants for scripts
import sys
import os

STOP_MASK_MIN_TP1004 = 0.0  # 12 ns rounds to 0 at us resolution
STOP_MASK_MAX_TP1004 = 4000  # 4ms

STOP_MASK_MIN_TP1204 = -0.25  # -250ns
STOP_MASK_MAX_TP1204 = 4000  # 4ms

STOP_MASK_DECIMALS = 2 
STOP_MASK_STEP = 0.01


def get_stop_mask_range(model_idn):
    """
    Returns the (minimum, maximum) stopMask values allowed, in us, for the connected Tempico device.

    :param model_idn: string from device.getModelIdn(), e.g. "TP1204"
    :return: tuple (minimum, maximum) in microseconds
    """
    if "TP12" in model_idn:
        return (STOP_MASK_MIN_TP1204, STOP_MASK_MAX_TP1204)
    return (STOP_MASK_MIN_TP1004, STOP_MASK_MAX_TP1004)

def _get_base_path():
    """
    Returns the folder that should be used as the base to locate the
    'Sources' folder (icons, splash image, etc).

    This is resolved against the executable/script location instead of the
    current working directory, so it works no matter how the app is
    launched (terminal, double click, .desktop entry, AppImage, etc).

    - If frozen with PyInstaller (onefile or onedir): the folder that
      contains the compiled executable (Sources is copied next to it).
    - If running from source: this file (Utils/constants.py, or
      src/Utils/constants.py, etc) is not necessarily next to 'Sources'.
      Instead of assuming a fixed number of parent folders, walk up the
      tree until a folder containing 'Sources' is found. This keeps
      working no matter how deep constants.py is nested in the project.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))

    current = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(current, "Sources")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            # Reached filesystem root without finding 'Sources'; fall back
            # to the folder containing this file (previous behavior).
            return os.path.dirname(os.path.abspath(__file__))
        current = parent


BASE_PATH = _get_base_path()

ICON_LOCATION = os.path.join(BASE_PATH, "Sources", "tausand_small.ico")
VERSION = "2.1.0"
PYTEMPICO_VERSION = "2.0.4"
BANNER = os.path.join(BASE_PATH, "Sources", "splash.png")
#Create the taskbarIcon for windows with ctypes
APPID = "tempico.tempico.01"
OVERFLOW_PARAMETER = -1
VERSION_PARAMETER = ""
#Links used in the "Help" menu (About / Github)
WEBSITE_LINK = "https://www.tausand.com/"
GITHUB_LINK = "https://github.com/Tausand-dev/TempicoSoftware"