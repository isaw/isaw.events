import os, sys, unittest

from zope.testing import doctest

from zope.app.testing.placelesssetup import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

import zope.app.component
import plone.memoize

def configurationSetUp(test):
    setUp()    
    
    XMLConfig('meta.zcml', zope.app.component)()
    XMLConfig('configure.zcml', plone.memoize)()

def configurationTearDown(test):
    tearDown()

def test_suite():
    try:
        from zope.publisher.interfaces.browser import IBrowserView, IBrowserRequest
    except ImportError:
        from zope.app.publisher.interfaces.browser import IBrowserView
        from zope.publisher.interfaces.browser import IBrowserRequest
    from zope.component import adapts
    from zope.component import provideAdapter
    from zope.interface import implements, Interface

    tests = (
        doctest.DocTestSuite('plone.memoize.compress',
                             setUp=configurationSetUp,
                             tearDown=configurationTearDown),
        doctest.DocFileSuite('instance.txt', 
                             package="plone.memoize",
                             setUp=configurationSetUp,
                             tearDown=configurationTearDown,
                             optionflags=optionflags,
                             globs=locals()),
        doctest.DocFileSuite('view.txt', 
                             package="plone.memoize",
                             setUp=configurationSetUp,
                             tearDown=configurationTearDown,
                             optionflags=optionflags,
                             globs=locals()),
        doctest.DocFileSuite('forever.txt', 
                             package="plone.memoize",
                             setUp=configurationSetUp,
                             tearDown=configurationTearDown,
                             optionflags=optionflags,
                             globs=locals()),
        doctest.DocFileSuite('README.txt'),
        doctest.DocTestSuite('plone.memoize.request',
                             setUp=configurationSetUp,
                             tearDown=configurationTearDown),
        doctest.DocTestSuite('plone.memoize.volatile'),
        doctest.DocTestSuite('plone.memoize.ram',
                             setUp=configurationSetUp,
                             tearDown=configurationTearDown),
        )

    return unittest.TestSuite(tests)


if __name__=="__main__":
    import unittest
    unittest.TextTestRunner().run(test_suite())
