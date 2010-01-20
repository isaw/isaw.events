from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from plone.portlet.static import static

from plone.portlet.static.tests.base import TestCase

class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='plone.portlet.static.Static')
        self.assertEquals(portlet.addview, 'plone.portlet.static.Static')

    def testInterfaces(self):
        portlet = static.Assignment(header=u"title", text="text")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='plone.portlet.static.Static')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={'header' : u"test title", 'text' : u"test text"})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], static.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = static.Assignment(header=u"title", text="text")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, static.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = static.Assignment(header=u"title", text="text")

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, static.Renderer))

        self.failUnless(renderer.available,
                        "Renderer should be available by default.")
        assignment = static.Assignment(header=u"title", text="text", hide=True)
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failIf(renderer.available, "Renderer should not be available.")


class TestRenderer(TestCase):
    
    def afterSetUp(self):
        self.setRoles(('Manager',))

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = assignment or static.Assignment(header=u"title", text="text")

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal, assignment=static.Assignment(header=u"title", text="<b>text</b>"))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.failUnless('title' in output)
        self.failUnless('<b>text</b>' in output)

    def test_available(self):
        r = self.renderer(
            context=self.portal,
            assignment=static.Assignment(header=u"title", text="<b>text</b>",
                                         hide=True))
        r = r.__of__(self.folder)
        r.update()
        self.failIf(r.available, "Renderer should not be available.")
        
    def test_css_class(self):
        r = self.renderer(context=self.portal, 
                          assignment=static.Assignment(header=u"Welcome text", text="<b>text</b>"))
        self.assertEquals('portlet-static-welcome-text', r.css_class())
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
