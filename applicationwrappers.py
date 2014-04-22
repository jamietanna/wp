from abc import ABCMeta, abstractmethod
import config

import os

from generic import error, execute

## <BASE>

class application_wrapper(object):
    __metaclass__ = ABCMeta
    name = ""

    def __init__(self, name):
        super(application_wrapper, self).__init__()
        self.name = name


    def get_name(self):
        return self.name

    # override if you want a shorter name for the command-line
    def get_short_name(self):
        return self.name

class background_manager(application_wrapper):
    def __init__(self, name):
        super(background_manager, self).__init__(name)

    @abstractmethod
    def change_background(self, path):
        pass

class config_writer(application_wrapper):

    def __init__(self, name):
        super(config_writer, self).__init__(name)

    def write_colours_to_file(self, colours, base_path):
        colours_for_file = self.format_colours_for_file(colours)
        with open(self.get_path(base_path), 'w') as f:
            f.write(colours_for_file)
        self.after_write(base_path)

    @abstractmethod
    def format_colours_for_file(self, colours):
        pass

    @abstractmethod
    def get_path(self, base_path):
        pass

    # blank function to be overriden if need to have anything that runs 
    #  after we've written i.e. symlinks
    def after_write(self, base_path):
        pass

    @abstractmethod
    def on_background_change(self, base_path):
        pass


## </BASE>

class feh_wallpaper(background_manager):
    def __init__(self):
        super(feh_wallpaper, self).__init__("FEH")

    def change_background(self, path):
        execute(["feh", "--bg-fill", path])

class gnome_wallpaper(background_manager):
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
    def __init__(self, name):
        super(window_manager, self).__init__(name)

    # make this abstract as we don't want the Config_writer implementation
    #  as it doesn't affect us, and the WM-specific code won't be similar
    @abstractmethod
    def write_colours_to_file(self, colours):
        pass

class i3wm(window_manager):
    def __init__(self):
        super(i3wm, self).__init__("I3 Window Manager")
        error("NOTE: I3WM has not been implemented yet. ")

    def format_colours_for_file(self, colours):
        pass

    def write_colours_to_file(self, colours):
        pass

    def get_path(self, base_path):
        return config.HOME_DIR + "/.i3/config"

    def get_short_name(self):
        return "I3WM"

    def on_background_change(self, base_path):
        pass

## </WM>

## <Shells>


# TODO: where is this actually used?
class shell_colours(config_writer):
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
