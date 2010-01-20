# Copyright (c) 2006
# Authors:
#   Jean-Paul Ladage <j.ladage@zestsoftware.nl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

import unittest
from Products.PloneTestCase import PloneTestCase
from plone.app.kss.tests.kss_and_plone_layer import KSSAndPloneTestCase
from zope import component
from zope.component import adapter
from kss.core.interfaces import IKSSView
from archetypes.kss.interfaces import IVersionedFieldModifiedEvent
from kss.core.BeautifulSoup import BeautifulSoup

PloneTestCase.setupPloneSite()

@adapter(None, IKSSView, IVersionedFieldModifiedEvent)
def field_modified_handler(ob, view, event):
    ob._eventCaught = True

class FieldsViewTestCase(KSSAndPloneTestCase):

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)
        # commands will be rendered as data structures,
        self.setDebugRequest()
        self.loginAsPortalOwner()
        context = self.portal['front-page']
        # Set up a view 
        self.view = context.restrictedTraverse('saveField')

    # --
    # test the KSS methods
    # --

    def testReplaceField(self):
        self.view.context.changeSkin('Plone Default', self.view.request)
        result = self.view.replaceField('title', 'kss_generic_macros', 'title-field-view')
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
            ('setStyle', '.portalMessage', 'css'),
            ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
            ('setAttribute', 'kssPortalMessage', 'htmlid'),
            ('setStyle', 'kssPortalMessage', 'htmlid'),
            ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ('focus', '#parent-fieldname-title .firstToFocus', '')
        ])

    def testReplaceWithView(self):
        self.view.context.changeSkin('Plone Default', self.view.request)
        result = self.view.replaceWithView('title', 'kss_generic_macros', 'title-field-view')
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
             ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ])

    # XXX this test should test without events, so it should stop events listening
    # but we have no more method for that
    def testSaveField(self):
        view = self.view
        result = view.saveField('title', {'title':'My Title'}, 
                                'kss_generic_macros', 'title-field-view')
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
             ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ])
        self.assertEqual('My Title', self.portal['front-page'].Title())
        res = view.saveField('description',
                             {'description':'Woot a funky description!'},
                             'kss_generic_macros', 'description-field-view')
        self.assertEqual('Woot a funky description!', self.portal['front-page'].Description())
    

    # XXX note how these tests are wwrong, obviously events are not listened in this setup
    def testSaveFieldWithEvents(self):
        view = self.view
        result = view.saveField('title', {'title':'My Title'}, 
                                'kss_generic_macros', 'title-field-view')
        self.assertEqual('My Title', self.portal['front-page'].Title())
        res = view.saveField('description',
                             {'description':'Woot a funky description!'},
                             'kss_generic_macros', 'description-field-view')
        self.assertEqual('Woot a funky description!', self.portal['front-page'].Description())


    def testSaveFieldWithValueFromRequest(self):
        view = self.view
        view.request.form['title'] = 'My Title'
        view.request.form['description'] = 'Woot a funky description!'
        result = view.saveField('title', None, 
                                'kss_generic_macros', 'title-field-view')
        self.assertEqual('My Title', self.portal['front-page'].Title())
        res = view.saveField('description',
                             None,
                             'kss_generic_macros', 'description-field-view')
        self.assertEqual('Woot a funky description!', 
                         self.portal['front-page'].Description())

    # XXX this test would only run, if events are really listened 
    # (which they are not) 
    def _XXX_testSaveFieldWithVersioning(self):
        view = self.view
        component.provideHandler(field_modified_handler)
        try:
            res = view.saveField('title', {'title':'My Title'}, 
                                    'kss_generic_macros', 'title-field-view')
            self.assert_(getattr(view.context, '_eventCaught', False))
            view.context._eventCaught = False
            res = view.saveField('description',
                                 {'description':'Woot a funky description!'},
                                 'kss_generic_macros', 'description-field-view')
            self.assert_(getattr(view.context, '_eventCaught', False))
        finally:
            sm = component.getSiteManager()
            sm.unregisterHandler(field_modified_handler)

    # XXX these tests with a provided target node id are a bit silly because the feature
    # is not currently in use in any templates -- we provide a target node id of
    # 'parent-fieldname-title' which is the default anyway -- but the tests make sure
    # this api extension work to some degree.
    
    def testReplaceFieldWithProvidedTargetNodeId(self):
        self.view.context.changeSkin('Plone Default', self.view.request)
        target = 'parent-fieldname-title'
        result = self.view.replaceField('title', 'kss_generic_macros', 'title-field-view', target=target)
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
            ('setStyle', '.portalMessage', 'css'),
            ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
            ('setAttribute', 'kssPortalMessage', 'htmlid'),
            ('setStyle', 'kssPortalMessage', 'htmlid'),
            ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ('focus', '#parent-fieldname-title .firstToFocus', '')
        ])

    def testReplaceWithViewWithProvidedTargetNodeId(self):
        self.view.context.changeSkin('Plone Default', self.view.request)
        target = 'parent-fieldname-title'
        result = self.view.replaceWithView('title', 'kss_generic_macros', 'title-field-view', target=target)
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
             ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ])

    def testSaveFieldWithProvidedTargetNodeId(self):
        view = self.view
        target = 'parent-fieldname-title'
        result = view.saveField('title', {'title':'My Title'}, 
                                'kss_generic_macros', 'title-field-view', target=target)
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
             ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ])
        self.assertEqual('My Title', self.portal['front-page'].Title())

    def testReplaceFieldWithProvidedContext(self):
        # set the global context to /news
        context = self.portal['news']
        view = context.restrictedTraverse('saveField')
        context.changeSkin('Plone Default', view.request)

        frontpage_uid = self.portal['front-page'].UID()
        result = view.replaceField('title', 'kss_generic_macros', 'title-field-view', uid=frontpage_uid)

        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
            ('setStyle', '.portalMessage', 'css'),
            ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
            ('setAttribute', 'kssPortalMessage', 'htmlid'),
            ('setStyle', 'kssPortalMessage', 'htmlid'),
            ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ('focus', '#parent-fieldname-title .firstToFocus', '')
        ])

        # make sure we've got the right context:
        replaceHTML = ''.join([r['params'].get('html', '') for r in result])
        self.assertEqual(u"Welcome to Plone" in replaceHTML, True)       

    def testReplaceWithViewWithProvidedContext(self):
        # set the global context to /news
        context = self.portal['news']
        view = context.restrictedTraverse('saveField')
        context.changeSkin('Plone Default', view.request)

        frontpage_uid = self.portal['front-page'].UID()
        result = view.replaceWithView('title', 'kss_generic_macros', 'title-field-view', uid=frontpage_uid)

        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
             ('replaceHTML', 'parent-fieldname-title', 'htmlid'),
            ])

        # make sure we've got the right context:
        replaceHTML = ''.join([r['params'].get('html', '') for r in result])
        self.assertEqual(u"Welcome to Plone" in replaceHTML, True)       

    def testSaveFieldWithProvidedContext(self):
        # set the global context to /news
        context = self.portal['news']
        view = context.restrictedTraverse('saveField')
        context.changeSkin('Plone Default', view.request)

        frontpage_uid = self.portal['front-page'].UID()
        result = view.saveField('title', {'title': 'My Title'},
                                'kss_generic_macros', 'title-field-view', uid=frontpage_uid)

        self.assertEqual('My Title', self.portal['front-page'].Title())

    
    def testMarkerInATField(self):
        # writeable
        view = self.portal['front-page'].restrictedTraverse('kss_field_decorator_view')
        result = view.getKssClasses('title')
        self.assertEqual(result, ' kssattr-atfieldname-title')
        result = view.getKssClasses('title', 'template')
        self.assertEqual(result, ' kssattr-atfieldname-title kssattr-templateId-template')
        result = view.getKssClasses('title', 'template', 'macro')
        self.assertEqual(result, ' kssattr-atfieldname-title kssattr-templateId-template kssattr-macro-macro')
        self.logout()
        result = view.getKssClasses('title')
        # not writeable
        self.assertEqual(result, '')

    def testMarkerInATFieldInlineEditable(self):
        # writeable
        view = self.portal['front-page'].restrictedTraverse('kss_field_decorator_view')
        result = view.getKssClassesInlineEditable('title', 'template')
        self.assertEqual(result, ' kssattr-atfieldname-title kssattr-templateId-template inlineEditable')
        result = view.getKssClassesInlineEditable('title', 'template', 'macro')
        self.assertEqual(result, ' kssattr-atfieldname-title kssattr-templateId-template kssattr-macro-macro inlineEditable')
        self.logout()
        # not writeable
        result = view.getKssClassesInlineEditable('title', 'template')
        self.assertEqual(result, '')

    def testMarkerInNonATField(self):
        # portal root is not an AT object
        view = self.portal.restrictedTraverse('kss_field_decorator_view')
        result = view.getKssClasses('title')
        # not writeable
        self.assertEqual(result, '')

    def testVersionPreviewIsNotInlineEditable(self):
        """If the kss_inline_editable variable is defined to False
        in a page template, all the fields will be globally prohibited 
        to be editable. This works via the getKssClasses method.
        Similarly, is suppress_preview is set to true, inline
        editing is prohibited. This is set from CMFEditions, in the
        versions_history_form.

        In this test we check that the versions history is not
        inline editable at all.
        """
        obj = self.portal['front-page']
        # Make sure we actually have a revision
        pr = self.portal.portal_repository
        pr.save(obj)
        # Render versions history of the front page
        obj.REQUEST.form['version_id'] = '0'
        rendered = obj.versions_history_form()
        soup = BeautifulSoup(rendered)
        # check that inline edit is not active, by looking at title
        tag = soup.find(id='parent-fieldname-title')
        klass = tag['class']
        # just to check that we are looking at the right bit...
        # XXX but this is no more, we can't check it
        #self.assert_('documentFirstHeading' in klass)
        # ... and now see we are really not inline editable:
        self.assert_('inlineEditable' not in klass)
        # make sure the rest is still there or instant validation and possibly
        # other stuff will fail
        self.assert_('kssattr-templateId-' in klass)
        self.assert_('kssattr-macro-' in klass)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FieldsViewTestCase),
        ))
