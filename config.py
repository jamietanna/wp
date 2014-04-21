"""
Config settings for the wp application. 
"""

import os
from applicationwrappers import FehWallpaper, GnomeWallpaper, ShellColours, \
                                GnomeShellColours, I3WM

HOME_DIR = os.path.expanduser('~')
WM    = [I3WM()]
BG    = [FehWallpaper(), GnomeWallpaper()]
SHELL = [ShellColours(), GnomeShellColours()]
WP_DIRECTORY = HOME_DIR + "/.wp"
ALLOWED_FILE_EXTS = ['.png', '.jpg']
WP_CONFIG_FILE = WP_DIRECTORY + "/.config"
WP_CONFIG_SECTION = "wp"
IS_DEBUG_MODE = True
INDENT_STR = ":: "