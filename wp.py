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

    WM = -1
    BG = -1

    # enumerateChoices(sys.argv)

    if len(sys.argv) == 4:
        WM = sys.argv[2]
        BG = sys.argv[3]
    else:
        WMi = enumerateChoices(config.WM)
        WM = config.WM[int(WMi)]
        BGi = enumerateChoices(config.BG)
        BG = config.BG[int(BGi)]
    
    config_file = ConfigParser.RawConfigParser()
    config_file.add_section("wp")

    indent("You chose " + WM)
    config_file.set("wp", "WindowManager", WM)
    
    indent("You chose " + BG)
    config_file.set("wp", "BackgroundManager", BG)
    
    with open(config.WP_CONFIG_FILE, 'wb') as config_file_:
        config_file.write(config_file_)


    indent("Setup!")
    pass

def main():
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) > 1:
        if os.path.isdir(config.WP_DIRECTORY):
            if not os.path.exists(config.WP_CONFIG_FILE):
                setup()
        else:
            os.makedirs(config.WP_DIRECTORY)
            setup()
        
        cmd = sys.argv[1].lower()
        if cmd == "setup":
            setup()



if __name__ == "__main__":
    main()



