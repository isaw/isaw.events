import sys

def __parent__(modulename, level=1):
    'Figure out parent module'
    for i in range(level):
        if not isinstance(modulename, basestring):
            modulename = modulename.__name__
        modulename = sys.modules['.'.join(modulename.split('.')[:-1])]
    return modulename
