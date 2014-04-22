# wp

`wp` is a tool to change your background, and update your system colours based on the background. 

## Credits
This is a rewrite in Python 2 of the version by [Caleb Everett](https://github.com/everett1992/wp). The files [colorz.py](colorz.py) and [colour.py](colour.py) are *predominantly* his. 

## Dependencies
> *As far as I know this only relies on PIL, python image library. I was able to fulfill this dependency with the `python-pillow` package on Arch Linux. On other systems, `pip install Pillow`.*
From [Caleb's README](https://github.com/everett1992/wp/blob/master/README.md#dependencies).

Please note that this has only been tested on Ubuntu 13.10, and not on any other setup. If there are any issues, please submit an issue ticket and I will try and correct any issues. 

## Features

At time of writing, `wp` supports the following Window Managers:

- I3 WM
    - NOTE: I3 filler code is in effect, but has not been implemented yet. This will be soon to come. 

`wp` supports the following shell types:

- Gnome shell

`wp` supports the following background managers:

- FEH
- Gnome

In order to access `wp` from any directory, add the following line to your `.bashrc` or `.zshrc`:
```
alias wp="/path/to/wp/directory/wp"
```


### Commands

#### Setup

In order to actually use `wp` you will need to run `wp setup`. This will create the config file and folder, and allow you to start populating the folder with your own wallpapers. 

```
$ wp setup
```

Note that you will need to run a `wp refresh` if you've changed your existing settings. 

#### Add

In order to add a new file to the system, you will need to run `wp add`, passing file(s) as arguments. 
```
$ wp add [file]

$ wp add ~/Pictures/img.png

```

This will generate the appropriate config files in the `~/.wp` directory, and allow you to change to that file. 


#### Change

Change the background and update system colours as per config. 
```
$ wp change
```

#### Refresh

Effectively call `wp add` for all files in your `~/.wp` directory. Useful if you've manually copied files in, or if you've changed your config file/run `wp setup`.
```
wp refresh
```


## Open for Extension

If you have something you'd like to be done differently, or you'd like to add your own shell or window/background manager, then please fork the project and add your own functionality. Finally, please send in your pull requests!

Also, if you find any problems, please send me an issue so I can work on fixing them; or if you've fixed them, send me a pull request. 

### Adding a new Shell

In [applicationwrappers.py](applicationwrappers.py), create a new class extending `Configwriter` and implementing the abstract methods:

- `format_colours_for_file()`
- `get_path()`
- `on_background_change()`
- *possibly* `get_short_name()`. 

### Adding a new Window Manager

In [applicationwrappers.py](applicationwrappers.py), create a new class extending `Windowmanager` and implementing the abstract methods:

- `format_colours_for_file()`
- `write_colours_to_file()`
- `get_path()`
- `on_background_change()`
- *possibly* `get_short_name()`


### Adding a new Background Manager

In [applicationwrappers.py](applicationwrappers.py), create a new class extending `Backgroundmanager` and implementing the abstract methods:

- `change_background()`
- *possibly* `get_short_name()`

### Sending Pull Requests

Before sending a pull request, please run `pylint` on the code you're submitting. This is so that we can ensure all code is well structured. 