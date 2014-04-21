import config

# Store this here otherwise we get circular references
INDENT_STR = ":: "

def indent(to_print, colour_esc_code):
    """
    Indent a string with INDENT, and colourise it through the given 
     colour_esc_code.
    """
    print colour_esc_code + INDENT_STR + str(to_print) + "\033[0m"

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

    while True:
        for ndx, val in enumerate(the_list):
            output( str(ndx) + ") " + val)
        opt_idx = raw_input("Please enter an option: ")
        
        idxi = int(opt_idx)

        invalid_input = not idxi >= 0 and idxi < len(the_list)
        if invalid_input:
            error("Please enter a valid option. ")
    return idxi    