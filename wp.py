#!/usr/bin/python

import sys
import os

import signal

import ConfigParser

import shutil

import colour

_WM = ""
_BG = ""

from abc import ABCMeta, abstractmethod

# SO 1112343
def signal_handler(signal, frame):
    print
    error("User cancelled operation(s). ")
    error("Now exiting. ")
    sys.exit(1)

class ConfigWriter(object):
    __metaclass__ = ABCMeta
    __name = ""

    def __init__(self, name):
        super(ConfigWriter, self).__init__()
        __name = name

    def getName(self):
        return __name

    def writeColoursToFile(self, colours, basePath):
        coloursForFile = self.formatColoursForFile(colours)
        with open(self.getPath(basePath), 'w') as f:
            f.write(coloursForFile)
        self.afterWrite(basePath)

    @abstractmethod
    def formatColoursForFile(self, colours):
        pass

    @abstractmethod
    def getPath(self, basePath):
        pass

    # blank function to be overriden if need to have anything that runs after we've written i.e. symlinks
    def afterWrite(self):
        pass

class ShellColours(ConfigWriter):
    def __init__(self):
        super(ShellColours, self).__init__("Shell Colours")

    def formatColoursForFile(self, colours):
        shcols = ""
        for idx, c in enumerate(colours):
            shcols += """export COLOR{}="{}"\n""".format(idx, c)
        return shcols

    def getPath(self, basePath):
        return config.WP_DIRECTORY + "/." + basePath + ".shcolours"

    def afterWrite(self, basePath):
        # TODO : move to the change functions
        # SYM_PATH = config.HOME_DIR + "/.colours"

        # if os.path.exists(SYM_PATH):
        #     os.remove(SYM_PATH)

        # os.symlink(self.getPath(basePath), SYM_PATH)


SHELL_COLOURS = ShellColours()

class config:
    HOME_DIR = os.path.expanduser('~')
    WM = ["I3",    "X",  "OTHER"]
    BG = ["GNOME", "FEH"]
    WP_DIRECTORY = HOME_DIR + "/.wp"
    WP_CONFIG_FILE = WP_DIRECTORY + "/.config"
    INDENT = ":: "

def indent(toPrint, colour):
    print colour + config.INDENT + str(toPrint) + "\033[0m"

def output(toPrint):
    indent(toPrint, "\033[91m")

def error(toPrint):
    indent("Error: " + str(toPrint), "\033[92m")

def enumerateChoices(var):
    
    invalidInput = True
    idxi = -1

    while True:
        for ndx, val in enumerate(var):
            output( `ndx` + ") " + val)
        opt_idx = raw_input("Please enter an option: ")
        
        idxi = int(opt_idx)

        if idxi >= 0 and idxi < len(var):
            break
        else:
            error("Please enter a valid option. ")

    return idxi

def populateSettings():
    config_file = ConfigParser.ConfigParser()
    config_file.read(config.WP_CONFIG_FILE)
    global _WM, _BG

    _WM = config_file.get("wp", "windowmanager")
    _BG = config_file.get("wp", "backgroundmanager")



def setup():
    # WM=(I3|OTHER)
    # BG=(GNOME|FEH)
    # 

    WM = -1
    BG = -1

    anyErrors = False

    # enumerateChoices(sys.argv)

    if len(sys.argv) == 4:
        if sys.argv[2].upper() in config.WM:
            WM = sys.argv[2]
        else:
            error("Invalid Window Manager")
            anyErrors = True

        if sys.argv[3].upper() in config.BG:
            BG = sys.argv[3]
        else:
            error("Invalid Background Manager")
            anyErrors = True

    else:
        WMi = enumerateChoices(config.WM)
        WM  = config.WM[int(WMi)]
        BGi = enumerateChoices(config.BG)
        BG  = config.BG[int(BGi)]
    
    config_file = ConfigParser.RawConfigParser()
    config_file.add_section("wp")

    config_file.set("wp", "WindowManager", WM)
    
    config_file.set("wp", "BackgroundManager", BG)
    
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
    path_meta =  config.WP_DIRECTORY + "/." + os.path.basename(oldPath)

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

    SHELL_COLOURS.writeColoursToFile(colours, os.path.basename(oldPath))


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



