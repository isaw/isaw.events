# Copyright (c) 2006
# Authors: Plone
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

PloneTestCase.setupPloneSite()

class ValidationViewTestCase(KSSAndPloneTestCase):

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)
        # commands will be rendered as data structures,
        self.setDebugRequest()
        self.loginAsPortalOwner()
        context = self.portal['front-page']
        # create content
        self.portal.invokeFactory(id='testfile', type_name='File')
        self.portal.invokeFactory(id='testdoc', type_name='Document')

    # --
    # test the Kss methods
    # --

    def testValidateFormWithEvents(self):
        """Test validating a form works with events
        """
        # Set up a view 
        context = self.portal.testdoc
        view = context.restrictedTraverse('kssValidateForm')
        # this form contains a file field that needs to be ignored. 
        data = {'': 'A kiv\xc3\xa1lasztott elemek elt\xc3\xa1vol\xc3\xadt\xc3\xa1sa', 'allowDiscussion': 'None',
            'cmfeditions_save_new_version': 'false', 'contributors': [],
            'creators': ['ree'], 'description': '', 'description_text_format':
            'text/plain', 'effectiveDate': '', 'effectiveDate_ampm': '',
            'effectiveDate_day': '00', 'effectiveDate_hour': '00',
            'effectiveDate_minute': '00', 'effectiveDate_month': '00',
            'effectiveDate_year': '2006', 'excludeFromNav': '0',
            'excludeFromNav_visible': 'false', 'expirationDate': '',
            'expirationDate_ampm': '', 'expirationDate_day': '00',
            'expirationDate_hour': '00', 'expirationDate_minute': '00',
            'expirationDate_month': '00', 'expirationDate_year': '2006',
            'fieldset': 'default', 'file_file':
            '', 'id':
            'file.2006-12-21.4001159106', 'language': 'Meghat\xc3\xa1rozatlan nyelv(a port\xc3\xa1l alap\xc3\xa9rtelmezett nyelve)', 'last_referer':
            'http://localhost:9888/new16/uacheckin.pdf/view?portal_status_message=Changes%20saved.',
            'relatedItems': [''], 'rights': '', 'rights_text_format': 'text/plain',
            'subject_existing_keywords': [''], 'subject_keywords': [], 'title': 'The new title'}
            
        result = view.kssValidateForm(data)
        
    def testValidateForm(self):
        """Test validating a form works
        """
        # Set up a view 
        context = self.portal.testdoc
        view = context.restrictedTraverse('kssValidateForm')
        # this form contains a file field that needs to be ignored. 
        data = {'': 'A kiv\xc3\xa1lasztott elemek elt\xc3\xa1vol\xc3\xadt\xc3\xa1sa', 'allowDiscussion': 'None',
            'cmfeditions_save_new_version': 'false', 'contributors': [],
            'creators': ['ree'], 'description': '', 'description_text_format':
            'text/plain', 'effectiveDate': '', 'effectiveDate_ampm': '',
            'effectiveDate_day': '00', 'effectiveDate_hour': '00',
            'effectiveDate_minute': '00', 'effectiveDate_month': '00',
            'effectiveDate_year': '2006', 'excludeFromNav': '0',
            'excludeFromNav_visible': 'false', 'expirationDate': '',
            'expirationDate_ampm': '', 'expirationDate_day': '00',
            'expirationDate_hour': '00', 'expirationDate_minute': '00',
            'expirationDate_month': '00', 'expirationDate_year': '2006',
            'fieldset': 'default', 'file_file':
            '', 'id':
            'file.2006-12-21.4001159106', 'language': 'Meghat\xc3\xa1rozatlan nyelv(a port\xc3\xa1l alap\xc3\xa9rtelmezett nyelve)', 'last_referer':
            'http://localhost:9888/new16/uacheckin.pdf/view?portal_status_message=Changes%20saved.',
            'relatedItems': [''], 'rights': '', 'rights_text_format': 'text/plain',
            'subject_existing_keywords': [''], 'subject_keywords': [], 'title': 'The new title', 
            'text': 'XXX'}
            
        result = view.kssValidateForm(data)
        
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
                ('plone-submitCurrentForm', '', 'samenode'),
            ])

    def testValidateFormFailed(self):
        """Test validating a form works, with the title field not validatiing
        """
        # Set up a view 
        context = self.portal.testdoc
        view = context.restrictedTraverse('kssValidateForm')
        # this form contains a file field that needs to be ignored. 
        data = {'': 'A kiv\xc3\xa1lasztott elemek elt\xc3\xa1vol\xc3\xadt\xc3\xa1sa', 'allowDiscussion': 'None',
            'cmfeditions_save_new_version': 'false', 'contributors': [],
            'creators': ['ree'], 'description': '', 'description_text_format':
            'text/plain', 'effectiveDate': '', 'effectiveDate_ampm': '',
            'effectiveDate_day': '00', 'effectiveDate_hour': '00',
            'effectiveDate_minute': '00', 'effectiveDate_month': '00',
            'effectiveDate_year': '2006', 'excludeFromNav': '0',
            'excludeFromNav_visible': 'false', 'expirationDate': '',
            'expirationDate_ampm': '', 'expirationDate_day': '00',
            'expirationDate_hour': '00', 'expirationDate_minute': '00',
            'expirationDate_month': '00', 'expirationDate_year': '2006',
            'fieldset': 'default', 'file_file':
            'thefile.txt', 'id':
            'file.2006-12-21.4001159106', 'language': 'Meghat\xc3\xa1rozatlan nyelv(a port\xc3\xa1l alap\xc3\xa9rtelmezett nyelve)', 'last_referer':
            'http://localhost:9888/new16/uacheckin.pdf/view?portal_status_message=Changes%20saved.',
            'relatedItems': [''], 'rights': '', 'rights_text_format': 'text/plain',
            'subject_existing_keywords': [''], 'subject_keywords': [], 'title': '', 'text': 'XXX'}
        
        result = view.kssValidateForm(data)
        
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
                 ('setStyle', '.portalMessage', 'css'),
                 ('replaceInnerHTML', 'kssPortalMessage', 'htmlid'),
                 ('setAttribute', 'kssPortalMessage', 'htmlid'),
                 ('setStyle', 'kssPortalMessage', 'htmlid'),
                 ('clearChildNodes', 'div.field div.fieldErrorBox', 'css'),
                 ('replaceInnerHTML', 'div#archetypes-fieldname-title div.fieldErrorBox', 'css'), 
                 ('setAttribute', 'archetypes-fieldname-title', 'htmlid'),
            ])

    def testValidateFormWithUploads(self):
        """Test validating a form works with uploads
        """
        # Set up a view 
        context = self.portal.testfile
        view = context.restrictedTraverse('kssValidateForm')
        # this form contains a file field that needs to be ignored. 
        data = {'': 'A kiv\xc3\xa1lasztott elemek elt\xc3\xa1vol\xc3\xadt\xc3\xa1sa', 'allowDiscussion': 'None',
        'cmfeditions_save_new_version': 'false', 'contributors': [],
        'creators': ['ree'], 'description': '', 'description_text_format':
        'text/plain', 'effectiveDate': '', 'effectiveDate_ampm': '',
        'effectiveDate_day': '00', 'effectiveDate_hour': '00',
        'effectiveDate_minute': '00', 'effectiveDate_month': '00',
        'effectiveDate_year': '2006', 'excludeFromNav': '0',
        'excludeFromNav_visible': 'false', 'expirationDate': '',
        'expirationDate_ampm': '', 'expirationDate_day': '00',
        'expirationDate_hour': '00', 'expirationDate_minute': '00',
        'expirationDate_month': '00', 'expirationDate_year': '2006',
        'fieldset': 'default', 'file_file':
        '/home/ree/docs/canon_biztosito/melleklet.odt', 'id':
        'file.2006-12-21.4001159106', 'language': 'Meghat\xc3\xa1rozatlan nyelv (a port\xc3\xa1l alap\xc3\xa9rtelmezett nyelve)', 'last_referer':
        'http://localhost:9888/new16/uacheckin.pdf/view?portal_status_message=Changes%20saved.',
        'relatedItems': [''], 'rights': '', 'rights_text_format': 'text/plain',
        'subject_existing_keywords': [''], 'subject_keywords': [], 'title': 'New title'}
        
        result = view.kssValidateForm(data)
        
        self.assertEqual([(r['name'], r['selector'], r['selectorType'])
                             for r in result], [
                ('plone-submitCurrentForm', '', 'samenode'),
            ])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ValidationViewTestCase),
        #doctest.DocTestSuite('archetypes.kss.fields'),
        ))
