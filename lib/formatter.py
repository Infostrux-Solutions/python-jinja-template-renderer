"""
    Simple Formatting class.
"""
header      = '\033[95m'
bold        = '\033[1m'
underline   = '\033[4m'

warning     = '\033[1;33m'
fail        = '\033[1;31m'
info_white  = '\033[1;37m'
info_cyan   = '\033[1;36m'
info_blue   = '\033[1;34m'
good_green  = '\033[1;31m'
clear       = '\033[0m'

def warning(message):
    message = f'{fail}[WARNING] {message}{clear}'
    return message

def error(message):
    message = f'{fail}[ERROR] {message}{clear}'
    return message

def info(message, colour = 'white'):

    if colour == 'white':
        format_start = info_white
    elif colour == 'blue':
        colour = info_blue
    elif colour == 'cyan':
        colour = info_cyan
    else:
        colour = bold

    message = f'{format_start}[INFO] {message}{clear}'
    
    return message    