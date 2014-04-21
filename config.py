"""
Config settings for the wp application. 
"""

import os


HOME_DIR = os.path.expanduser('~')
WP_DIRECTORY = HOME_DIR + "/.wp"
ALLOWED_FILE_EXTS = ['.png', '.jpg']
WP_CONFIG_FILE = WP_DIRECTORY + "/.config"
WP_CONFIG_SECTION = "wp"
IS_DEBUG_MODE = True
INDENT_STR = ":: "