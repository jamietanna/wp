from abc import ABCMeta, abstractmethod
import config

from generic import *

import subprocess

class WallpaperChanger(object):
    __metaclass__ = ABCMeta
    name = ""

    def __init__(self, name):
        super(WallpaperChanger, self).__init__()
        self.name = name

    @abstractmethod
    def changeBackground(self, path):
        pass

    def getName(self):
        return name

    # override if you want a shorter name for the command-line
    def getShortName(self):
        return name

    def execute(self, args):
        ret = subprocess.call(args)
        if not ret == 0:
            error("Some unknown error occured when changing background. ")

class FehWallpaper(WallpaperChanger):
    def __init__(self):
        super(FehWallpaper, self).__init__("FEH")

    def changeBackground(self, path):
        self.execute(["feh", "--bg-fill", path])

class GnomeWallpaper(WallpaperChanger):
    def __init__(self):
        super(GnomeWallpaper, self).__init__("Gnome Wallpaper Changer")

    def changeBackground(self, path):
        self.execute(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "'file://" + path + "'"])

    def getShortName(self):
        return "GnomeWP"




class ConfigWriter(object):
    __metaclass__ = ABCMeta
    name = ""

    def __init__(self, name):
        super(ConfigWriter, self).__init__()
        self.name = name
        

    def getName(self):
        return name

    # override if you want a shorter name for the command-line
    def getShortName(self):
        return name

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
    def afterWrite(self, basePath):
        pass

# TODO: where is this actually used?
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

    def getShortName(self):
        return "SH"

class GnomeShellColours(ConfigWriter):
    def __init__(self):
        super(GnomeShellColours, self).__init__("Shell Colours (Gnome)")

    def formatColoursForFile(self, colours):
        return ":".join(colours)

    def getPath(self, basePath):
        return config.WP_DIRECTORY + "/." + basePath + ".gshcolours"

    def getShortName(self):
        return "GSH"

