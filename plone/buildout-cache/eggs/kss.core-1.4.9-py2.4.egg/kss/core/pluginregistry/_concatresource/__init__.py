'''\
Product init
'''
# alias myself to python import root, directly
try:
    import sys
    if not 'concatresource' in sys.modules:
    # only 1st import is aliased.
        sys.modules['concatresource'] = sys.modules[globals()['__name__']]
except ImportError:
    pass
