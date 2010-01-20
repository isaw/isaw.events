"""
Mail related doctests
"""

import unittest
from zope.testing import doctest

from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.CMFPlone.tests import PloneTestCase

from Acquisition import aq_base
from zope.component import getSiteManager
from Products.MailHost.interfaces import IMailHost
from Products.CMFPlone.tests.utils import MockMailHost

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


class MockMailHostTestCase(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(self.portal._original_MailHost),
                           provided=IMailHost)


def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite('mails.txt',
                               optionflags=OPTIONFLAGS,
                               package='Products.CMFPlone.tests',
                               test_class=MockMailHostTestCase),
        ))
