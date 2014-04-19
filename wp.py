#!/usr/bin/python

import sys
import os

import ConfigParser

class config:
    class wm:
        I3    = 1
        OTHER = 2
    class bg:
        GNOME = 1
        FEH   = 2
    WM = ["I3",    "OTHER"]
    BG = ["GNOME", "FEH"]
    WP_DIRECTORY = os.path.expanduser('~') + "/.wp"
    WP_CONFIG_FILE = WP_DIRECTORY + "/.config"

def indent(strToPrint):
    print "\033[91m:: " + strToPrint + "\033[0m"

def enumerateChoices(var):
    for ndx, val in enumerate(var):
        indent( `ndx` + ") " + val)
    return raw_input("Please enter an option: ")


def setup():
    # WM=(I3|OTHER)
    # BG=(GNOME|FEH)
    # 

    config_file = ConfigParser.RawConfigParser()
    config_file.add_section("wp")

    WM = enumerateChoices(config.WM)
    indent("You chose " + config.WM[int(WM)])
    config_file.set("wp", "WindowManager", config.WM[int(WM)])
    
    BG = enumerateChoices(config.BG)
    indent("You chose " + config.BG[int(BG)])
    config_file.set("wp", "BackgroundManager", config.BG[int(BG)])
    
    with open(config.WP_CONFIG_FILE, 'wb') as config_file_:
        config_file.write(config_file_)


    indent("Setup!")
    pass

def main():
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    if os.path.isdir(config.WP_DIRECTORY):
        if not os.path.exists(config.WP_CONFIG_FILE):
            setup()
    else:
        os.makedirs(config.WP_DIRECTORY)
        setup()

if __name__ == "__main__":
    main()



