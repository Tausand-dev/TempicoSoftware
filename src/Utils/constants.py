#File of constants for scripts
import sys
import os

STOP_MASK_MAX = 4000  # 4ms

STOP_MASK_MIN_TP1004_FALLBACK = 0.0
STOP_MASK_MIN_TP1204_FALLBACK = -0.25

STOP_MASK_DECIMALS = 2 
STOP_MASK_STEP = 0.01


def get_stop_mask_range(device):
    """
    Returns the (minimum, maximum) stopMask values allowed, in us, for the
    connected Tempico device.

    The minimum is queried directly from the device via
    device.getStopMaskMinimum() (pyTempico >= 2.0.2), so it always matches
    the real hardware/firmware limit instead of a hardcoded constant that
    can go out of sync with future models or firmware revisions.

    :param device: an open pyTempico.TempicoDevice instance
    :return: tuple (minimum, maximum) in microseconds
    """
    try:
        minimum = device.getStopMaskMinimum()
    except Exception:
        # Fallback: assume the more permissive TP12 range if the device
        # can't answer the query for some reason.
        model_idn = device.getModelIdn()
        minimum = STOP_MASK_MIN_TP1204_FALLBACK if "TP12" in model_idn else STOP_MASK_MIN_TP1004_FALLBACK
    return (minimum, STOP_MASK_MAX)

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
VERSION = "2.1.1"
PYTEMPICO_VERSION = "2.0.4"
BANNER = os.path.join(BASE_PATH, "Sources", "splash.png")
#Create the taskbarIcon for windows with ctypes
APPID = "tempico.tempico.01"
OVERFLOW_PARAMETER = -1
VERSION_PARAMETER = ""
#Links used in the "Help" menu (About / Github)
WEBSITE_LINK = "https://www.tausand.com/"
GITHUB_LINK = "https://github.com/Tausand-dev/TempicoSoftware"