import unittest

import plone.portlets

from zope.testing import doctest
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def configurationSetUp(test):
    setUp()

    import zope.contentprovider
    import zope.security
    import zope.app.component
    import zope.app.container
    import zope.app.pagetemplate
    import zope.app.security

    XMLConfig('meta.zcml', zope.security)()
    XMLConfig('meta.zcml', zope.app.component)()
    XMLConfig('meta.zcml', zope.app.pagetemplate)()
    XMLConfig('meta.zcml', zope.app.security)()

    # BBB conditional code for loading the utility dispatchers
    # In Zope 2.11 they are in zope.component
    try:
        import zope.component
        XMLConfig('configure.zcml', zope.component)()
    except IOError:
        pass
    # In Zope 2.10 they are in zope.app.event
    try:
        import zope.app.event
        XMLConfig('configure.zcml', zope.app.event)()
    except (ImportError, IOError):
        pass

    XMLConfig('configure.zcml', zope.app.security)()
    XMLConfig('configure.zcml', zope.app.container)()
    XMLConfig('configure.zcml', zope.contentprovider)()
    
    XMLConfig('configure.zcml', plone.portlets)()


def configurationTearDown(test):
    tearDown()

def test_safe_render():
    r"""
    Render the portlet safely, so that when an exception
    occurs, we log and don't bail out.

      >>> from plone.portlets.manager import PortletManagerRenderer
      >>> class PortletRenderer:
      ...     def __init__(self, error=False):
      ...         self.error = error
      ...     def render(self):
      ...         if self.error:
      ...             raise Exception()
      ...         return 'portlet rendered'

    When no error occurs, ``safe_render`` will return the portlet
    renderer's ``render()``:
    
      >>> renderer = PortletManagerRenderer(*(None,) * 4)
      >>> renderer.safe_render(PortletRenderer())
      'portlet rendered'

    When an error is raised, the ``error_message`` template is
    rendered:
    
      >>> renderer.error_message = lambda: 'error rendered'
      >>> renderer.safe_render(PortletRenderer(error=True))
      'error rendered'
    """

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags),
        doctest.DocFileSuite(
            'uisupport.txt',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags),
        doctest.DocFileSuite(
            'utils.txt',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags),
        doctest.DocTestSuite()))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
