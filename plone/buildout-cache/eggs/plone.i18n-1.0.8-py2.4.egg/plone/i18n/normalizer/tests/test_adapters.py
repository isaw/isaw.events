# -*- coding: utf-8 -*-
"""
    Adapters tests.
"""

import unittest

from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig
from zope.publisher.browser import BrowserLanguages
from zope.publisher.browser import TestRequest

from zope.testing import doctest
from zope.testing.doctestunit import DocTestSuite

from plone.i18n.normalizer.adapters import UserPreferredFileNameNormalizer
from plone.i18n.normalizer.adapters import UserPreferredURLNormalizer


def configurationSetUp(self):
    import plone.i18n.normalizer
    import zope.component
    setUp()
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('configure.zcml', plone.i18n.normalizer)()
    zope.component.provideAdapter(BrowserLanguages)


def testUserPreferredFileNameNormalizer():
    """
    Create a German and English request and filename normalizer:

      >>> de_request = TestRequest(environ=dict(HTTP_ACCEPT_LANGUAGE = 'de'))
      >>> de_filename = UserPreferredFileNameNormalizer(de_request)

      >>> en_request = TestRequest(environ=dict(HTTP_ACCEPT_LANGUAGE = 'en'))
      >>> en_filename = UserPreferredFileNameNormalizer(en_request)

    Test the German normalization:

      >>> de_filename.normalize(u'simpleandsafe')
      'simpleandsafe'

      >>> de_filename.normalize(unicode('text with umläut', 'utf-8'))
      'text with umlaeut'

    Test the English normalization:

      >>> en_filename.normalize(u'simpleandsafe')
      'simpleandsafe'

      >>> en_filename.normalize(unicode('text with umläut', 'utf-8'))
      'text with umlaeut'
    """


def testUserPreferredURLNormalizer():
    """
    Create a German and English request and url normalizer:

      >>> de_request = TestRequest(environ=dict(HTTP_ACCEPT_LANGUAGE = 'de'))
      >>> de_url = UserPreferredURLNormalizer(de_request)

      >>> en_request = TestRequest(environ=dict(HTTP_ACCEPT_LANGUAGE = 'en'))
      >>> en_url = UserPreferredURLNormalizer(en_request)

    Test the German normalization:

      >>> de_url.normalize(u'simpleandsafe')
      'simpleandsafe'

      >>> de_url.normalize(unicode('text with umläut', 'utf-8'))
      'text-with-umlaeut'

    Test the English normalization:

      >>> en_url.normalize(u'simpleandsafe')
      'simpleandsafe'

      >>> en_url.normalize(unicode('text with umläut', 'utf-8'))
      'text-with-umlaeut'
    """


def test_suite():
    return unittest.TestSuite((
        DocTestSuite(setUp=configurationSetUp,
                     tearDown=tearDown,
                     optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest="test_suite")
