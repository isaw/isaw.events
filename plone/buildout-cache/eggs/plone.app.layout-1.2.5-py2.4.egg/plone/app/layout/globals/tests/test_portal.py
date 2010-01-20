import unittest
from plone.app.layout.globals.tests.base import GlobalsTestCase

from plone.app.layout.navigation.root import getNavigationRoot
from zope.i18n.locales import locales

class TestPortalStateView(GlobalsTestCase):
    """Ensure that the basic redirector setup is successful.
    """
    
    def afterSetUp(self):
        self.view = self.folder.restrictedTraverse('@@plone_portal_state')
    
    def test_portal(self):
        self.assertEquals(self.view.portal(), self.portal)
        
    def test_portal_title(self):
        self.portal.title = 'My title'
        self.assertEquals(self.view.portal_title(), 'My title')
        
    def test_portal_url(self):
        self.assertEquals(self.view.portal_url(), self.portal.absolute_url())
                       
    def test_navigation_root_path(self):
        self.assertEquals(self.view.navigation_root_path(), getNavigationRoot(self.folder))
        
    def test_navigation_root_url(self):
        url = self.app.REQUEST.physicalPathToURL(getNavigationRoot(self.folder))
        self.assertEquals(self.view.navigation_root_url(), url)

    def test_default_language(self):
        self.portal.portal_properties.site_properties.default_language = 'no'
        self.assertEquals(self.view.default_language(), 'no')

    def test_language(self):
        self.app.REQUEST.set('language', 'no')
        self.assertEquals(self.view.language(), 'no')

    def test_locale(self):
        self.app.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'no')
        no = locales.getLocale('no', None, None)
        self.assertEquals(self.view.locale(), no)
        
    def test_is_rtl(self):
        self.app.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'no')
        self.assertEquals(self.view.is_rtl(), False)
        del self.app.REQUEST.__annotations__
        self.app.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'he')
        self.assertEquals(self.view.is_rtl(), True)
        
    def test_member(self):
        self.assertEquals(self.view.member(), self.portal.portal_membership.getAuthenticatedMember())
        
    def test_anonymous(self):
        self.assertEquals(self.view.anonymous(), False)
        self.logout()
        del self.app.REQUEST.__annotations__
        self.assertEquals(self.view.anonymous(), True)
        
    def test_friendly_types(self):
        self.portal.portal_properties.site_properties.types_not_searched = ('Document',)
        self.failIf('Document' in self.view.friendly_types())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPortalStateView))
    return suite
