
import sys
import unittest
from zope.testing.doctestunit import DocTestSuite
from __parent__ import __parent__
configfeature = __parent__(__name__, 2)

def test_fiveconfig():
    """
    The fiveconfig.zcml file declares various Five compatibility features.
    We only test that the configuration file can be run.

    >>> import zope.configuration.tests
    >>> import zope.configuration.xmlconfig
    >>> context = zope.configuration.xmlconfig.file('metacore.zcml', configfeature)
    >>> context = zope.configuration.xmlconfig.file('fiveconfig.zcml', configfeature, context)
    
    >>> context.hasFeature('compat_five') or context.hasFeature('compat_not_five')
    True

    """


def test_suite():
    return unittest.TestSuite((
        DocTestSuite(),
        ))
