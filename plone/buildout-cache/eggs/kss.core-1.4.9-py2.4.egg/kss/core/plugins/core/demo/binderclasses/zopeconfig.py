
from kss.demo.interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    )
from kss.demo.resource import (
    KSSDemo,
    KSSSeleniumTestDirectory,
    )
from zope.interface import implements
     
# Create a mesh of provided interfaces
# This is needed, because an utility must have a single interface.
class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    pass

# XXX you do not need to change anything above here
# -------------------------------------------------

class KSSDemos(object):
    implements(IResource)

    demos = (
        # List your demos here. 
        # (Second parameter can be a subcategory within the demo if needed.)
        KSSDemo('', 'Core syntax', 'kss_binder_classes.html', 'Binder class usage'),

        )

    # directories are relative from the location of this .py file
    selenium_tests = (
        # if you only have one test directory, you
        # need not change anything here.
        KSSSeleniumTestDirectory('selenium_tests'),
        )
