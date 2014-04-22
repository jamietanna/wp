"""
The below classes define the main functionality of the wp tool. For more details
 on adding your own, check out README.md.
"""
from abc import ABCMeta, abstractmethod
import config

import os

from generic import error, execute

## <BASE>

class application_wrapper(object):
    """
    A default base class for all wp classes - define some standard methods, and
     make sure the interpreter knows that we're using an abstract class. 
    """
    __metaclass__ = ABCMeta
    name = ""

    def __init__(self, name):
        super(application_wrapper, self).__init__()
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

class background_manager(application_wrapper):
    """
    A class to execute the system commands depending on background manager used.
    """
    def __init__(self, name):
        super(background_manager, self).__init__(name)

    @abstractmethod
    def change_background(self, path):
        """
        Change the background to the new one. 
        """
        pass

class config_writer(application_wrapper):
    """
    A class to handle the writing of colours to a config file in a specific 
     format (format_colours_for_file())
    """

    def __init__(self, name):
        super(config_writer, self).__init__(name)

    def write_colours_to_file(self, colours, base_path):
        """
        Write colours to the correct path, in the correct format. 
        """
        colours_for_file = self.format_colours_for_file(colours)
        with open(self.get_path(base_path), 'w') as f:
            f.write(colours_for_file)

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

class feh_wallpaper(background_manager):
    """
    Update the background using the feh tool. 
    """
    def __init__(self):
        super(feh_wallpaper, self).__init__("FEH")

    def change_background(self, path):
        execute(["feh", "--bg-fill", path])

class gnome_wallpaper(background_manager):
    """
    Update the background using the gnome desktop background settings. 
    """
    def __init__(self):
        super(gnome_wallpaper, self).__init__("Gnome Wallpaper Changer")

    def change_background(self, path):
        execute(["gsettings", "set", "org.gnome.desktop.background", 
                      "picture-uri", "'file://" + path + "'"])

    def get_short_name(self):
        return "GNOMEWP"

## </BG>


## <WM>

class window_manager(config_writer):
    """
    Update the colours for the standard Window Manager for the system.
    """
    def __init__(self, name):
        super(window_manager, self).__init__(name)

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

class i3wm(window_manager):
    """
    Update the I3WM colours. 
    """
    def __init__(self):
        super(i3wm, self).__init__("I3 Window Manager")
        error("NOTE: I3WM has not been implemented yet. ")

    def format_colours_for_file(self, colours):
        pass

    def write_colours_to_file(self, colours, _ ):
        pass

    def get_path(self, base_path):
        return config.HOME_DIR + "/.i3/config"

    def get_short_name(self):
        return "I3WM"

    def on_background_change(self, base_path):
        pass

## </WM>

## <Shells>


class shell_colours(config_writer):
    """
    The colours for ????
    TODO: where is this actually used?  
    """
    def __init__(self):
        super(shell_colours, self).__init__("Shell Colours")

    def format_colours_for_file(self, colours):
        shcols = ""
        for idx, c in enumerate(colours):
            shcols += """export COLOR{}="{}"\n""".format(idx, c)
        return shcols

    def get_path(self, base_path):
        return config.WP_DIRECTORY + "/." + base_path + ".shcolours"

    def get_short_name(self):
        return "SH"

    def on_background_change(self, base_path):
        pass


class gnome_shell_colours(config_writer):
    """
    The colours that are used with gnome-shell in i.e. Ubuntu. 
    """
    def __init__(self):
        super(gnome_shell_colours, self).__init__("Shell Colours (Gnome)")

    def format_colours_for_file(self, colours):
        return ":".join(colours)

    def get_path(self, base_path):
        return config.WP_DIRECTORY + "/." + os.path.basename(base_path) \
                + ".gshcolours"

    def get_short_name(self):
        return "GSH"

    def on_background_change(self, base_path):
        with open(self.get_path(base_path)) as f:
            colours = f.read()

        execute(["gconftool-2", "--set", 
            "/apps/gnome-terminal/profiles/Default/palette", "--type", 
            "string", colours])


## </Shells>



WM    = [i3wm()]
BG    = [feh_wallpaper(), gnome_wallpaper()]
SHELL = [shell_colours(), gnome_shell_colours()]
