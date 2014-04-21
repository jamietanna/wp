from abc import ABCMeta, abstractmethod
import config

import os

from generic import *

import subprocess


## <BASE>

class ApplicationWrapper(object):
    __metaclass__ = ABCMeta
    name = ""

    def __init__(self, name):
        super(ApplicationWrapper, self).__init__()
        self.name = name

    def execute(self, args):
        ret = subprocess.call(args)
        if not ret == 0:
            error("Some unknown error occured when executing {}".format(args[0]))

    def getName(self):
        return self.name

    # override if you want a shorter name for the command-line
    def getShortName(self):
        return self.name

class BackgroundManager(ApplicationWrapper):
    def __init__(self, name):
        super(BackgroundManager, self).__init__(name)

    @abstractmethod
    def changeBackground(self, path):
        pass

class ConfigWriter(ApplicationWrapper):

    def __init__(self, name):
        super(ConfigWriter, self).__init__(name)

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

    @abstractmethod
    def onBackgroundChange(self, basePath):
        pass


## </BASE>

class FehWallpaper(BackgroundManager):
    def __init__(self):
        super(FehWallpaper, self).__init__("FEH")

    def changeBackground(self, path):
        self.execute(["feh", "--bg-fill", path])

class GnomeWallpaper(BackgroundManager):
    def __init__(self):
        super(GnomeWallpaper, self).__init__("Gnome Wallpaper Changer")

    def changeBackground(self, path):
        self.execute(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "'file://" + path + "'"])

    def getShortName(self):
        return "GNOMEWP"

## </BG>


## <WM>

class WindowManager(ConfigWriter):
    def __init__(self, name):
        super(WindowManager, self).__init__(name)

    # make this abstract as we don't want the ConfigWriter implementation
    #  as it doesn't affect us, and the WM-specific code won't be similar
    @abstractmethod
    def writeColoursToFile(self, colours):
        pass

class I3WM(WindowManager):
    def __init__(self):
        super(I3WM, self).__init__("I3 Window Manager")
        error("NOTE: I3WM has not been implemented yet. ")

    def formatColoursForFile(self, colours):
        pass

    def writeColoursToFile(self, colours):
        pass

    def getPath(self, basePath):
        return config.HOME_DIR + "/.i3/config"

    def getShortName(self):
        return "I3WM"

    def onBackgroundChange(self, basePath):
        pass

## </WM>

## <Shells>


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

    def onBackgroundChange(self, basePath):
        pass


class GnomeShellColours(ConfigWriter):
    def __init__(self):
        super(GnomeShellColours, self).__init__("Shell Colours (Gnome)")

    def formatColoursForFile(self, colours):
        return ":".join(colours)

    def getPath(self, basePath):
        return config.WP_DIRECTORY + "/." + os.path.basename(basePath) + ".gshcolours"

    def getShortName(self):
        return "GSH"

    def onBackgroundChange(self, basePath):
        with open(self.getPath(basePath)) as f:
            colours = f.read()

        self.execute(["gconftool-2", "--set", "/apps/gnome-terminal/profiles/Default/palette", "--type", "string", colours])


## </Shells>