from unittest import TestSuite, main
from Testing.ZopeTestCase import ZopeDocFileSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite

from zope.component import testing, provideAdapter
from zope.traversing.adapters import DefaultTraversable
from zope.publisher.browser import BrowserLanguages
from zope.publisher.http import HTTPCharsets

__docformat__ = "reStructuredText"

def setUp(test):
    testing.setUp(test)
    provideAdapter(DefaultTraversable, (None,))
    provideAdapter(BrowserLanguages)
    provideAdapter(HTTPCharsets)

def test_suite():
    return TestSuite([
        #DocTestSuite('five.customerize.browser'),
        ZopeDocFileSuite('zpt.txt', package="five.customerize",
                         setUp=setUp, tearDown=testing.tearDown),
        ZopeDocFileSuite('customerize.txt', package="five.customerize"),
        FunctionalDocFileSuite('browser.txt', package="five.customerize")
        ])

if __name__ == '__main__':
    main(defaultTest='test_suite')
