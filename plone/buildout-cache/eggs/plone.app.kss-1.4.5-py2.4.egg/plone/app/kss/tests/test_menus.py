# Copyright (c) 2006
# Authors:
#   David '/dev/null' Convent  <davconvent@gmail.com>
#   Daniel 'import pdb' Nouri
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
from plone.app.kss import content_replacer

PloneTestCase.setupPloneSite()

class ContentActionMenusTestCase(KSSAndPloneTestCase):

    def afterSetUp(self):
        KSSAndPloneTestCase.afterSetUp(self)
        self.setDebugRequest()
        self.loginAsPortalOwner()
        self.fpage = self.portal['front-page']

    # --
    # test the Kss methods
    # --

    def testReplaceContentRegion(self):
        req = self.portal.REQUEST
        view = content_replacer.ContentView(self.fpage, req)
        result = view.replaceContentRegion(self.fpage.absolute_url(), tabid='contentview-edit')
        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
                         [('replaceHTML', 'region-content', 'htmlid'),
                          ('setAttribute', 'ul.contentViews li', 'css'),
                          ('setAttribute', 'contentview-edit', 'htmlid'),
                          ('replaceHTML', 'contentActionMenus', 'htmlid'),
                         ])

    def testChangeViewTemplate(self):
        # Let's set the default page on front-page,
        # should set default layout of portal
        req = self.portal.REQUEST
        self.assertEqual(self.portal.getLayout(), 'folder_listing')
        view = content_replacer.ContentMenuView(self.fpage, req)
        url = self.fpage.absolute_url() + '?templateId=atct_album_view'
        result = view.changeViewTemplate(url)
        self.assertEqual(self.portal.getLayout(), 'atct_album_view')
        
        resh = req.RESPONSE.headers
        self.assertEqual(resh['status'], '200 OK')
        self.failUnless(req.RESPONSE.cookies['statusmessages'].has_key('expires'), 'cookies not expired')

    def testKssCutObject(self):
        req = self.portal.REQUEST
        # XXX This menu is missing from front page, so we test them on the user folder.
        view = content_replacer.ContentMenuView(self.folder, req)
        result = view.cutObject()

        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
                         [('replaceHTML', 'contentActionMenus', 'htmlid'),
                          ('setStyle', '.portalMessage', 'css'),
                          ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
                          ('setAttribute', 'kssPortalMessage', 'htmlid'),
                          ('setStyle', 'kssPortalMessage', 'htmlid'),
                         ])

    def testCutObject(self):
        req = self.portal.REQUEST
        self.failIf(req.RESPONSE.cookies.has_key('__cp'), 'has cut cookie')
        # XXX This menu is missing from front page, so we test them on the user folder.
        view = content_replacer.ContentMenuView(self.folder, req)
        result = view.cutObject()
        resh = req.RESPONSE.headers
        self.assertEqual(resh['status'], '200 OK')
        self.failUnless(req.RESPONSE.cookies.has_key('__cp'), 'no cut cookie')
        
    def testKssCopyObject(self):
        req = self.portal.REQUEST
        # XXX This menu is missing from front page, so we test them on the user folder.
        view = content_replacer.ContentMenuView(self.folder, req)

        result = view.copyObject()
        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
                         [('replaceHTML', 'contentActionMenus', 'htmlid'),
                          ('setStyle', '.portalMessage', 'css'),
                          ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
                          ('setAttribute', 'kssPortalMessage', 'htmlid'),
                          ('setStyle', 'kssPortalMessage', 'htmlid'),
                         ])

    def testCopyObject(self):
        req = self.portal.REQUEST
        self.failIf(req.RESPONSE.cookies.has_key('__cp'), 'has copy cookie')
        # XXX This menu is missing from front page, so we test them on the user folder.
        view = content_replacer.ContentMenuView(self.folder, req)
        result = view.copyObject()
        resh = req.RESPONSE.headers
        self.assertEqual(resh['status'], '200 OK')
        self.failUnless(req.RESPONSE.cookies.has_key('__cp'), 'no copy cookies')

    def testChangeWorkflowState(self):
        # change the state of the front-page to published
        # I suppose to have the publish transition available
        req = self.portal.REQUEST
        view = content_replacer.ContentMenuView(self.fpage, req)
        url = self.fpage.absolute_url() + '/content_status_modify?workflow_action=publish'
        result = view.changeWorkflowState(url)
        self.assertEqual([(r['name'], r['selector'], r['selectorType']) for r in result],
                         [
                          ('replaceHTML', '.contentViews', 'css'),
                          ('replaceHTML', 'contentActionMenus', 'htmlid'),
                          ('setStyle', '.portalMessage', 'css'),
                          ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
                          ('setAttribute', 'kssPortalMessage', 'htmlid'),
                          ('setStyle', 'kssPortalMessage', 'htmlid'),
                         ])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ContentActionMenusTestCase),
        ))
