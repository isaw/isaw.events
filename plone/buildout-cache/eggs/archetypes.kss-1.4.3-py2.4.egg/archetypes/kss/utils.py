
import inspect

# --
# Getting information about the caller template
# --

class FrameError(Exception):
    pass
    
def get_econtext():
    '''Inspects full context of the caller page

    We access the caller stack and thus the *entire*
    context of the page template, including globals (defines).
    (This could not be passed from the template, normally, due to
    its restricted nature.)

    Some explanation:

    We walk up the the python expression stack until we find the
    Pagetemplates.ZRPythonExpr.__call__ that has econtext
    in the locals. The econtext is a 
    <Products.PageTemplates.Expressions.ZopeContext object that has: 

        vars:           global and local variables combined, readonly.

        setLocal:       set local context variable

        setGlobal:      set global context variable
    
    '''
    frame = inspect.currentframe().f_back
    econtext = None
    try:
        while frame is not None:
            try:
                econtext = frame.f_locals['econtext']
            except KeyError:
                # go one frame up
                frame = frame.f_back
            else:
                # found
                return econtext
        else: 
            # Econtext frame not found
            return None
    finally:
        del frame
        del econtext
