import doctest
import unittest

from DateTime.DateTime import DateTime
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

setupPloneSite()

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def addMember(self, username, fullname="", email="", roles=('Member',), last_login_time=None):
    self.portal.portal_membership.addMember(username, 'secret', roles, [])
    member = self.portal.portal_membership.getMemberById(username)
    member.setMemberProperties({'fullname': fullname, 'email': email,
                                'last_login_time': DateTime(last_login_time),})
                                
def setUp(self):
    addMember(self, 'member1', 'Member one')
    addMember(self, 'member2', 'Member two')

def test_suite():
    from unittest import TestSuite, makeSuite
    return unittest.TestSuite((Suite('README.txt',
                                     optionflags=OPTIONFLAGS,
                                     package='plone.locking',
                                     setUp=setUp,
                                     test_class=FunctionalTestCase),))
