import unittest

import zope.annotation
import zope.security
import zope.app.security
import zope.app.component
import zope.app.container

import plone.contentrules

from zope.testing import doctest
from zope.app.testing.placelesssetup import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def configurationSetUp(test):
    setUp()
    
    XMLConfig('meta.zcml', zope.security)()
    XMLConfig('meta.zcml', zope.app.security)()
    XMLConfig('meta.zcml', zope.app.component)()
    
    XMLConfig('configure.zcml', zope.app.security)()
    XMLConfig('configure.zcml', zope.app.container)()
    XMLConfig('configure.zcml', zope.annotation)()
    
    XMLConfig('configure.zcml', plone.contentrules)()
    # XMLConfig('meta.zcml', plone.contentrules)()

def configurationTearDown(test):
    tearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt', 
            setUp=configurationSetUp, 
            tearDown=configurationTearDown,
            optionflags=optionflags),
        doctest.DocFileSuite(
            'zcml.txt', 
            setUp=configurationSetUp, 
            tearDown=configurationTearDown,
            optionflags=optionflags),
        ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')