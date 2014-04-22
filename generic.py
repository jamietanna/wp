"""
Functions that don't need to necessarily be left in the main application code, 
 but could be used for more general programs. 
"""

# pylint: disable=W1401 
# ignore \0 errors, we need it for ansi colours

import config

import subprocess

def indent(to_print, colour_esc_code):
    """
    Indent a string with INDENT_STR, and colourise it through the given 
     colour_esc_code.
    """
    print colour_esc_code + config.INDENT_STR + str(to_print) + "\033[0m"

def output(to_print):
    """
    Output a string as Yellow (or as theme has changed it)
    """
    indent(to_print, "\033[93m")

def error(to_print):
    """
    Output a string as Red (or as theme has changed it)
    """
    indent("Error: " + str(to_print), "\033[91m")

def debug(to_print):
    """
    Output a string as Yellow (or as theme has changed it), only if we're not
     in debug mode
    """
    if config.IS_DEBUG_MODE:
        indent("DEBUG: " + str(to_print), "\033[95m")

def enumerate_choices(the_list):
    """
    Iterate through a list, and return the index in the list, iff it is valid.
     Keep asking for input until valid. 
    """
    invalid_input = True
    idxi = -1

    while invalid_input:
        for ndx, val in enumerate(the_list):
            output( str(ndx) + ") " + val)
        opt_idx = raw_input("Please enter an option: ")
        
        idxi = int(opt_idx)

        invalid_input = not idxi >= 0 and idxi < len(the_list)
        if invalid_input:
            error("Please enter a valid option. ")
    return idxi    


def execute(args):
    """
    Execute a given command (denoted by args), informing user of an error
     and if config.IS_DEBUG_MODE, output the error code. 
    """
    ret = subprocess.call(args)
    if not ret == 0:
        error("Some unknown error occured when executing {}".
                format(args[0]))
        debug("Error code {} when calling [{}]".format(ret, " ".join(args)))



def in_list_upper(to_check, the_list, error_str):
    """
    Check if an uppercased value is in a given the_list, and if so, return it. 
     Otherwise, return none, and output an error.
    """
    if to_check.upper() in the_list:
        return to_check.upper()
    else:
        error(error_str)
        return None
