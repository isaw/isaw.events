from zope.testing import doctest
from unittest import TestSuite

from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

from plone.app.controlpanel.tests.cptc import ControlPanelTestCase

setupPloneSite()

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def test_suite():
    tests = ['calendar.txt',
             'filter.txt',
             'mail.txt',
             'maintenance.txt',
             'security_enable_user_folder.txt',
             'search.txt',
             'site.txt',
             'skins.txt',
             'markup.txt',
             'types.txt',
             ]
    suite = TestSuite()
    for test in tests:
        suite.addTest(FunctionalDocFileSuite(test,
            optionflags=OPTIONFLAGS,
            package="plone.app.controlpanel.tests",
            test_class=ControlPanelTestCase))
    return suite
