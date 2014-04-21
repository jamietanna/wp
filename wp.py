#!/usr/bin/python

import sys
import os
import signal
import ConfigParser
import shutil

import colour
import config

from generic import *

_WM    = ""
_BG    = ""
_SHELL = ""

# SO 1112343
def signal_handler(signal, frame):
    print
    error("User cancelled operation(s). ")
    error("Now exiting. ")
    sys.exit(1)

def populateSettings():
    config_file = ConfigParser.ConfigParser()
    config_file.read(config.WP_CONFIG_FILE)
    global _WM, _BG

    _WM    = config_file.get("wp", "windowmanager")
    _BG    = config_file.get("wp", "backgroundmanager")
    try:
        _SHELL = config_file.get("wp", "shell")
    except:
        error("No valid shell in config, please run setup again.")
        sys.exit(1)


def setup():
    # WM=(I3|OTHER)
    # BG=(GNOME|FEH)
    # 

    WM = -1
    BG = -1
    SH = -1

    anyErrors = False

    # enumerateChoices(sys.argv)
    
    _shells = []
    for s in config.SHELL:
        _shells.append(s.getShortName())

    if len(sys.argv) == 5:
        if sys.argv[2].upper() in config.WM:
            WM = sys.argv[2].upper()
        else:
            error("Invalid Window Manager")
            anyErrors = True

        if sys.argv[3].upper() in config.BG:
            BG = sys.argv[3].upper()
        else:
            error("Invalid Background Manager")
            anyErrors = True

        if sys.argv[4].upper() in _shells:
            SH = sys.argv[4].upper()
        else:
            error("Invalid Background Manager")
            anyErrors = True

    else:
        WMi = enumerateChoices(config.WM)
        WM  = config.WM[int(WMi)]
        BGi = enumerateChoices(config.BG)
        BG  = config.BG[int(BGi)]
        SHi = enumerateChoices(_shells)
        SH  = config.SHELL[int(SHi)].getShortName()
        output(SH)

    config_file = ConfigParser.RawConfigParser()
    config_file.add_section("wp")

    config_file.set("wp", "WindowManager",      WM)
    config_file.set("wp", "BackgroundManager",  BG)
    config_file.set("wp", "Shell",              SH)
    
    if not anyErrors:
        with open(config.WP_CONFIG_FILE, 'wb') as config_file_:
            config_file.write(config_file_)

    pass

def usage():
    print """
    wp
    Usage: {0}
                setup [WM] [BGM]        Run setup, with optional WindowManager and BackgroundManager
                add file1 [file2 ...]   Add file(s), and generate metadata files
    """.format(sys.argv[0])

def addAFile(oldPath):
    path      = config.WP_DIRECTORY + "/" + os.path.basename(oldPath)
    path_meta = config.WP_DIRECTORY + "/." + os.path.basename(oldPath)

    shutil.copy(oldPath, path)

    # print colour.colourz(path)
    colours = colour.getColours(path)

    print ":::: WM = " + _WM
    print ":::: BG = " + _BG

    temp   = ""
    shcols = ""

    for idx, c in enumerate(colours):
        if _WM == "I3":
            pass
        elif _WM == "X":
            temp += """*color{}: {}\n""".format(idx, c)
        elif _WM == "OTHER":
            pass
        shcols += """export COLOR{}="{}"\n""".format(idx, c)
    
    # with open(path_meta + ".shcolours", "w") as f:
    #     f.write(shcols)

    _SHELL.writeColoursToFile(colours, os.path.basename(oldPath))

    print "FINAL: \n\033[93m" + temp + "\033[0m"

def add():
    for idx, f in enumerate(sys.argv):
        if idx > 1:
            addAFile(f)

def main():

    signal.signal(signal.SIGINT, signal_handler)

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

    if len(sys.argv) > 1:
        
        cmd = sys.argv[1].lower()
        if cmd == "setup":
            setup()
        else:
            if os.path.isdir(config.WP_DIRECTORY):
                if not os.path.exists(config.WP_CONFIG_FILE):
                    setup()
            else:
                os.makedirs(config.WP_DIRECTORY)
                setup()
            # do rest of 'switch' statement

            populateSettings()

            if cmd == "add":
                add()
            
    else:
        usage()

if __name__ == "__main__":
    main()



