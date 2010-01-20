# Copyright (c) 2005
# Authors:
#   Godefroid Chapelle <gotcha@bubblenet.be>
#   Tarek Ziade <tz@nuxeo.com>
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
import unittest, os
from zope.testing import doctest
from Testing.ZopeTestCase import ZopeTestCase
from kss.core.tests.base import KSSViewTestCase
from Products.Five.zcml import load_string, load_config
import kss.demo

try:
    import Products.Five
except AttributeError:
    from kss.demo.simplecontent_z3 import SimpleContent
else:
    from kss.demo.simplecontent import SimpleContent

class KSSDemoTestCase(KSSViewTestCase):

    class layer(KSSViewTestCase.layer):
        @classmethod
        def setUp(cls):
            load_config('meta.zcml', package=kss.demo)
            load_config('configure.zcml', package=kss.demo)

    def afterSetUp(self):
        KSSViewTestCase.afterSetUp(self)
        self.setDebugRequest()
        self.folder._setObject('demo', SimpleContent('Demo', 'Demo'))
        self.view = self.folder.demo.restrictedTraverse('getDivContent')

    def test_instantiation(self):
        view = self.view
        commands = view.getCommands()
        self.assertNotEquals(view, None)

    # XXX This shows the idea of how the commands output can be
    # tested by using DebugTestRequest. 
    def test_getDivContent(self):
        view = self.view
        commands = view.getCommands()
        res = view.getDivContent()
        self.assertEquals(res, [
            {'selectorType': '', 'params': {
                    'html': u'<![CDATA[<h1>it worked</h1>]]>',
                    'withKssSetup': u'True',
                }, 'name': 'replaceInnerHTML', 'selector': 'div#demo'}, 
            {'selectorType': '', 'params': {
                    'html': u'<![CDATA[<h1 id="workedagain">it worked&#160;again</h1>]]>',
                    'withKssSetup': u'True',
                }, 'name': 'replaceInnerHTML', 'selector': 'div#demo'},
            ])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(KSSDemoTestCase),
        ))
