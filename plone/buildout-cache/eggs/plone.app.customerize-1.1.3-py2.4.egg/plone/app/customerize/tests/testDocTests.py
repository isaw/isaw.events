# setup tests with all doctests found in docs/

from plone.app.customerize import docs
from plone.app.customerize.tests import layer
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase import PloneTestCase
from Products.Five.testbrowser import Browser
from unittest import TestSuite
from os.path import join, split, abspath, dirname
from os import walk
from re import compile
from sys import argv


PloneTestCase.setupPloneSite()

from zope.testing import doctest
OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class CustomerizeFunctionalTestCase(PloneTestCase.FunctionalTestCase):

    layer = layer.PloneCustomerize
    
    def afterSetUp(self):
        """ set up the tests """
        pass

    def getBrowser(self, loggedIn=False):
        """ instantiate and return a testbrowser for convenience """
        browser = Browser()
        if loggedIn:
            user = PloneTestCase.default_user
            pwd = PloneTestCase.default_password
            browser.addHeader('Authorization', 'Basic %s:%s' % (user, pwd))
        return browser

# we check argv to enable testing of explicitely named doctests
if '-t' in argv:
    pattern = compile('.*\.(txt|rst)$')
else:
    pattern = compile('^test.*\.(txt|rst)$')

def test_suite():
    suite = TestSuite()
    docs_dir = abspath(dirname(docs.__file__)) + '/'
    for path, dirs, files in walk(docs_dir):
        for name in files:
            relative = join(path, name)[len(docs_dir):]
            if not '.svn' in split(path) and pattern.search(name):
                suite.addTest(FunctionalDocFileSuite(relative,
                    optionflags=OPTIONFLAGS,
                    package=docs.__name__,
                    test_class=CustomerizeFunctionalTestCase))
    return suite
