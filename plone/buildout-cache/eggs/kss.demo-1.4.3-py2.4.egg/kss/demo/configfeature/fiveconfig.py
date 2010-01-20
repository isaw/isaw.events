'''\
Compatibility configuration switches

This is a transitional solution to attack the problem
of quickly changing Zope3 and Five APIs.

Import checks are done centrally from here.
The point is that compatibility imports should fail here,
if anything goes wrong. Components should only check
the switches set from here.

Corresponding configuration features are also set up
from the compat.zcml file. The idea is that all switches
are accessible both from python and zcml.


Supported versions:
-------------------

Zope  2.9, 2.10
Zope  3.2, 3.3

Compatibility matrix
--------------------

The following table shows which Five version can and should be used 
with which Zope 2 and Zope 3 versions.

.           Zope 2.8         Zope 2.9     Zope 2.10
.           Zope X3 3.0      Zope 3.2     Zope 3.3  
Five 1.0    included                               
Five 1.2    X                                      
Five 1.3                     included              
Five 1.4                     X                      
Five trunk                                included 

'''

__all__ = ('__compat__', )

class DictLike(object):
    pass
    
__compat__ = DictLike()

try:
    import zope.component.interface
    # XXX this now fails on Zope 3.4, so
    # commented out even if it gives bad result now
    ##import zope.component.location
    __compat__.zope_pre_3_3 = False
except ImportError:
    # The only supported pre_3_3 version is 3.2
    import zope.app.component.interface
    ##import zope.app.location
    __compat__.zope_pre_3_3 = True
    
try:
    import Products.Five
except ImportError:
    __compat__.five = False
else:
    __compat__.five = True
    try:
        # Zope 2.8 / Five 1.0.2
        from Products.Five.resource import Resource
        __compat__.five_pre_1_3 = True
    except ImportError:
        # Zope 2.9 / Five 1.3
        from Products.Five.browser.resource import Resource
        __compat__.five_pre_1_3 = False

# Unsupported versions.
if __compat__.five and __compat__.five_pre_1_3:
    raise Exception, 'Zope 2.8 or prior versions (Five 1.2 or prior versions) are unsupported, please upgrade!'
