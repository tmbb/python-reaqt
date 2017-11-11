def format_float(f, precision=2):
    """Format a floating point number with the specified precision"""
    format_string = "{0:." + str(precision) + "f}" 
    return format_string.format(round(f, 2))

def printer(name):
    """A debug helper."""
    def helper(obj):
        print(name + ":", obj)
    return helper


def identity(*args):
    """A convenient identity function."""
    if len(args) == 1:
        return args[0]
    else:
        return args

def scale(s):
    def helper(x):
        return x*s
    return helper
