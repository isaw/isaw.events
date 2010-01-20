
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

class ValueProviderDemos(object):
    implements(IResource)

    demos = (
        KSSDemo('', 'Value providers', 'pf_forms.html', 'Forms'),
        KSSDemo('', 'Value providers', 'kss_form_submit_multiprop.html', 'Form submit, with multiproperties'),
        )

    # directories are relative from the location of this .py file
    selenium_tests = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
