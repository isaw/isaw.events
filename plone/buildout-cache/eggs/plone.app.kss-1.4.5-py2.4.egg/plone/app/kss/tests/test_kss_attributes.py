from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from kss.core.BeautifulSoup import BeautifulSoup
from Products.Five.testbrowser import Browser

# XXX should not this be like this?
#from plone.app.kss.tests.kss_and_plone_layer import KSSAndPloneTestCase
#class TestKSSAttributes(KSSAndPloneTestCase, ptc.FunctionalTestCase):
class TestKSSAttributes(ptc.FunctionalTestCase):
    
    BeautifulSoup = BeautifulSoup

    def afterSetUp(self):
        self.folder.invokeFactory('Document', 'page')
        self.page = self.folder.page
        self.page.setTitle('My title')
        self.page.setDescription('My description')
        self.page.setText('<p>My text</p>')
        self.user = ptc.default_user
        self.password = ptc.default_password
        self.browser = Browser()
        props = self.portal.portal_properties.site_properties
        # In Plone 3.3 inline editing is switched off by default; for
        # the tests we turn it on.
        props._updateProperty('enable_inline_editing', True)

class TestForKSSInlineEditing:
      
    def test_notLogged():
        r"""
       
        We publish the page.

            >>> self.portal.portal_workflow.doActionFor(self.page, 'submit')
            >>> self.loginAsPortalOwner()
            >>> self.portal.portal_workflow.doActionFor(self.page, 'publish')
            >>> self.logout()

        We call it.
        
            >>> self.browser.open(self.page.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)
        
        We find the title tag.
        
            >>> title = soup.find(id='parent-fieldname-title')
            >>> title is not None
            True
        
        We see that the KSS hooks shouldn't be there because we're not
        logged in!
        
            >>> 'kssattr-atfieldname-' in title['class']
            False
            >>> 'kssattr-templateId-' in title['class']
            False
            >>> 'kssattr-macro-' in title['class']
            False
            >>> 'inlineEditable' in title['class']
            False
        """

    def test_logged():
        r"""
        
        Okay, we don't go straight away for the page but we actually
        do authenticate
        
            >>> self.browser.addHeader(
            ...    'Authorization', 'Basic %s:%s' % (self.user, self.password))
            >>> self.browser.open(self.page.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)
        
        We find the title
        
            >>> title = soup.find(id='parent-fieldname-title')
            >>> title is not None
            True
        
        We check everything is in now, especially that
        ``kssattr-fieldname-`` matched the right field, and is not
        only there, but actually makes some sense
        Also, we check that the class is ``inlineEditable`` because our KSS
        hooks there (look at at.kss for details)
        
            >>> 'kssattr-atfieldname-title' in title['class']
            True
            >>> 'kssattr-templateId-' in title['class']
            True
            >>> 'kssattr-macro-' in title['class']
            True
            >>> 'inlineEditable' in title['class']
            True

        Rerun, description now! (which is not a Francis Ford Coppola's
        movie)
        
            >>> description = soup.find(
            ...    id='parent-fieldname-description')
            >>> description is not None
            True
            >>> 'kssattr-atfieldname-description' in description['class']
            True
            >>> 'kssattr-templateId-' in description['class']
            True
            >>> 'kssattr-macro-' in description['class']
            True
            >>> 'inlineEditable' in description['class']
            True
        
        Now, time for the text
        
            >>> text = soup.find(id='parent-fieldname-text')
            >>> text is not None
            True
            >>> 'kssattr-atfieldname-text' in text['class']
            True
            >>> 'kssattr-templateId-' in text['class']
            True
            >>> 'kssattr-macro-' in text['class']
            True
            >>> 'inlineEditable' in text['class']
            True
        """

class TestContentsTabs:
    def test_tab_ids():
        r"""
        Okay, we don't go straight away for the page but we actually
        do authenticate
        
            >>> self.browser.addHeader(
            ...    'Authorization', 'Basic %s:%s' % (self.user, self.password))
            >>> self.browser.open(self.page.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)
        
        The content tabs must have li tags with special ids:

            >>> soup.find('li', dict(id='contentview-view')) is not None
            True
            >>> soup.find('li', dict(id='contentview-edit')) is not None
            True
            >>> soup.find('li', dict(id='contentview-local_roles')) is not None
            True
        """

    def test_ul_id():
        r"""
        We actually authenticate and we'll doing some tests about ul id (which it should be present)
        
            >>> self.browser.addHeader(
            ...    'Authorization', 'Basic %s:%s' % (self.user, self.password))
            >>> self.browser.open(self.page.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)
        
        The content tabs must have li tags with special ids:
        Checking for the correct ul tag class

            >>> content_ul_tag = soup.find('ul', {'class':'contentViews'})
            >>> content_ul_tag is not None
            True 
          
        a tags inside of the li tags shouldn't have ids; li tags should have id attributes.
        There may be three or four tags (contentview-history was removed in Plone 3.3).

            >>> [a.get('id') for a in content_ul_tag.findAll('a') if a.get('id')]
            []
            >>> [li.get('id') for li in content_ul_tag.findAll('li')][:3]
            [u'contentview-view', u'contentview-edit', u'contentview-local_roles']

        """
    
class TestContentMenu:
    def test_menu_presence():
        r"""
        We must authenticate because content menu is only present for logged in users
        
            >>> self.browser.addHeader(
            ...  'Authorization', 'Basic %s:%s' % (self.user, self.password))
            >>> self.browser.open(self.page.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)
          
        We are in a page so we must have the "change workflow" menu.
        
            >>> contentmenu_dl_tag = soup.find('dl', {'id':'plone-contentmenu-workflow'})
            >>> contentmenu_dl_tag is not None
            True

            >>> contentmenu_dl_tag.find('dd',{'class':'actionMenuContent'}) is not None
            True  
          
        Then you must have the copy and cut links
        
            >>> soup.find('a', {'class':'actionicon-object_buttons-cut'}) is not None
            True
            
            >>> soup.find('a', {'class':'actionicon-object_buttons-copy'}) is not None
            True
        
        Now we go to the folder, so we must have the "change view" menu.
            
            >>> self.browser.open(self.folder.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)    
            >>> contentmenu_dl_tag = soup.find('dl', {'id':'plone-contentmenu-display'})
            >>> contentmenu_dl_tag is not None
            True

            >>> contentmenu_dl_tag.find('dd',{'class':'actionMenuContent'}) is not None
            True
          
        A couple of things again, basically the stuff we hook on with kss, which are, the 
        external div and the inner ul (one is used for content replacement through innerHTML,
        the other used to hook events on load)
            
            >>> self.browser.open(self.folder.absolute_url())
            >>> soup = self.BeautifulSoup(self.browser.contents)
            
        Ok let's see if we have the hook to replace the content
            
            >>> content_td = soup.find('td', {'id': 'portal-column-content'})
            >>> content_td is not None
            True
            >>> content_actions = content_td.find('div', {'class': 'contentActions'})
            >>> content_actions is not None
            True
            
        This is great, now let's check if we have the bind load stuff in place too
            
            >>> content_actions_ul = content_actions.find('ul', {'id': 'contentActionMenus'})
            >>> content_actions_ul is not None
            True

        """

def test_suite():
    suite = ztc.FunctionalDocTestSuite(test_class=TestKSSAttributes)
    suite.layer = PloneSite
    return suite
