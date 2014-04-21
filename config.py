import os
from applicationwrappers import *

HOME_DIR = os.path.expanduser('~')
WM    = ["I3",    "X",  "OTHER"]
BG    = [FehWallpaper(), GnomeWallpaper()]
# SHELL = ["GNOME"]
SHELL = [ShellColours(), GnomeShellColours()]
WP_DIRECTORY = HOME_DIR + "/.wp"
WP_CONFIG_FILE = WP_DIRECTORY + "/.config"

