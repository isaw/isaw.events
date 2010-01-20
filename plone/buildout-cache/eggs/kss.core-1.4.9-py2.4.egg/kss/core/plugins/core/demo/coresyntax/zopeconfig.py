
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

class KSSCoreSyntaxDemos(object):
    implements(IResource)

    demos = (
        KSSDemo('', 'Core syntax', "kss_selector_param.html", "Kss selector parameters"),
        KSSDemo('', 'Core syntax', "kss_url_param.html", "Kss url parameters"),
        KSSDemo('', 'Core syntax', "kss_selector_param_multiprop.html", "Kss selector parameters, with multiproperties"),
        KSSDemo('', 'Core syntax', "kss_url_param_multiprop.html", "Kss url parameters, with multiproperties"),
        KSSDemo('', 'Core syntax', "kss_client_action_alias.html", "Client action aliases"),
        )

    # directories are relative from the location of this .py file
    selenium_tests = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
