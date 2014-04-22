"""
The below classes define the main functionality of the wp tool. For more details
 on adding your own, check out README.md.
"""
from abc import ABCMeta, abstractmethod
import config

import os

from generic import error, execute

## <BASE>

class Applicationwrapper(object):
    """
    A default base class for all wp classes - define some standard methods, and
     make sure the interpreter knows that we're using an abstract class. 
    """
    __metaclass__ = ABCMeta
    name = ""

    def __init__(self, name):
        super(Applicationwrapper, self).__init__()
        self.name = name


    def get_name(self):
        """
        Get the full descriptive name of the class. 
        """
        return self.name

    def get_short_name(self):
        """
        Get the short name of the class. 

        NOTE: By default, returns the full name. Need to override as 
               appropriate.
        """
        return self.name

class Backgroundmanager(Applicationwrapper):
    """
    A class to execute the system commands depending on background manager used.
    """
    def __init__(self, name):
        super(Backgroundmanager, self).__init__(name)

    @abstractmethod
    def change_background(self, path):
        """
        Change the background to the new one. 
        """
        pass

class Configwriter(Applicationwrapper):
    """
    A class to handle the writing of colours to a config file in a specific 
     format (format_colours_for_file())
    """

    def __init__(self, name):
        super(Configwriter, self).__init__(name)

    def write_colours_to_file(self, colours, base_path):
        """
        Write colours to the correct path, in the correct format. 
        """
        colours_for_file = self.format_colours_for_file(colours)
        with open(self.get_path(base_path), 'w') as config_file:
            config_file.write(colours_for_file)

    @abstractmethod
    def format_colours_for_file(self, colours):
        """
        Return the correct format for current config type. 
        """
        pass

    @abstractmethod
    def get_path(self, base_path):
        """
        Return the path the current config type is to write to. 
        """
        pass

    @abstractmethod
    def on_background_change(self, base_path):
        """
        Update the system to reflect the background has changed. 
        """
        pass


## </BASE>

class Fehwallpaper(Backgroundmanager):
    """
    Update the background using the feh tool. 
    """
    def __init__(self):
        super(Fehwallpaper, self).__init__("FEH")

    def change_background(self, path):
        execute(["feh", "--bg-fill", path])

class Gnomewallpaper(Backgroundmanager):
    """
    Update the background using the gnome desktop background settings. 
    """
    def __init__(self):
        super(Gnomewallpaper, self).__init__("Gnome Wallpaper Changer")

    def change_background(self, path):
        execute(["gsettings", "set", "org.gnome.desktop.background", 
                      "picture-uri", "'file://" + path + "'"])

    def get_short_name(self):
        return "GNOMEWP"

## </BG>


## <WM>

class Windowmanager(Configwriter):
    """
    Update the colours for the standard Window Manager for the system.
    """
    def __init__(self, name):
        super(Windowmanager, self).__init__(name)

    # 
    # 
    @abstractmethod
    def write_colours_to_file(self, colours, _ ):
        """
        Write colours to the correct path, in the correct format. 
        
        NOTE: Make this abstract as we don't want the Config_Writer
               implementation as it doesn't affect us, and the WM-specific
               code won't be similar
        """
        pass

class I3wm(Windowmanager):
    """
    Update the I3WM colours. 
    """
    def __init__(self):
        super(I3wm, self).__init__("I3 Window Manager")
        error("NOTE: I3WM has not been implemented yet. ")

    def format_colours_for_file(self, colours):
        error("NOTE: I3WM has not been implemented yet. ")
        pass

    def write_colours_to_file(self, colours, _ ):
        error("NOTE: I3WM has not been implemented yet. ")
        pass

    def get_path(self, base_path):
        return config.HOME_DIR + "/.i3/config"

    def get_short_name(self):
        return "I3WM"

    def on_background_change(self, base_path):
        error("NOTE: I3WM has not been implemented yet. ")
        pass

## </WM>

## <Shells>


class Shellcolours(Configwriter):
    """
    The colours for ????
    TODO: where is this actually used?  
    """
    def __init__(self):
        super(Shellcolours, self).__init__("Shell Colours")

    def format_colours_for_file(self, colours):
        shcols = ""
        for idx, colour in enumerate(colours):
            shcols += """export COLOR{}="{}"\n""".format(idx, colour)
        return shcols

    def get_path(self, base_path):
        return config.WP_DIRECTORY + "/." + base_path + ".shcolours"

    def get_short_name(self):
        return "SH"

    def on_background_change(self, base_path):
        pass

class Gnomeshellcolours(Configwriter):
    """
    The colours that are used with gnome-shell in i.e. Ubuntu. 
    """
    def __init__(self):
        super(Gnomeshellcolours, self).__init__("Shell Colours (Gnome)")

    def format_colours_for_file(self, colours):
        return ":".join(colours)

    def get_path(self, base_path):
        return config.WP_DIRECTORY + "/." + os.path.basename(base_path) \
                + ".gshcolours"

    def get_short_name(self):
        return "GSH"

    def on_background_change(self, base_path):
        with open(self.get_path(base_path)) as config_file:
            colours = config_file.read()

        execute(["gconftool-2", "--set", 
            "/apps/gnome-terminal/profiles/Default/palette", "--type", 
            "string", colours])


## </Shells>



WM    = [I3wm()]
BG    = [Fehwallpaper(), Gnomewallpaper()]
SHELL = [Shellcolours(), Gnomeshellcolours()]
