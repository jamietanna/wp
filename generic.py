import config

INDENT = ":: "

def indent(toPrint, colour):
    print colour + INDENT + str(toPrint) + "\033[0m"

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

